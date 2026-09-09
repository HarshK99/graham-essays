import unittest
from src.settings import load, validate, geometry, ROOT


class SettingsTests(unittest.TestCase):
    def test_default_writing_spaces_do_not_overlap(self):
        g = geometry(load())
        self.assertAlmostEqual(g['text_width'], 364)
        self.assertAlmostEqual(g['text_height'], 646)
        self.assertAlmostEqual(g['right_width'], 162)
        self.assertAlmostEqual(g['bottom_height'], 114)

    def test_reject_conflicting_and_nonfinite_settings(self):
        for change in ({'right_notes': .99}, {'bottom_notes': 1}, {'margin_left': 900},
                       {'body_size': float('nan')}, {'line_height': 0}, {'page_width': True},
                       {'body_font': 'Missing Font'}, {'cover': 'missing-cover.png'},
                       {'text_color': 'red'}, {'extra_field': 3}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate(load() | change)

    def test_optional_writing_space(self):
        s = validate(load() | {'right_notes': 0, 'bottom_notes': 0})
        self.assertEqual(geometry(s)['text_width'], 540)
        self.assertEqual(geometry(s)['text_height'], 760)

    def test_missing_font_visible(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory, self.assertRaisesRegex(ValueError, 'Missing font'):
            validate(load(), Path(directory))
