"""Direct Chromium PDF export, with explicit book navigation and build records."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path
import uuid

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject

from . import catalog as ordering
from .collection import ROOT
from .print_content import data_url, excerpt, prepare
from .settings import FONTS, geometry, load, validate

SAMPLE = ['c11523703cab29b2850d', '3855b9d49700d8423e1e', 'b5344f6ddd1c17701bd7',
          'ed31db79cd9ddc04671b', 'd650febe466d594d32b3']
LINK_BASE = 'https://reading-edition.invalid/'


def styles(s, root):
    faces = []
    for family in set(s[k] for k in ('body_font', 'label_font', 'code_font')):
        for filename, style, weight in zip(FONTS[family], ('normal', 'italic', 'normal'), (400, 400, 600)):
            if filename:
                uri = data_url(root / 'assets/fonts' / filename, 'font/ttf')
                faces.append(f'@font-face {{font-family:"{family}";font-style:{style};font-weight:{weight};src:url("{uri}");}}')
    variables = {'body': '"' + s['body_font'] + '"', 'label': '"' + s['label_font'] + '"',
                 'code': '"' + s['code_font'] + '"', 'size': str(s['body_size']) + 'pt',
                 'code-size': str(s['code_size']) + 'pt', 'leading': s['line_height'],
                 'note-size': str(s['note_size']) + 'pt', 'alignment': s['alignment'],
                 'paragraph': str(s['paragraph_space']) + 'pt', 'ink': s['text_color'],
                 'paper': s['background_color'], 'accent': s['accent_color'],
                 'cover-height': str(s['page_height']) + 'pt'}
    return ''.join(faces) + ':root{' + ''.join(f'--{k}:{v};' for k, v in variables.items()) + '}' + (root / 'templates/book.css').read_text(encoding='utf-8')


def render(page, body, css, s, margins):
    top, right, bottom, left = margins
    page_css = f'@page {{size:{s["page_width"]}pt {s["page_height"]}pt;margin:{top}pt {right}pt {bottom}pt {left}pt;}}'
    page.set_content('<!doctype html><html lang="en"><meta charset="utf-8"><style>' + css + page_css + '</style><body>' + body + '</body></html>')
    page.evaluate('document.fonts.ready')
    failures = page.evaluate('''() => [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.alt || 'unnamed image')''')
    if failures:
        raise ValueError('Images did not load: ' + ', '.join(failures))
    return page.pdf(print_background=True, prefer_css_page_size=True, tagged=True)


def build(selected=None, settings=None, root=ROOT, output=None, excerpts=None):
    s = validate(dict(settings), root) if settings is not None else load(root=root)
    if excerpts is None:
        excerpts = json.loads((root / 'config/sample-selection.json').read_text()) if selected is None else {}
    selected = SAMPLE if selected is None else list(selected)
    if not selected or len(set(selected)) != len(selected):
        raise ValueError('Choose at least one essay, with no repeated selections.')
    catalog = json.loads((root / 'data/catalog.json').read_text(encoding='utf-8'))
    local = root / 'config/book.local.json'
    book_path = local if local.exists() else root / 'config/book.json'
    book = json.loads(book_path.read_text(encoding='utf-8'))
    ordering.validate(book, catalog)
    unknown = set(selected) - set(book['essays'])
    if unknown:
        raise ValueError('Unknown essay selection: ' + ', '.join(unknown))
    excluded = [key for key in selected if not book['essays'][key]['included']]
    if excluded:
        raise ValueError('Selected essays are excluded in book settings: ' + ', '.join(excluded))
    records = [(section, r) for section in book['sections'] for r in ordering.ordered(book, catalog, section) if r['id'] in selected]
    prepared = [(section, r, *prepare(r, root, s['note_returns'])) for section, r in records]
    for index, (section, r, content, evidence) in enumerate(prepared):
        if r['id'] in excerpts:
            content, evidence['excerpt'] = excerpt(content, excerpts[r['id']])
            evidence['excerpt_rule'] = excerpts[r['id']]
            evidence['source_note_references'] = evidence['note_references']
            evidence['note_references'] = len(BeautifulSoup(content, 'html.parser').select('a[href^="#"]:not(.note-return)'))
            prepared[index] = (section, r, content, evidence)
    g = geometry(s)
    css = styles(s, root)
    margins = (g['text_top'], s['page_width'] - g['text_left'] - g['text_width'],
               s['page_height'] - g['text_top'] - g['text_height'], g['text_left'])
    output = Path(output) if output else root / 'output'
    output.mkdir(parents=True, exist_ok=True)
    stem = 'sample-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
    pdf_path = output / (stem + '.pdf')
    build_record = dict(schema_version=1, kind='sample', created_at=datetime.now(timezone.utc).isoformat(),
                        approval='Trial settings; iPad review pending', settings=s, geometry=g,
                        tools={name: version(name) for name in ('playwright', 'pypdf', 'pypdfium2')},
                        font_assets=json.loads((root / 'assets/fonts/manifest.json').read_text()),
                        essays=[], intentionally_excluded=[k for k, v in book['essays'].items() if not v['included']],
                        outside_sample=[r['id'] for r in catalog['essays'] if r['id'] not in selected], failures=[])
    build_record['layout_sha256'] = hashlib.sha256((root / 'templates/book.css').read_bytes()).hexdigest()
    build_record['book_choices_sha256'] = hashlib.sha256(book_path.read_bytes()).hexdigest()
    for asset in build_record['font_assets']:
        if hashlib.sha256((root / 'assets/fonts' / asset['file']).read_bytes()).hexdigest() != asset['sha256']:
            raise ValueError('Bundled font or licence differs from its recorded version: ' + asset['file'])
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            build_record['browser'] = browser.version
            page = browser.new_page()
            # All fonts and images are embedded data, so export never fetches remote content.
            page.route('http://**/*', lambda route: route.abort())
            page.route('https://**/*', lambda route: route.abort())
            essay_pdfs = []
            previous = None
            for section, record, content, evidence in prepared:
                opener = '<h2>' + html.escape(section) + '</h2>' if section != previous else ''
                body = opener + '<h1>' + html.escape(record['title']) + '</h1>'
                body += '<div class="meta">PAUL GRAHAM' + (' · Publication date unknown' if not record.get('date') else '')
                if evidence.get('excerpt'):
                    body += '<br>EXCERPT · ' + html.escape(evidence['excerpt'])
                body += '</div><article class="reading">' + content + '</article>'
                print('Typesetting: ' + record['title'], flush=True)
                essay_pdfs.append(render(page, body, css, s, margins))
                previous = section
                evidence.pop('print_text')
                build_record['essays'].append(dict(id=record['id'], title=record['title'], section=section,
                    url=record['url'], source=record['source'], source_sha256=record['sha256'],
                    retrieved_at=record['retrieved_at'], **evidence))
            if s['cover'] == 'typographic':
                cover = '<div class="cover"><div class="eyebrow">THE READING EDITION</div><h1>Paul<br>Graham<br><i>Essays</i></h1><div class="edition">A SELECTION<br>WITH ROOM FOR THOUGHT</div></div>'
            else:
                from PIL import Image
                cover_path = root / s['cover']
                with Image.open(cover_path) as im:
                    mime = Image.MIME[im.format]
                cover = '<img style="margin:0;width:100%;height:' + str(s['page_height']) + 'pt;object-fit:contain" src="' + data_url(cover_path, mime) + '">'
                build_record['cover_sha256'] = hashlib.sha256(cover_path.read_bytes()).hexdigest()
            cover_pdf = render(page, cover, css, s, (0, 0, 0, 0))
            title = '<div class="title-page"><div class="eyebrow">PAUL GRAHAM</div><h1>Essays</h1><p>A reading edition</p><div class="colophon">A selection of ' + str(len(records)) + ' pieces, with space to think in the margins.<br><br>Writing by Paul Graham. Original chapter attribution is retained in the text. Sources: paulgraham.com.<br><br>Prepared for personal reading. This sample is not the complete collection.<br><br>' + html.escape(' · '.join(s[k] for k in ('body_font', 'label_font', 'code_font'))) + '<br>Trial typography — device review pending.</div></div>'
            title_pdf = render(page, title, css, s, (48, 48, 48, 48))
            front_count = len(PdfReader(BytesIO(cover_pdf)).pages) + len(PdfReader(BytesIO(title_pdf)).pages)
            toc_count = 1
            for attempt in range(4):
                offset, toc, current = front_count + toc_count, '<div class="contents"><div class="eyebrow">A READING SAMPLE</div><h1>Contents</h1>', None
                for entry, payload in zip(build_record['essays'], essay_pdfs):
                    entry['start_page'] = offset + 1
                    entry['page_count'] = len(PdfReader(BytesIO(payload)).pages)
                    if current != entry['section']:
                        if current is not None:
                            toc += '</div>'
                        toc += '<div class="toc-section"><h2><a href="' + LINK_BASE + entry['id'] + '">' + html.escape(entry['section']) + '</a></h2>'
                        current = entry['section']
                    toc += '<a class="toc-entry" href="' + LINK_BASE + entry['id'] + '"><span>' + html.escape(entry['title']) + '</span><span>' + str(offset + 1) + '</span></a>'
                    offset += entry['page_count']
                toc += '</div></div>'
                toc_pdf = render(page, toc, css, s, (48, 48, 48, 48))
                actual = len(PdfReader(BytesIO(toc_pdf)).pages)
                if actual == toc_count:
                    break
                toc_count = actual
            else:
                raise ValueError('Contents page count did not settle.')
            writer = PdfWriter()
            for payload in (cover_pdf, title_pdf, toc_pdf, *essay_pdfs):
                writer.append(BytesIO(payload), import_outline=False)
            targets = {LINK_BASE + e['id']: e['start_page'] - 1 for e in build_record['essays']}
            for pdf_page in writer.pages:
                for ref in pdf_page.get('/Annots', []):
                    annot = ref.get_object()
                    action = annot.get('/A', {})
                    uri = action.get('/URI')
                    if uri in targets:
                        annot.pop('/A')
                        annot[NameObject('/Dest')] = ArrayObject([writer.pages[targets[uri]].indirect_reference, NameObject('/Fit')])
            writer.add_outline_item('Cover', 0)
            writer.add_outline_item('Title page', len(PdfReader(BytesIO(cover_pdf)).pages))
            writer.add_outline_item('Contents', front_count)
            current, parent = None, None
            for e in build_record['essays']:
                if current != e['section']:
                    parent = writer.add_outline_item(e['section'], e['start_page'] - 1)
                    current = e['section']
                writer.add_outline_item(e['title'], e['start_page'] - 1, parent=parent)
            # Draw title and global page number on one header line, plus the bottom divider.
            layers = []
            reading_start = front_count + toc_count
            for index in range(len(writer.pages)):
                marks = ''
                if index:
                    entry = next((e for e in build_record['essays'] if e['start_page']-1 <= index < e['start_page']-1+e['page_count']), None)
                    heading = html.escape(entry['title']) if entry else ''
                    width = g['text_width'] if entry else g['usable_width']
                    marks += f'<div style="position:absolute;left:{s["margin_left"]}pt;top:{s["margin_top"]}pt;width:{width}pt;display:flex;align-items:baseline;font:9pt/12pt var(--label);color:var(--accent)"><span style="flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{heading}</span><span style="margin-left:12pt">{index + 1}</span></div>'
                if index >= reading_start and s['bottom_notes'] > 0:
                    marks += f'<div style="position:absolute;left:{s["margin_left"]}pt;top:{g["text_top"]+g["text_height"]+5}pt;width:{g["usable_width"]}pt;border-top:.35pt solid #e5e9e5"></div>'
                if index >= reading_start and s['notes_background'] == 'dots':
                    pattern = 'position:absolute;background-image:radial-gradient(#cdd4ce .55pt,transparent .65pt);background-size:12pt 12pt;'
                    marks += f'<div style="{pattern}left:{s["page_width"]-s["margin_right"]-g["right_width"]}pt;top:{g["text_top"]}pt;width:{g["right_width"]}pt;height:{g["text_height"]}pt"></div>'
                    marks += f'<div style="{pattern}left:{s["margin_left"]}pt;top:{g["text_top"]+g["text_height"]}pt;width:{g["usable_width"]}pt;height:{g["bottom_height"]}pt"></div>'
                layers.append(f'<div style="position:relative;height:{s["page_height"]}pt;break-after:page">{marks}</div>')
            overlay = PdfReader(BytesIO(render(page, ''.join(layers), css + 'body{background:transparent}', s, (0, 0, 0, 0))))
            if len(overlay.pages) != len(writer.pages):
                raise ValueError('Page-number layer does not match book length.')
            for index, pdf_page in enumerate(writer.pages):
                pdf_page.merge_page(overlay.pages[index])
            writer.add_metadata({'/Title': 'Paul Graham — Essays: Reading Sample', '/Author': 'Paul Graham', '/Creator': 'iPad Reading Edition'})
            build_record['page_count'] = len(writer.pages)
            # Exclusive creation protects existing exports even under concurrent requests.
            with pdf_path.open('xb') as stream:
                writer.write(stream)
        finally:
            browser.close()
    build_record['pdf_sha256'] = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    build_record['file_bytes'] = pdf_path.stat().st_size
    with pdf_path.with_suffix('.json').open('x', encoding='utf-8') as stream:
        json.dump(build_record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description='Create a new sample PDF from saved essays.')
    parser.add_argument('--settings', type=Path, help='JSON settings overrides')
    parser.add_argument('--essays', nargs='+', help='Saved essay IDs; defaults to the five-piece trial')
    parser.add_argument('--output', type=Path, help='Output folder')
    parser.add_argument('--complete-essays', action='store_true', help='Use complete selected pieces instead of the default short trial excerpts')
    args = parser.parse_args()
    try:
        path = build(args.essays, load(args.settings), output=args.output, excerpts={} if args.complete_essays else None)
    except Exception as error:
        print(f'Export did not finish: {error}')
        return 1
    print('Sample saved: ' + str(path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
