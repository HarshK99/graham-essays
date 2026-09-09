"""Validated page settings, measured in PDF points (72 per inch)."""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONTS = {
    'Source Serif 4': ('SourceSerif4-Regular.ttf', 'SourceSerif4-It.ttf', 'SourceSerif4-Semibold.ttf'),
    'Source Sans 3': ('SourceSans3-Regular.ttf', None, 'SourceSans3-Semibold.ttf'),
    'Source Code Pro': ('SourceCodePro-Regular.ttf', None, None),
}


def geometry(s):
    width = s['page_width'] - s['margin_left'] - s['margin_right']
    height = s['page_height'] - s['margin_top'] - s['margin_bottom'] - s['header_height'] - s['footer_height']
    return dict(usable_width=width, usable_height=height,
                text_width=width * (1 - s['right_notes']) - (s['notes_gap'] if s['right_notes'] else 0),
                text_height=height * (1 - s['bottom_notes']),
                text_left=s['margin_left'], text_top=s['margin_top'] + s['header_height'],
                right_width=width * s['right_notes'], bottom_height=height * s['bottom_notes'])


def validate(s, root=ROOT):
    defaults = json.loads((ROOT / 'config/reading-defaults.json').read_text(encoding='utf-8'))
    if set(s) != set(defaults):
        raise ValueError('Settings fields do not match the default preset: ' + ', '.join(sorted(set(s) ^ set(defaults))))
    for key, default in defaults.items():
        if type(default) in (int, float):
            if type(s[key]) not in (int, float) or not math.isfinite(s[key]) or s[key] < 0:
                raise ValueError(f'{key} must be a finite, non-negative number.')
    if type(s['note_returns']) is not bool:
        raise ValueError('note_returns must be true or false.')
    if s['alignment'] not in ('left', 'justify'):
        raise ValueError('Alignment must be left or justify.')
    if not 8 <= s['note_size'] <= s['body_size']:
        raise ValueError('Note size must be at least 8 pt and no larger than body size.')
    for key in ('right_notes', 'bottom_notes'):
        if not 0 <= s[key] < 1:
            raise ValueError(f'{key} must be at least 0 and less than 1 (100%).')
    if not 8 <= s['body_size'] <= 36 or not 8 <= s['code_size'] <= 24 or not 1 <= s['line_height'] <= 2.5:
        raise ValueError('Body size must be 8–36 pt, code size 8–24 pt, and line height 1–2.5.')
    if not 300 <= s['page_width'] <= 1440 or not 400 <= s['page_height'] <= 2000:
        raise ValueError('Page width must be 300–1440 pt and height 400–2000 pt.')
    if s['header_height'] < 18 or s['footer_height'] < 18:
        raise ValueError('Header and footer heights must each be at least 18 pt.')
    g = geometry(s)
    if g['text_width'] < max(144, 12 * s['body_size']) or g['text_height'] < 12 * s['body_size'] * s['line_height']:
        raise ValueError('Page dimensions, outer margins, writing areas and text size leave too little room for reading. Reduce margins/writing areas or increase page dimensions.')
    for key in ('text_color', 'background_color', 'accent_color'):
        if not isinstance(s[key], str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', s[key]):
            raise ValueError(f'{key} must be a six-digit colour such as #252622.')
    for key in ('body_font', 'label_font', 'code_font'):
        if not isinstance(s[key], str) or s[key] not in FONTS:
            raise ValueError(f'{key} must name one of the bundled font families: ' + ', '.join(FONTS))
        for name in FONTS[s[key]]:
            if name and not (root / 'assets/fonts' / name).is_file():
                raise ValueError(f'Missing font: assets/fonts/{name}. Restore the bundled fonts before exporting.')
    if s['notes_background'] not in ('blank', 'dots'):
        raise ValueError('Writing background must be blank or dots.')
    if not isinstance(s['cover'], str) or not s['cover']:
        raise ValueError('Cover must be typographic or a local image path.')
    if s['cover'] != 'typographic' and not (root / s['cover']).is_file():
        raise ValueError('The selected cover image does not exist: ' + s['cover'])
    return s


def load(path=None, root=ROOT):
    s = json.loads((root / 'config/reading-defaults.json').read_text(encoding='utf-8'))
    local = root / 'config/reading-settings.json'
    path = Path(path) if path is not None else local if local.exists() else None
    if path is not None:
        overrides = json.loads(path.read_text(encoding='utf-8-sig'))
        if not isinstance(overrides, dict):
            raise ValueError(f'Settings must be a JSON object of named fields: {path}')
        s.update(overrides)
    return validate(s, root)
