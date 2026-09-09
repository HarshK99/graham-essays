import json
from pathlib import Path
import tempfile
import unittest
from src.catalog import build, validate, ordered, SECTIONS
from src.collection import collect, save_json
from test_collection import Fake


class CatalogTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
