import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import requests
from src.collection import collect, canonical, discover, extract, Fetcher, reprocess, decorative, identity, collect_attachments, save_json


def index(titles):
    return ('<table><tr><td><table><tr>' + ''.join(f'<td><img width="10" height="10"><font><a href="{url}">{title}</a></font></td>' for url, title in titles) + '</tr></table></td></tr></table>').encode()


BODY = b'<html><title>Example</title><table><tr><td><font face="verdana">July 2023<br>Words &amp; punctuation: <i>emphasis</i>. A sufficiently long essay for the content check.<pre>(+ 1 2)\n  (+ 3 4)</pre><a href="#n1">1</a><b id="n1">Notes</b><table><tr><td>Data</td></tr></table></font></td></tr></table></html>'


class Fake:
    def __init__(self, fail=False, title='Example'):
        self.fail, self.title, self.calls = fail, title, []

    def get(self, url):
        self.calls.append(url)
        if url.endswith('articles.html'):
            return index([('example.html', self.title), ('broken.html', 'Broken')]), url
        if self.fail and url.endswith('broken.html'):
            raise requests.ConnectionError('Simulated failure')
        return BODY, url


class CollectionTests(unittest.TestCase):
    def test_duplicates_and_url_identity(self):
        entries, dupes = discover(index([('example.html', 'One'), ('http://www.paulgraham.com/example.html#x', 'Two')]))
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(dupes), 1)
        self.assertEqual(canonical('http://www.paulgraham.com/example.html'), entries[0]['url'])
        self.assertEqual(identity('https://sep.turbifycdn.com/ty/cdn/paulgraham/acl1.txt?t=1'), identity('https://sep.turbifycdn.com/ty/cdn/paulgraham/acl1.txt?t=2'))

    def test_sibling_full_text_link_is_preserved_and_archived(self):
        raw = b'<html><title>Example</title><table><tr><td><table><tr><td><font face="verdana">July 2023<br>' + b'An introductory paragraph. ' * 5 + b'</font></td></tr><tr><td><a href="https://sep.turbifycdn.com/ty/cdn/paulgraham/example.txt">Full text</a></td></tr></table></td></tr></table></html>'
        result = extract(raw, 'https://paulgraham.com/example.html')
        self.assertIn('Full text', result['html'])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog = collect(root, fetcher=Fake())
            (root / catalog['essays'][0]['content']).write_text(result['html'], encoding='utf-8')
            class Companion(Fake):
                def get(self, url):
                    self.calls.append(url)
                    return b'  (+ 1 2)\n' * 20, url
            fetcher = Companion()
            catalog = collect_attachments(root, fetcher)
            self.assertEqual(catalog['essays'][0]['attachments'][0]['content_status'], 'ready')
            collect_attachments(root, fetcher)
            self.assertEqual(len(fetcher.calls), 2)  # both fixture records share a source fragment

    def test_preserves_structure_and_date_precision(self):
        result = extract(BODY, 'https://paulgraham.com/example.html')
        self.assertEqual(result['date'], '2023-07')
        for fragment in ['<i>emphasis</i>', '(+ 1 2)\n  (+ 3 4)', 'href="#n1"', 'id="n1"', '<table>']:
            self.assertIn(fragment, result['html'])
        self.assertIsNone(extract(BODY.replace(b'July 2023', b'Undated'), 'https://paulgraham.com/example.html')['date'])
        self.assertIsNone(extract(BODY.replace(b'July 2023', b'This follows a talk in April 2001 at BBN.'), 'https://paulgraham.com/example.html')['date'])
        self.assertEqual(extract(BODY.replace(b'July 2023', b'1993'), 'https://paulgraham.com/example.html')['date'], '1993')

    def test_plain_text_code(self):
        raw = b'Chapter 1\n\n' + b'  (+ 1 2) <example> & punctuation\n' * 4
        result = extract(raw, 'https://example.org/chapter.txt?version=1')
        from bs4 import BeautifulSoup
        self.assertEqual(BeautifulSoup(result['html'], 'html.parser').get_text(), raw.decode())
        self.assertIsNone(result['date'])

    def test_decorative_footer_is_explicit(self):
        from bs4 import BeautifulSoup
        icon = BeautifulSoup('<img src="http://ycombinator.com/images/y18.gif">', 'html.parser').img
        self.assertTrue(decorative(icon, 'Example'))
        illustration = BeautifulSoup('<img src="https://example.org/chart.png">', 'html.parser').img
        self.assertFalse(decorative(illustration, 'Example'))

    def test_changed_content_keeps_version_and_offline_reprocess(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = collect(root, fetcher=Fake())
            old_source = original['essays'][0]['source']
            class Changed(Fake):
                def get(self, url):
                    raw, final = super().get(url)
                    return (raw if url.endswith('articles.html') else raw.replace(b'Example', b'Updated')), final
            updated = collect(root, refresh=True, fetcher=Changed())
            self.assertEqual(updated['essays'][0]['versions'][0]['source'], old_source)
            self.assertEqual((root / old_source).read_bytes(), BODY)
            result = reprocess(root)
            self.assertEqual(result['essays'][0]['page_title'], 'Updated')

    def test_failure_resume_and_title_change_preserve_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = collect(root, fetcher=Fake(fail=True))
            source = root / first['essays'][0]['source']
            self.assertEqual(source.read_bytes(), BODY)
            self.assertEqual(first['essays'][1]['status'], 'failed')
            retry = Fake()
            second = collect(root, fetcher=retry)
            self.assertEqual(len(retry.calls), 1)
            self.assertEqual(second['essays'][1]['status'], 'success')
            third = collect(root, refresh=True, fetcher=Fake(title='Changed title'))
            self.assertEqual(third['essays'][0]['id'], first['essays'][0]['id'])
            self.assertEqual(third['essays'][0]['title_history'], ['Example'])
            self.assertEqual(source.read_bytes(), BODY)

    @patch('src.collection.time.sleep')
    def test_bounded_retries(self, sleep):
        fetcher = Fetcher()
        with patch.object(fetcher.session, 'get', side_effect=requests.ConnectionError('offline')) as get:
            with self.assertRaises(requests.ConnectionError):
                fetcher.get('https://paulgraham.com/example.html')
            self.assertEqual(get.call_count, 3)


if __name__ == '__main__':
    unittest.main()
