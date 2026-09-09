"""Editorial choices and a review list, independent of downloaded sources."""
import json
import re
from collections import Counter
from bs4 import BeautifulSoup
from .collection import ROOT, save_json

SECTIONS = [
    'Startups & Building Companies', 'Work, Learning & Ambition',
    'Thinking, Writing & Creativity', 'Society, Wealth & Power',
    'Programming & Technology', 'Lisp & Technical Deep Dives',
]
TOPICS = [
    'startup startups founder founders investor investors company companies funding venture customers users business',
    'work learning ambition school college life kids hard determination career curiosity',
    'thinking writing essay essays ideas creativity art painting taste truth argument discovery',
    'society wealth inequality tax taxes politics political power government rich religion economy',
    'programming programmer programmers software technology computer computers language languages hacker hackers spam',
    'lisp lisps macro macros dialect dialects recursive recursion s-expression',
]


def propose(title, text):
    words = Counter(re.findall(r"[a-z]+(?:-[a-z]+)?", text.lower()))
    heading = Counter(re.findall(r'[a-z]+', title.lower()))
    scores = [sum(words[t] + 12 * heading[t] for t in topic.split()) for topic in TOPICS]
    ranked = sorted(range(6), key=lambda i: scores[i], reverse=True)
    section = ranked[0]
    if words['lisp'] >= 10 or heading['lisp'] or heading['lisps']:
        section = 5
    secondary = [SECTIONS[i] for i in ranked if i != section and scores[i] >= max(4, scores[section] * .45)][:2]
    return dict(section=SECTIONS[section], included=True, secondary_topics=secondary,
                review_required=True, reason='Provisional content-term match; editorial review pending.' +
                (' Also overlaps ' + ', '.join(secondary) + '.' if secondary else ''))


def validate(book, catalog):
    sections = book['sections']
    if len(sections) != len(set(sections)) or set(sections) != set(SECTIONS):
        raise ValueError('Section list must contain each of the six sections once.')
    records = catalog['essays']
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)) or len({r['url'] for r in records}) != len(ids):
        raise ValueError('Duplicate source identity or URL.')
    if set(book['essays']) != set(ids):
        raise ValueError('Every catalog essay must have exactly one book choice.')
    for key, choice in book['essays'].items():
        if choice['section'] not in sections or type(choice['included']) is not bool:
            raise ValueError(f'Invalid section or inclusion choice for {key}.')


def ordered(book, catalog, section):
    records = [r for r in catalog['essays'] if book['essays'][r['id']]['section'] == section]
    return sorted(records, key=lambda r: (book['essays'][r['id']].get('order', 10**9), r.get('date') is None, r.get('date') or '', r['source_order']))


def review_text(book, catalog):
    validate(book, catalog)
    counts = Counter(r['status'] for r in catalog['essays'])
    excluded = sum(not c['included'] for c in book['essays'].values())
    lines = ['# Proposed essay order', '', 'Status: Awaiting user review. This file contains titles and source links, not essay text.', '',
             f"Sources: {len(catalog['essays'])}; successful: {counts['success']}; failed/pending: {len(catalog['essays']) - counts['success']}; intentionally excluded: {excluded}.", '',
             'Dates keep only the precision printed in the opening. Unknown dates appear last in source order. All initial assignments are proposals; overlaps are marked. Moving or excluding an essay changes book choices only.', '',
             'Edit `config/book.json`, then run `.\\.venv\\Scripts\\python.exe -m src.catalog` to rebuild this list. Set `included` to false to exclude; optional numeric `order` overrides chronology within a section.', '']
    for section in book['sections']:
        records = ordered(book, catalog, section)
        lines += [f'## {section} ({len(records)})', '', '| Essay | Date | Included | Download | Placement / review |', '| --- | --- | --- | --- | --- |']
        for r in records:
            c = book['essays'][r['id']]
            title = r['title'].replace('|', '\\|')
            reason = c['reason'].replace('|', '\\|')
            if r.get('page_title') and r['page_title'] != r['title']:
                reason += ' Index/page title differs; inspect source.'
            if not r.get('on_index', True):
                reason += ' No longer on latest index; retained.'
            if r.get('error'):
                reason += ' ' + r['error'].replace('|', '\\|')
            if r.get('content_scope'):
                reason += ' ' + r['content_scope']
            for attachment in r.get('attachments', []):
                reason += f" Companion: [{attachment['title']}]({attachment['url']}) — {attachment['status']}; {attachment.get('content_status', 'not ready')}."
            lines.append(f"| [{title}]({r['url']}) | {r.get('date') or 'Unknown — review'} | {'Yes' if c['included'] else 'No'} | {r['status']} | {reason} |")
        lines.append('')
    failures = [(r['title'], a['url']) for r in catalog['essays'] for a in r.get('assets', []) if a['status'] == 'failed']
    lines += ['## Image failures', '', *([f'- {title}: {url}' for title, url in failures] or ['None.']), '']
    return '\n'.join(lines)


def build(root=ROOT):
    catalog = json.loads((root / 'data/catalog.json').read_text(encoding='utf-8'))
    local = root / 'config/book.local.json'
    path = local if local.exists() else root / 'config/book.json'
    book = json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(schema_version=1, sections=SECTIONS.copy(), essays={})
    for r in catalog['essays']:
        if r['id'] not in book['essays']:
            content = (root / r['content']).read_text(encoding='utf-8') if r.get('content') else ''
            book['essays'][r['id']] = propose(r['title'], BeautifulSoup(content, 'html.parser').get_text(' ', strip=True))
    validate(book, catalog)
    save_json(path, book)
    (root / 'docs').mkdir(exist_ok=True)
    (root / 'docs/essay-review.md').write_text(review_text(book, catalog), encoding='utf-8')
    print(f"Review list saved: {root / 'docs/essay-review.md'}")


if __name__ == '__main__':
    build()
