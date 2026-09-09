"""Prepare saved HTML for print without modifying the archived source."""
import base64
import hashlib
import html
import json
import re
import unicodedata
from bs4 import BeautifulSoup, Comment, NavigableString


def data_url(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def excerpt(content, rule):
    """Keep opening blocks and their linked notes; report the excerpt boundary."""
    soup = BeautifulSoup(content, 'html.parser')
    blocks = list(soup.contents)
    if 'max_blocks' in rule:
        kept = blocks[:rule['max_blocks']]
        description = 'Opening excerpt, with any referenced author notes.'
    else:
        boundary = next((i for i, b in enumerate(blocks) if getattr(b, 'name', '') == 'h3' and b.get_text().startswith(rule['until_heading'])), None)
        if boundary is None:
            raise ValueError('Sample excerpt boundary was not found: ' + rule['until_heading'])
        kept = blocks[:boundary]
        description = 'Opening through the section before ' + rule['until_heading'] + '.'
    result = BeautifulSoup(''.join(map(str, kept)), 'html.parser')
    notes = []
    for a in result.find_all('a', href=True):
        if a['href'].startswith('#') and not result.find(id=a['href'][1:]):
            target = soup.find(id=a['href'][1:])
            if target is None or target.find_parent('p') is None:
                raise ValueError('Cannot carry an excerpt note into the sample: ' + a['href'])
            note = target.find_parent('p')
            if str(note) not in notes:
                notes.append(str(note))
    if notes:
        result.append(BeautifulSoup('<h3 class="notes-heading">Notes to this excerpt</h3>' + ''.join(notes), 'html.parser'))
    for a in result.find_all('a', href=True):
        if a['href'].startswith('#') and not result.find(id=a['href'][1:]):
            # Multiple references may point to one note; keep only returns present here.
            if 'note-return' in a.get('class', []):
                a.decompose()
            else:
                raise ValueError('Excerpt leaves a broken link: ' + a['href'])
    return str(result), description


def chapter_html(text):
    """Reflow prose; retain indentation in code, figures and exercises."""
    blocks = []
    for block in re.split(r'\n\s*\n', text.strip()):
        if re.match(r'^2\.\d+\s', block) or block.strip() in ('Welcome to Lisp', 'Summary', 'Exercises', 'Notes'):
            blocks.append('<h3>' + html.escape(block.strip()) + '</h3>')
        elif any(re.match(r'^(?: {2,}|>|\(|\)|;|\d+$)', line) for line in block.splitlines()):
            blocks.append('<pre>' + html.escape(block) + '</pre>')
        else:
            blocks.append('<p>' + html.escape(' '.join(block.splitlines())) + '</p>')
    return ''.join(blocks)


def prepare(record, root, note_returns=False, include_images=True):
    if record['status'] != 'success':
        raise ValueError('Source is not ready: ' + record['title'])
    if record.get('content_scope'):
        raise ValueError('Full-text companion needs explicit preparation before export: ' + record['title'])
    raw = (root / record['source']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != record['sha256']:
        raise ValueError('Original source fingerprint changed: ' + record['title'])
    source = (root / record['content']).read_text(encoding='utf-8')
    soup = BeautifulSoup(source, 'html.parser')
    # XMP is a raw-text element: reparsing its serialized entities changes text.
    for tag in soup.find_all('xmp'):
        tag.name = 'pre'
    removed = []
    for tag in soup.find_all(string=lambda t: isinstance(t, Comment)):
        tag.extract()
    for tag in soup.select('aside[data-source-links]'):
        removed.append(dict(reason='website related/translation links', text=tag.get_text(' ', strip=True)))
        tag.decompose()
    for tag in soup.find_all(['script', 'style', 'iframe', 'object']):
        tag.decompose()
    assets = {a['url']: a for a in record.get('assets', [])}
    image_rules_path = root / 'config/image-text.json'
    image_rules = json.loads(image_rules_path.read_text(encoding='utf-8')) if image_rules_path.exists() else {}
    image_replacements = []
    for img in soup.find_all('img'):
        asset = assets.get(img.get('src'))
        rule = image_rules.get(asset.get('sha256')) if asset else None
        if not include_images and not (rule and rule['kind'] == 'heading'):
            removed.append(dict(reason='essay image omitted by reading settings', url=img.get('src')))
            img.decompose()
            continue
        if asset and asset['status'].startswith('decorative'):
            removed.append(dict(reason='source title or decorative image', url=img.get('src')))
            img.decompose()
        elif asset and asset['status'] == 'success':
            path = root / asset['source']
            if hashlib.sha256(path.read_bytes()).hexdigest() != asset['sha256']:
                raise ValueError('Saved image fingerprint changed: ' + asset['url'])
            rule = image_rules.get(asset['sha256'])
            if rule:
                image_replacements.append(dict(url=asset['url'], sha256=asset['sha256'], **rule))
                if rule['kind'] == 'heading':
                    heading = soup.new_tag('h3'); heading.string = rule['text']
                    img.replace_with(heading)
                else:
                    removed.append(dict(reason='image title supplied by essay heading' if rule['kind'] == 'title' else 'website footer icon', text=rule['text']))
                    img.decompose()
                continue
            from PIL import Image
            with Image.open(path) as image:
                mime = Image.MIME[image.format]
            img['src'] = data_url(path, mime)
        else:
            raise ValueError('Image has no usable saved record: ' + str(img.get('src')))
    promotions = {'Want to start a startup? Get funded by Y Combinator .',
                  'Watch how this essay was written .',
                  'Like to build things? Try Hacker News .',
                  "You'll find this essay and 14 others in Hackers & Painters ."}
    for table in list(soup.find_all('table')):
        text = ' '.join(table.get_text(' ', strip=True).split())
        if text in promotions:
            removed.append(dict(reason='website promotional banner', text=text))
            table.decompose()
    for tag in list(soup.find_all(['b', 'strong'])):
        if tag.get_text(strip=True) in ('Related:', 'More Info:'):
            removed.append(dict(reason='website related-links label', text=tag.get_text(strip=True)))
            tag.decompose()
    source_text = soup.get_text(' ', strip=True)
    # Repair the source's unclosed table cells explicitly before browser parsing.
    for table in reversed(soup.find_all('table')):
        if not table.find('tr'):
            table.unwrap()
            continue
        # Nested single-cell tables are quotation furniture, not data grids.
        direct_rows = [tr for tr in table.find_all('tr') if tr.find_parent('table') == table]
        if len(direct_rows) == 1 and len(direct_rows[0].find_all(['td', 'th'], recursive=False)) == 1:
            cell = direct_rows[0].find(['td', 'th'], recursive=False)
            quote = soup.new_tag('blockquote')
            for child in list(cell.contents):
                quote.append(child.extract())
            children = [c for c in quote.contents if not isinstance(c, NavigableString) or str(c).strip()]
            if len(children) == 1 and getattr(children[0], 'name', None) == 'blockquote':
                quote = children[0].extract()
            table.replace_with(quote)
            continue
        rows = []
        for tr in direct_rows:
            cells = []
            for td in tr.find_all(['td', 'th']):
                cell = BeautifulSoup(str(td), 'html.parser').find(['td', 'th'])
                for nested in list(cell.find_all(['td', 'th'])):
                    nested.decompose()
                own = cell.decode_contents()
                cells.append('<td>' + own + '</td>')
            rows.append('<tr>' + ''.join(cells) + '</tr>')
        table.replace_with(BeautifulSoup('<table>' + ''.join(rows) + '</table>', 'html.parser'))
    for tag in list(soup.find_all(['font', 'center'])):
        tag.unwrap()
    for p in list(soup.find_all('p')):
        p.insert_before(soup.new_tag('br')); p.insert_before(soup.new_tag('br'))
        p.append(soup.new_tag('br')); p.append(soup.new_tag('br')); p.unwrap()
    if soup.td and soup.td.parent == soup:
        soup.td.unwrap()
    for tag in soup.find_all(True):
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in ('href', 'src', 'alt', 'id', 'name', 'colspan', 'rowspan')}
    if len(soup.find_all('pre')) == 1 and len(soup.get_text()) == len(soup.pre.get_text()):
        chapter = soup.pre.get_text()
        promotion = re.search(r'\n-{10,}\s*Available at: http://www\.amazon\.com/[^\n]+\s*$', chapter)
        if promotion:
            removed.append(dict(reason='trailing book purchase link', text=promotion.group().strip()))
            chapter = chapter[:promotion.start()]
            source_text = chapter
        soup = BeautifulSoup(chapter_html(chapter), 'html.parser')
        in_notes = False
        for block in soup.find_all(['p', 'pre', 'h3']):
            if block.name == 'h3' and block.get_text(strip=True) == 'Notes':
                in_notes = True
            if in_notes and block.name == 'p' and re.match(r'^\[\d+\]', block.get_text()):
                n = re.match(r'^\[(\d+)\]', block.get_text())[1]
                anchor = soup.new_tag('a', id='chapter-note-' + n)
                block.insert(0, anchor)
            elif not in_notes:
                for node in list(block.find_all(string=True)):
                    value = re.sub(r'\[(\d+)\]', r'<a href="#chapter-note-\1">[\1]</a>', html.escape(str(node)))
                    node.replace_with(BeautifulSoup(value, 'html.parser'))
    else:
        blocks, pending = [], []
        def flush():
            value = ''.join(pending).strip(); pending.clear()
            value = re.sub(r'^(?:<br\s*/?>\s*)+|(?:<br\s*/?>\s*)+$', '', value).strip()
            if value:
                blocks.append('<p>' + value + '</p>')
        nodes = list(soup.contents)
        i = 0
        while i < len(nodes):
            node = nodes[i]
            if getattr(node, 'name', None) in ('table', 'pre', 'blockquote', 'ul', 'ol', 'img', 'hr', 'h3'):
                flush(); blocks.append(str(node)); i += 1; continue
            if getattr(node, 'name', None) == 'br':
                j, breaks = i, 0
                while j < len(nodes) and (getattr(nodes[j], 'name', None) == 'br' or isinstance(nodes[j], NavigableString) and not str(nodes[j]).strip()):
                    breaks += int(getattr(nodes[j], 'name', None) == 'br'); j += 1
                if breaks >= 2:
                    flush()
                    if breaks >= 4:
                        blocks.append('<div class="pause" aria-hidden="true">· · ·</div>')
                else:
                    pending.append('<br>')
                i = j; continue
            pending.append(html.escape(str(node)) if isinstance(node, NavigableString) else str(node)); i += 1
        flush()
        soup = BeautifulSoup(''.join(blocks), 'html.parser')
    # Source padding at either edge is not an intentional section break.
    while soup.contents and getattr(soup.contents[-1], 'attrs', {}).get('class') == ['pause']:
        soup.contents[-1].extract()
    while soup.contents and getattr(soup.contents[0], 'attrs', {}).get('class') == ['pause']:
        soup.contents[0].extract()
    comparison = BeautifulSoup(str(soup), 'html.parser')
    for ornament in comparison.select('.pause'):
        ornament.decompose()
    norm = lambda t: re.sub(r'\s+', '', unicodedata.normalize('NFKC', t))
    if norm(source_text) != norm(comparison.get_text(' ', strip=True)):
        raise ValueError('Print preparation changed source wording: ' + record['title'])
    for p in soup.find_all(['p', 'h3']):
        children = [n for n in p.contents if not isinstance(n, NavigableString) or str(n).strip()]
        if len(children) == 1 and getattr(children[0], 'name', None) in ('b', 'strong'):
            p.name = 'h3'
        if p.get_text(strip=True) in ('Note', 'Notes'):
            p.name = 'h3'; p['class'] = 'notes-heading'
    # Namespace note targets; return links are optional and disabled in the current trial.
    prefix = record['id'] + '-'
    for tag in soup.find_all(True):
        target = tag.get('id') or tag.get('name')
        if target:
            tag['id'] = prefix + target
            tag.attrs.pop('name', None)
    count = 0
    for a in list(soup.find_all('a', href=True)):
        if a['href'].startswith('#'):
            target = soup.find(id=prefix + a['href'][1:])
            if target is None:
                raise ValueError('Unresolved author-note target: ' + record['title'] + ' ' + a['href'])
            count += 1
            a['href'] = '#' + target['id']; a['id'] = prefix + 'ref-' + str(count)
            paragraph = target.find_parent('p')
            if paragraph:
                paragraph['class'] = list(paragraph.get('class', [])) + ['author-note']
            if note_returns:
                back = soup.new_tag('a', href='#' + a['id']); back['class'] = 'note-return'; back.string = ' Back to text'
                if paragraph:
                    paragraph.append(back)
                else:
                    target.insert_after(back)
    # Keep a note marker attached to the preceding word rather than stranded on a line.
    result = re.sub(r'\s*\[(<a href="#[^"]+" id="[^"]+">\d+</a>)\]', r'&nbsp;<sup class="note-reference">[\1]</sup>', str(soup))
    soup = BeautifulSoup(result, 'html.parser')
    return str(soup), dict(removed=removed, note_references=count,
                          image_replacements=image_replacements,
                          content_sha256=hashlib.sha256(source.encode()).hexdigest(),
                          print_text=soup.get_text(' ', strip=True))
