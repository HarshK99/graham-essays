import unittest
import json
from pathlib import Path
import shutil
import tempfile
from src.settings import load, validate, geometry, ROOT


class SettingsTests(unittest.TestCase):
    def test_personal_settings_persist_and_explicit_defaults_reset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'config', root / 'config')
            shutil.copytree(ROOT / 'assets/fonts', root / 'assets/fonts')
            defaults = root / 'config/reading-defaults.json'
            before = defaults.read_bytes()
            local = root / 'config/reading-settings.json'
            local.write_text(json.dumps({'right_notes': .2}), encoding='utf-8-sig')
            for _ in range(2):
                self.assertEqual(load(root=root)['right_notes'], .2)
            self.assertEqual(load(defaults, root)['right_notes'], .25)
            local.rename(root / 'config/reading-settings.backup.json')
            self.assertEqual(load(root=root)['right_notes'], .25)
            self.assertEqual(defaults.read_bytes(), before)
            for value in ([], None, 'bad'):
                local.write_text(json.dumps(value), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'JSON object'):
                    load(root=root)

    def test_default_writing_spaces_do_not_overlap(self):
        g = geometry(load())
        self.assertAlmostEqual(g['text_width'], 391)
        self.assertAlmostEqual(g['text_height'], 703)
        self.assertAlmostEqual(g['right_width'], 135)
        self.assertAlmostEqual(g['bottom_height'], 57)

    def test_reject_conflicting_and_nonfinite_settings(self):
        for change in ({'right_notes': .99}, {'bottom_notes': 1}, {'margin_left': 900},
                       {'body_size': float('nan')}, {'line_height': 0}, {'page_width': True},
                       {'body_font': 'Missing Font'}, {'cover': 'missing-cover.png'},
                       {'text_color': 'red'}, {'extra_field': 3}, {'note_size': 20},
                       {'note_returns': 'false'}, {'alignment': 'center'}):
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
