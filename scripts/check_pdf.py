"""Check actual PDF text, fonts, navigation, writing space and source preservation."""
import argparse
from collections import Counter
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pypdfium2 as pdfium
from pypdf import PdfReader
from src.collection import ROOT
from src.print_content import excerpt, prepare


def normal(text):
    # PDFium marks some line-ending hyphens as U+0002 in bounded extraction.
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text).replace('\u00ad', '').replace('\u200b', '').replace('\x02', '-'))


def check(path, root=ROOT):
    path = Path(path)
    meta = json.loads(path.with_suffix('.json').read_text(encoding='utf-8'))
    reader = PdfReader(path)
    s, g = meta['settings'], meta['geometry']
    issues, fonts, texts, sparse = [], set(), [], []
    internal = external = images = 0
    if hashlib.sha256(path.read_bytes()).hexdigest() != meta['pdf_sha256']:
        issues.append('PDF differs from its build fingerprint.')
    if len(reader.pages) != meta['page_count']:
        issues.append('Page count differs from build record.')
    first_reading = meta['essays'][0]['start_page'] - 1
    page_ids = {p.indirect_reference.idnum: i for i, p in enumerate(reader.pages)}
    def destination_page(dest):
        if isinstance(dest, str):
            target = reader.named_destinations.get(dest)
            return reader.get_destination_page_number(target) if target else None
        return page_ids.get(dest[0].idnum) if dest and hasattr(dest[0], 'idnum') else None
    def outline(items):
        result = []
        for item in items:
            if isinstance(item, list):
                result.extend(outline(item))
            else:
                result.append((item.title, reader.get_destination_page_number(item)))
        return result
    outline_entries = outline(reader.outline)
    for e in meta['essays']:
        if (e['title'], e['start_page'] - 1) not in outline_entries or (e['section'], e['start_page'] - 1) not in outline_entries and e['section'] not in [t for t, _ in outline_entries]:
            issues.append('Bookmark missing or wrong: ' + e['title'])
    with pdfium.PdfDocument(path) as doc:
        for i, p in enumerate(reader.pages):
            if abs(float(p.mediabox.width) - s['page_width']) > 1 or abs(float(p.mediabox.height) - s['page_height']) > 1:
                issues.append(f'Page {i+1}: unexpected dimensions.')
            for font_ref in p['/Resources'].get('/Font', {}).values():
                font = font_ref.get_object()
                for actual in font.get('/DescendantFonts', [font]):
                    actual = actual.get_object()
                    fonts.add(str(actual.get('/BaseFont')))
                    descriptor = actual.get('/FontDescriptor')
                    if not descriptor or not any(k in descriptor.get_object() for k in ('/FontFile', '/FontFile2', '/FontFile3')):
                        issues.append(f'Page {i+1}: font is not embedded: {actual.get("/BaseFont")}')
            for ref in p.get('/Annots', []):
                a = ref.get_object()
                if a.get('/Subtype') != '/Link':
                    issues.append(f'Page {i+1}: unexpected personal annotation.')
                action = a.get('/A', {})
                dest = a.get('/Dest') or action.get('/D')
                if dest is not None:
                    internal += 1
                    if destination_page(dest) is None:
                        issues.append(f'Page {i+1}: broken internal link.')
                elif action.get('/URI'):
                    external += 1
                    if 'reading-edition.invalid' in action['/URI']:
                        issues.append(f'Page {i+1}: unresolved contents link.')
                else:
                    issues.append(f'Page {i+1}: link has no destination.')
            page = doc[i]
            tp = page.get_textpage()
            body = tp.get_text_bounded(left=g['text_left']-2, right=g['text_left']+g['text_width']+2,
                                       top=s['page_height']-g['text_top']+1, bottom=s['page_height']-g['text_top']-g['text_height']-1)
            # Chromium inserts U+2010 for automatic word breaks. Remove only
            # line-ending discretionary hyphens, retaining source punctuation.
            texts.append(re.sub('\u2010(?:\r?\n|$)', '', body))
            if i >= first_reading:
                if len(body.strip()) < 15:
                    issues.append(f'Page {i+1}: empty reading page.')
                if len(body.strip()) < 180:
                    sparse.append(i+1)
                for ci in range(tp.count_chars()):
                    char = tp.get_text_range(ci, 1)
                    if not char.strip():
                        continue
                    left, bottom, right, top = tp.get_charbox(ci)
                    y_top, y_bottom = s['page_height'] - top, s['page_height'] - bottom
                    # Header and footer have their own bands, outside usable writing space.
                    if y_bottom < g['text_top'] - 1 or y_top > s['page_height'] - s['margin_bottom'] - s['footer_height']:
                        continue
                    # Serif ink overhangs alignment edges: j/p on the left,
                    # f on the justified right edge (measured up to 1.51 pt).
                    if left < g['text_left'] - 2 or right > g['text_left'] + g['text_width'] + 2 or y_bottom > g['text_top'] + g['text_height'] + 1:
                        issues.append(f'Page {i+1}: text enters writing space or outer margin.'); break
                for obj in page.get_objects():
                    if obj.type == 3:
                        images += 1
                        left, bottom, right, top = obj.get_bounds()
                        if left < g['text_left']-1 or right > g['text_left']+g['text_width']+1 or s['page_height']-bottom > g['text_top']+g['text_height']+1:
                            issues.append(f'Page {i+1}: image enters writing space.')
            tp.close(); page.close()
    cat = json.loads((root / 'data/catalog.json').read_text(encoding='utf-8'))
    source_records = {r['id']: r for r in cat['essays']}
    preservation = []
    for e in meta['essays']:
        content, evidence = prepare(source_records[e['id']], root, s.get('note_returns', True))
        if e.get('excerpt_rule'):
            content, _ = excerpt(content, e['excerpt_rule'])
        from bs4 import BeautifulSoup
        expected = normal(BeautifulSoup(content, 'html.parser').get_text(' ', strip=True))
        actual = normal(''.join(texts[e['start_page']-1:e['start_page']-1+e['page_count']]))
        # Strip editorial opening, then require the entire prepared source in order.
        start = actual.find(expected[:100])
        passed = start >= 0 and expected in actual[start:]
        if not passed:
            matcher = difflib.SequenceMatcher(None, expected, actual)
            differences = [(tag, expected[a:b][:80], actual[c:d][:80]) for tag, a, b, c, d in matcher.get_opcodes() if tag in ('replace', 'delete')]
            issues.append('Text preservation mismatch: ' + e['title'] + ' ' + repr(differences[:4]))
        preservation.append(dict(title=e['title'], passed=passed, expected_characters=len(expected)))
    result = dict(pdf=path.name, pages=len(reader.pages), embedded_fonts=sorted(fonts), internal_links=internal,
                  external_links=external, images=images, outline_entries=len(outline_entries), sparse_pages_for_visual_review=sparse,
                  text_preservation=preservation, issues=issues)
    path.with_suffix('.checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf', type=Path)
    args = parser.parse_args()
    result = check(args.pdf)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(bool(result['issues']))
