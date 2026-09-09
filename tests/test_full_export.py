"""Regression cases found while preparing the full collection; original text only."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from src.print_content import prepare


class FullContentTests(unittest.TestCase):
    def prepared(self, content):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.html").write_text(content, encoding="utf-8")
            record = dict(id="original", title="Original", status="success", source="source.html",
                          content="source.html", sha256=hashlib.sha256(content.encode()).hexdigest())
            result, evidence = prepare(record, root)
            self.assertEqual((root / "source.html").read_text(encoding="utf-8"), content)
            return BeautifulSoup(result, "html.parser"), evidence

    def test_literal_angle_brackets_and_ampersands(self):
        soup, _ = self.prepared("<td>Meet &lt;Your Name&gt; &amp; friends.<br><br>Keep &lt;group&gt;.</td>")
        self.assertEqual(soup.get_text(" ", strip=True), "Meet <Your Name> & friends. Keep <group>.")

    def test_nested_quotation_prints_once(self):
        soup, _ = self.prepared('<td>Opening.<table><tr><td><table><tr><td>A quiet quotation.</td></tr></table></td></tr></table>Ending.</td>')
        self.assertEqual(soup.get_text(" ", strip=True).count("A quiet quotation."), 1)
        self.assertIn("Ending.", soup.get_text())

    def test_rowless_layout_table_retains_prose(self):
        soup, _ = self.prepared("<td><table><!-- row commented out -->The entire essay.<br><br>Its ending.</table></td>")
        self.assertEqual(soup.get_text(" ", strip=True), "The entire essay. Its ending.")

    def test_raw_code_entities_do_not_accumulate_escaping(self):
        soup, _ = self.prepared("<td>Code follows.<xmp>(if (&lt; x 3) &value)</xmp>Ending.</td>")
        self.assertEqual(soup.pre.get_text(), "(if (&lt; x 3) &value)")

    def test_verified_image_heading_becomes_text_and_records_source(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'config').mkdir()
            Image.new('RGB', (30, 10), 'white').save(root / 'heading.png')
            digest = hashlib.sha256((root / 'heading.png').read_bytes()).hexdigest()
            (root / 'config/image-text.json').write_text(json.dumps({digest: {'kind': 'heading', 'text': 'An Original Heading'}}))
            content = '<td><img src="heading.png"><br><br>Original paragraph.</td>'
            (root / 'source.html').write_text(content)
            record = dict(id='original', title='Original', status='success', source='source.html', content='source.html',
                          sha256=hashlib.sha256(content.encode()).hexdigest(),
                          assets=[dict(url='heading.png', source='heading.png', status='success', sha256=digest)])
            result, evidence = prepare(record, root)
            soup = BeautifulSoup(result, 'html.parser')
            self.assertEqual(soup.h3.get_text(), 'An Original Heading')
            self.assertIsNone(soup.img)
            self.assertEqual(evidence['image_replacements'][0]['sha256'], digest)
            self.assertEqual((root / 'source.html').read_text(), content)
