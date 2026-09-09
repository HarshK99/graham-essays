import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from src.catalog import build, validate, ordered, list_essays, SECTIONS
from src.collection import collect, save_json
from test_collection import Fake


class CatalogTests(unittest.TestCase):
    def test_invalid_manual_order_rejected(self):
        catalog = {'essays': [{'id': 'one', 'url': 'https://example.org/one'}]}
        for order in ('first', True, None, float('nan'), float('inf')):
            book = {'sections': SECTIONS, 'essays': {'one': {'section': SECTIONS[0], 'included': True, 'order': order}}}
            with self.subTest(order=order), self.assertRaisesRegex(ValueError, 'finite number'):
                validate(book, catalog)

    def test_move_exclude_and_repeat_preserve_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog = collect(root, fetcher=Fake())
            build(root)
            path = root / 'config/book.json'
            book = json.loads(path.read_text(encoding='utf-8'))
            key = catalog['essays'][0]['id']
            before = (root / catalog['essays'][0]['source']).read_bytes()
            book['essays'][key].update(section=SECTIONS[-1], included=False)
            save_json(path, book)
            build(root)
            after = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(after, book)
            self.assertEqual((root / catalog['essays'][0]['source']).read_bytes(), before)
            self.assertEqual(after['sections'][-1], SECTIONS[-1])
            self.assertIn('intentionally excluded: 1', (root / 'docs/essay-review.md').read_text(encoding='utf-8'))
            after['essays'][key]['section'] = 'invalid'
            with self.assertRaises(ValueError):
                validate(after, catalog)

    def test_private_choices_and_unknown_date_order(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            catalog = collect(root, fetcher=Fake())
            build(root)
            shipped = (root / 'config/book.json').read_bytes()
            book = json.loads(shipped)
            for choice in book['essays'].values():
                choice['section'] = SECTIONS[0]
            catalog['essays'][0]['date'] = None
            catalog['essays'][1]['date'] = '2001-04'
            self.assertEqual(ordered(book, catalog, SECTIONS[0])[0]['id'], catalog['essays'][1]['id'])
            save_json(root / 'config/book.local.json', book)
            build(root)
            self.assertEqual((root / 'config/book.json').read_bytes(), shipped)
            before = (root / 'config/book.local.json').read_bytes()
            review = (root / 'docs/essay-review.md').read_bytes()
            output = StringIO()
            with redirect_stdout(output):
                list_essays(root)
            self.assertIn(catalog['essays'][0]['id'], output.getvalue())
            self.assertIn(catalog['essays'][0]['title'], output.getvalue())
            self.assertEqual((root / 'config/book.local.json').read_bytes(), before)
            self.assertEqual((root / 'docs/essay-review.md').read_bytes(), review)


if __name__ == '__main__':
    unittest.main()
