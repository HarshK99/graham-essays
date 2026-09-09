"""Focused final-edition checks: selection, headings, navigation, fonts and images.

This does not compare every word or replace visual/device review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.catalog import ordered


def check(path):
    path = Path(path)
    meta = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
    catalog = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
    book = meta['book_choices']
    expected = [r['id'] for section in book['sections'] for r in ordered(book, catalog, section)
                if book['essays'][r['id']]['included']]
    issues = []
    if [e['id'] for e in meta['essays']] != expected:
        issues.append('Selection or order differs from the included catalog.')
    if hashlib.sha256(path.read_bytes()).hexdigest() != meta['pdf_sha256']:
        issues.append('PDF fingerprint differs from the build record.')
    reader = PdfReader(path)
    page_ids = {p.indirect_reference.idnum: i for i, p in enumerate(reader.pages)}
    named = reader.named_destinations
    contents = meta['contents_start_page'] - 1
    first = meta['essays'][0]['start_page'] - 1
    headers = 0
    targets = set()
    embedded_fonts = set()
    images = 0
    for index, page in enumerate(reader.pages):
        header_found = False
        for ref in page.get('/Annots', []):
            a = ref.get_object()
            dest = a.get('/Dest') or a.get('/A', {}).get('/D')
            if isinstance(dest, str):
                target = reader.get_destination_page_number(named[dest]) if dest in named else None
            else:
                target = page_ids.get(getattr(dest[0], 'idnum', None)) if dest else None
            if dest and target is None:
                issues.append(f'Page {index+1}: unresolved internal destination.')
            if target == contents and float(a['/Rect'][1]) > meta['settings']['page_height']-meta['settings']['margin_top']-20:
                header_found = True
            elif contents <= index < first and target is not None:
                targets.add(target)
        if index:
            headers += header_found
            if not header_found:
                issues.append(f'Page {index+1}: missing header return link.')
        for ref in page['/Resources'].get('/Font', {}).values():
            font = ref.get_object()
            for actual in font.get('/DescendantFonts', [font]):
                actual = actual.get_object()
                descriptor = actual.get('/FontDescriptor')
                descriptor = descriptor.get_object() if descriptor else {}
                embedded = any(k in descriptor for k in ('/FontFile', '/FontFile2', '/FontFile3'))
                embedded = embedded or (actual.get('/Subtype') == '/Type3' and bool(actual.get('/CharProcs')))
                if not embedded:
                    issues.append(f'Page {index+1}: font data is missing.')
                embedded_fonts.add(str(actual.get('/BaseFont') or descriptor.get('/FontName') or 'Type 3 embedded glyphs'))
    if targets != {e['start_page']-1 for e in meta['essays']}:
        issues.append('Contents does not reach every essay opening.')
    def flatten(items):
        result = []
        for item in items:
            result.extend(flatten(item)) if isinstance(item, list) else result.append((item.title, reader.get_destination_page_number(item)))
        return result
    outline = flatten(reader.outline)
    expected_outline = [('Cover', 0), ('Title page', 1), ('Contents', contents)]
    previous = None
    for entry in meta['essays']:
        if entry['section'] != previous:
            expected_outline.append((entry['section'], entry['start_page']-1))
            previous = entry['section']
        expected_outline.append((entry['title'], entry['start_page']-1))
    if outline != expected_outline:
        issues.append('Bookmark order or section destinations differ from the selection.')
    normalize = lambda text: re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))
    with pdfium.PdfDocument(path) as document:
        for entry in meta['essays']:
            if (entry['title'], entry['start_page']-1) not in outline:
                issues.append('Missing essay bookmark: ' + entry['title'])
            page = document[entry['start_page']-1]
            textpage = page.get_textpage()
            if normalize(entry['title']) not in normalize(textpage.get_text_range()):
                issues.append('Missing selectable opening title: ' + entry['title'])
            textpage.close(); page.close()
        for i in range(first, len(document)):
            page = document[i]
            images += sum(obj.type == 3 for obj in page.get_objects())
            page.close()
    if not meta['settings']['include_images'] and images:
        issues.append('Reading pages contain images despite image omission.')
    result = dict(pdf=path.name, pages=len(reader.pages), essays=len(expected),
                  contents_pages=first-contents, header_return_links=headers,
                  reading_images=images, embedded_fonts=sorted(embedded_fonts), issues=issues,
                  scope='Focused selection, opening-title, destination, font and image checks; not an every-word or full layout audit.')
    path.with_suffix('.navigation-checks.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    result = check(parser.parse_args().pdf)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['issues']))
