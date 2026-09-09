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
from pypdf.annotations import Link

from . import catalog as ordering
from .collection import ROOT
from .print_content import data_url, excerpt, prepare
from .settings import FONTS, geometry, load, validate

SAMPLE = []
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
                 'rule': s['rule_color'], 'cover-color': s['cover_color'],
                 'cover-height': str(s['page_height']) + 'pt',
                 'contents-size': str(s['contents_size']) + 'pt', 'contents-columns': s['contents_columns']}
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


def build(selected=None, settings=None, root=ROOT, output=None, excerpts=None,
          full=False, book_path=None, check_only=False):
    s = validate(dict(settings), root) if settings is not None else load(root=root)
    if full and (selected is not None or excerpts):
        raise ValueError('Full export uses all included essays without excerpts; do not combine it with essay selections or excerpt rules.')
    if excerpts is None:
        excerpts = json.loads((root / 'config/sample-selection.json').read_text()) if selected is None and not full else {}
    catalog = json.loads((root / 'data/catalog.json').read_text(encoding='utf-8'))
    local = root / 'config/book.local.json'
    book_path = Path(book_path) if book_path is not None else local if local.exists() else root / 'config/book.json'
    book = json.loads(book_path.read_text(encoding='utf-8-sig'))
    ordering.validate(book, catalog)
    author = book.get('author', 'Paul Graham')
    title_text = book.get('title', 'Essays')
    source_credit = book.get('source_credit', 'Writing by Paul Graham. Original chapter attribution is retained in the text. Sources: paulgraham.com.')
    selected = [k for k, v in book['essays'].items() if v['included']] if full else list(SAMPLE if selected is None else selected)
    if not selected or len(set(selected)) != len(selected):
        raise ValueError('Choose at least one included essay, with no repeated selections.')
    unknown = set(selected) - set(book['essays'])
    if unknown:
        raise ValueError('Unknown essay selection: ' + ', '.join(unknown))
    excluded = [key for key in selected if not book['essays'][key]['included']]
    if excluded:
        raise ValueError('Selected essays are excluded in book settings: ' + ', '.join(excluded))
    records = [(section, r) for section in book['sections'] for r in ordering.ordered(book, catalog, section) if r['id'] in selected]
    print(f"Selected {len(records)} essays; intentionally excluded {sum(not v['included'] for v in book['essays'].values())}. Book choices: {book_path}", flush=True)
    prepared, failures = [], []
    for position, (section, r) in enumerate(records, 1):
        try:
            prepared.append((section, r, *prepare(r, root, s['note_returns'], s['include_images'])))
        except (ValueError, OSError, KeyError) as error:
            failures.append(f"{r['title']} [{r['id']}]: {error}")
        if position % 25 == 0 or position == len(records):
            print(f'Checked content {position}/{len(records)}; preparation failures: {len(failures)}.', flush=True)
    if failures:
        raise ValueError(f'{len(failures)} selected essays could not be prepared; no PDF created.\n' + '\n'.join(failures))
    for index, (section, r, content, evidence) in enumerate(prepared):
        if r['id'] in excerpts:
            content, evidence['excerpt'] = excerpt(content, excerpts[r['id']])
            evidence['excerpt_rule'] = excerpts[r['id']]
            evidence['source_note_references'] = evidence['note_references']
            evidence['note_references'] = len(BeautifulSoup(content, 'html.parser').select('a[href^="#"]:not(.note-return)'))
            prepared[index] = (section, r, content, evidence)
    print(f'Content checks passed for {len(prepared)} essays.', flush=True)
    if check_only:
        return None
    g = geometry(s)
    css = styles(s, root)
    margins = (g['text_top'], s['page_width'] - g['text_left'] - g['text_width'],
               s['page_height'] - g['text_top'] - g['text_height'], g['text_left'])
    output = Path(output) if output else root / 'output'
    output.mkdir(parents=True, exist_ok=True)
    kind = 'full' if full else 'sample'
    stem = kind + '-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
    if full and book.get('output_name'):
        name = book['output_name']
        if not isinstance(name, str) or Path(name).name != name or not name.endswith('.pdf') or any(c in name for c in '/\\:'):
            raise ValueError('Output name must be a PDF filename without folders.')
        stem = Path(name).stem
    pdf_path = output / (stem + '.pdf')
    build_record = dict(schema_version=1, kind=kind, created_at=datetime.now(timezone.utc).isoformat(),
                        approval='Export does not establish layout approval or device testing; see docs/sample-review.md.', settings=s, geometry=g,
                        tools={name: version(name) for name in ('playwright', 'pypdf', 'pypdfium2')},
                        font_assets=json.loads((root / 'assets/fonts/manifest.json').read_text()),
                        essays=[], intentionally_excluded=[k for k, v in book['essays'].items() if not v['included']],
                        outside_sample=[r['id'] for r in catalog['essays'] if r['id'] not in selected], failures=[])
    build_record['selection_mode'] = 'all_included' if full else 'selected_sample'
    build_record['book_choices'] = book
    build_record['book_choices_file'] = str(book_path)
    build_record['outside_selection'] = build_record.pop('outside_sample')
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
                body += '<div class="meta">' + html.escape(author.upper()) + (' · Publication date unknown' if not record.get('date') else '')
                if evidence.get('excerpt'):
                    body += '<br>EXCERPT · ' + html.escape(evidence['excerpt'])
                body += '</div><article class="reading">' + content + '</article>'
                print(f"Typesetting {len(essay_pdfs)+1}/{len(prepared)}: " + record['title'], flush=True)
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
            cover = cover.replace('Paul<br>Graham<br><i>Essays</i>', html.escape(author).replace(' ', '<br>', 1) + '<br><i>' + html.escape(title_text) + '</i>')
            if s['cover_artwork']:
                from PIL import Image
                artwork = root / s['cover_artwork']
                with Image.open(artwork) as im:
                    mime = Image.MIME[im.format]
                cover = ('<div class="illustrated-cover"><img class="cover-art" src="' + data_url(artwork, mime)
                         + '"><div class="cover-lettering"><div class="cover-author">' + html.escape(author)
                         + '</div><h1>' + html.escape(title_text) + '</h1></div></div>')
                build_record['cover_sha256'] = hashlib.sha256(artwork.read_bytes()).hexdigest()
            cover_pdf = render(page, cover, css, s, (0, 0, 0, 0))
            summary = (str(len(records)) + ' essays by ' + author if full
                       else str(len(records)) + '-essay preview of the reading edition')
            title = ('<div class="title-page"><div class="edition-introduction">'
                     + '<div class="eyebrow">THE READING EDITION</div>'
                     + '<h1 class="edition-lead">About this edition</h1>'
                     + '<p class="edition-summary">' + html.escape(summary) + '</p>')
            if book.get('reading_tips'):
                title += '<h2>How to use this book</h2><ul class="reading-tips">'
                title += ''.join('<li>' + html.escape(tip) + '</li>' for tip in book['reading_tips'])
                title += '</ul>'
            elif book.get('format_note'):
                title += '<h2>How to use this book</h2><p>' + html.escape(book['format_note']) + '</p>'
            title += '</div><div class="compiler-details">'
            if book.get('compiled_by'):
                title += '<p class="compiler">Compiled by ' + html.escape(book['compiled_by']) + '</p>'
            edition_details = []
            if book.get('edition_version'):
                edition_details.append('Version ' + html.escape(book['edition_version']))
            if book.get('edition_updated'):
                updated = datetime.strptime(book['edition_updated'], '%Y-%m-%d')
                edition_details.append('Compilation updated ' + updated.strftime('%d %B %Y'))
            if edition_details:
                title += '<p class="edition-details">' + '<br>'.join(edition_details) + '</p>'
                # Use the complete included selection even when printing a short preview.
                dates = [r['date'] for r in catalog['essays']
                         if book['essays'][r['id']]['included'] and r.get('date')]
                if dates:
                    latest = datetime.strptime(max(dates)[:7], '%Y-%m')
                    title += '<p class="edition-details">Latest dated essay in this edition: ' + latest.strftime('%B %Y') + '</p>'
            if book.get('project_url'):
                title += ('<p class="project-credit">Project on GitHub<br><a href="'
                          + html.escape(book['project_url'], quote=True) + '">'
                          + html.escape(book['project_url'].removeprefix('https://')) + '</a></p>')
            if book.get('linkedin_url'):
                title += ('<p><a class="linkedin-icon" aria-label="LinkedIn profile" href="'
                          + html.escape(book['linkedin_url'], quote=True) + '">in</a></p>')
            if book.get('disclaimer'):
                title += '<p class="ownership-note">' + html.escape(book['disclaimer']) + '</p>'
            title += '</div></div>'
            title_pdf = render(page, title, css, s, (48, 48, 48, 48))
            front_count = len(PdfReader(BytesIO(cover_pdf)).pages) + len(PdfReader(BytesIO(title_pdf)).pages)
            toc_count = 1
            for attempt in range(4):
                offset, toc, current = front_count + toc_count, '<div class="contents"><div class="eyebrow">A READING SAMPLE</div><h1>Contents</h1><div class="toc-columns">', None
                if full:
                    toc = toc.replace('A READING SAMPLE', 'THE READING EDITION')
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
                toc += '</div></div></div>'
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
                    marks += f'<div style="position:absolute;left:{s["margin_left"]}pt;top:{g["text_top"]+g["text_height"]+5}pt;width:{g["usable_width"]}pt;border-top:.35pt solid var(--rule)"></div>'
                if index >= reading_start and s['notes_background'] == 'dots':
                    pattern = 'position:absolute;background-image:radial-gradient(var(--rule) .55pt,transparent .65pt);background-size:12pt 12pt;'
                    marks += f'<div style="{pattern}left:{s["page_width"]-s["margin_right"]-g["right_width"]}pt;top:{g["text_top"]}pt;width:{g["right_width"]}pt;height:{g["text_height"]}pt"></div>'
                    marks += f'<div style="{pattern}left:{s["margin_left"]}pt;top:{g["text_top"]+g["text_height"]}pt;width:{g["usable_width"]}pt;height:{g["bottom_height"]}pt"></div>'
                layers.append(f'<div style="position:relative;height:{s["page_height"]}pt;break-after:page">{marks}</div>')
            overlay = PdfReader(BytesIO(render(page, ''.join(layers), css + 'body{background:transparent}', s, (0, 0, 0, 0))))
            if len(overlay.pages) != len(writer.pages):
                raise ValueError('Page-number layer does not match book length.')
            for index, pdf_page in enumerate(writer.pages):
                pdf_page.merge_page(overlay.pages[index])
                pdf_page.compress_content_streams()
                if index:
                    # A single generous hit area covers both the title and number.
                    width = g['text_width'] if index >= reading_start else g['usable_width']
                    header_link = writer.add_annotation(index, Link(
                        rect=(s['margin_left'], s['page_height']-s['margin_top']-16,
                              s['margin_left']+width, s['page_height']-s['margin_top']+3),
                        target_page_index=front_count))
                    header_link[NameObject('/Dest')] = ArrayObject([
                        writer.pages[front_count].indirect_reference, NameObject('/Fit')])
            build_record['contents_start_page'] = front_count + 1
            print(f'Assembling {len(writer.pages)} pages and navigation.', flush=True)
            writer.add_metadata({'/Title': author + ' — ' + title_text + ': ' + ('Reading Edition' if full else 'Reading Sample'), '/Author': author, '/Creator': 'Reading Edition'})
            build_record['page_count'] = len(writer.pages)
            writer.compress_identical_objects()
            # Preserve any prior named edition and its records before publishing the replacement.
            if pdf_path.exists():
                archive = output / 'archive' / (datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8])
                archive.mkdir(parents=True)
                for prior in output.glob(pdf_path.stem + '.*'):
                    if prior.is_file():
                        prior.rename(archive / prior.name)
            # Exclusive creation also guards against concurrent exports.
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
    parser = argparse.ArgumentParser(description='Create a new sample or full PDF from saved essays, without downloading.')
    parser.add_argument('--settings', type=Path, help='JSON overrides; otherwise uses reading-settings.json when present, then defaults')
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--essays', nargs='+', help='Saved essay IDs; defaults to the four-piece trial')
    selection.add_argument('--full', action='store_true', help='Export every included essay in full, using saved book order')
    parser.add_argument('--book', type=Path, help='Book choices; otherwise prefers config/book.local.json over config/book.json')
    parser.add_argument('--check', action='store_true', help='Check settings and prepare selected content; create no PDF (does not check printed layout)')
    parser.add_argument('--output', type=Path, help='Output folder')
    parser.add_argument('--complete-essays', action='store_true', help='Use complete selected pieces instead of the default short trial excerpts')
    args = parser.parse_args()
    try:
        settings_path = args.settings if args.settings is not None else ROOT / 'config/reading-settings.json'
        if args.settings is None and not settings_path.exists():
            settings_path = ROOT / 'config/reading-defaults.json'
        print('Reading settings: ' + str(settings_path), flush=True)
        path = build(args.essays, load(args.settings), output=args.output, excerpts={} if args.complete_essays else None,
                     full=args.full, book_path=args.book, check_only=args.check)
    except Exception as error:
        print(f'Export did not finish: {error}')
        return 1
    if args.check:
        print('Checks passed; no PDF created. Printed layout still needs an export and PDF audit.')
    else:
        print('PDF saved: ' + str(path))
        print('Build record: ' + str(path.with_suffix('.json')))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
