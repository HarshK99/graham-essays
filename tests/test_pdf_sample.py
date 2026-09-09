import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from bs4 import BeautifulSoup
from pypdf import PdfReader
from src.catalog import SECTIONS
from src.collection import ROOT
from src.pdf_builder import build
from src.print_content import prepare, excerpt
from src.settings import load
from scripts.check_pdf import check


class PdfSampleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for folder in ('assets/fonts', 'templates', 'config'):
            shutil.copytree(ROOT / folder, self.root / folder)
        (self.root / 'data/sources').mkdir(parents=True)
        content = '<td><font>September 2026<br><br>A reader keeps a small notebook. <i>Ideas grow</i> when revisited. [<a href="#n1">1</a>]<br><br><blockquote>A quiet page makes room for a question.</blockquote><br><br><b>Notes</b><br><br>[<a name="n1">1</a>] This is an original note.</font></td>'
        self.record = dict(id='original', title='A Notebook for Tomorrow', url='https://example.org/notebook',
                           status='success', source='data/sources/original.html', content='data/sources/reading.html',
                           sha256=hashlib.sha256(content.encode()).hexdigest(), source_order=0,
                           date='2026-09', retrieved_at='2026-09-09T00:00:00Z', assets=[])
        for name in ('original.html', 'reading.html'):
            (self.root / 'data/sources' / name).write_text(content, encoding='utf-8')
        (self.root / 'data/catalog.json').write_text(json.dumps({'essays': [self.record]}))
        (self.root / 'config/book.json').write_text(json.dumps({'sections': SECTIONS, 'essays': {'original': {'section': SECTIONS[0], 'included': True}}}))
        local = self.root / 'config/book.local.json'
        if local.exists():
            local.unlink()

    def tearDown(self):
        self.temp.cleanup()

    def test_print_notes_and_source_unchanged(self):
        before = (self.root / self.record['source']).read_bytes()
        content, evidence = prepare(self.record, self.root)
        soup = BeautifulSoup(content, 'html.parser')
        self.assertEqual(evidence['note_references'], 1)
        for link in soup.select('a[href^="#"]'):
            self.assertIsNotNone(soup.find(id=link['href'][1:]))
        self.assertEqual(before, (self.root / self.record['source']).read_bytes())
        short, _ = excerpt(content, {'max_blocks': 2})
        self.assertIn('This is an original note.', short)
        self.assertIn('note-return', short)

    def test_incomplete_companion_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Full-text companion'):
            prepare(self.record | {'content_scope': 'Introduction only'}, self.root)

    def test_unclosed_table_cells_are_not_duplicated(self):
        content = '<td><font>Example<br><br><table><tr><td><font>tax<td><font>taken</font></td></font></td></tr><tr><td>1%<td>45%</td></td></tr></table><br><br><br><br></font></td>'
        self.record['sha256'] = hashlib.sha256(content.encode()).hexdigest()
        for key in ('source', 'content'):
            (self.root / self.record[key]).write_text(content)
        result, _ = prepare(self.record, self.root)
        soup = BeautifulSoup(result, 'html.parser')
        self.assertEqual([c.get_text() for c in soup.select('tr:first-child td')], ['tax', 'taken'])
        self.assertFalse(str(soup.contents[-1]).startswith('<div'))

    def test_exports_preserve_navigation_and_do_not_overwrite(self):
        first = build(['original'], root=self.root)
        original = first.read_bytes()
        report = check(first, self.root)
        self.assertEqual(report['issues'], [], report['issues'])
        self.assertGreaterEqual(report['internal_links'], 4)
        from PIL import Image
        Image.new('RGB', (300, 400), '#e9ede7').save(self.root / 'original-cover.png')
        changed = load() | {'body_size': 15, 'right_notes': .2, 'notes_background': 'dots', 'cover': 'original-cover.png'}
        second = build(['original'], changed, root=self.root)
        self.assertNotEqual(first, second)
        self.assertEqual(first.read_bytes(), original)
        self.assertEqual(check(second, self.root)['issues'], [])
        self.assertIn('A Notebook for Tomorrow', ''.join(p.extract_text() for p in PdfReader(second).pages))

    def test_unknown_excluded_and_duplicate_selection_rejected(self):
        for ids in ([], ['missing'], ['original', 'original']):
            with self.assertRaises(ValueError):
                build(ids, root=self.root)
        book = json.loads((self.root / 'config/book.json').read_text())
        book['essays']['original']['included'] = False
        (self.root / 'config/book.json').write_text(json.dumps(book))
        with self.assertRaisesRegex(ValueError, 'excluded'):
            build(['original'], root=self.root)
