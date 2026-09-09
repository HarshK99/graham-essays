"""Resumable, paced collection. Original bytes are never overwritten."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import time
from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup
import requests

ROOT = Path(__file__).resolve().parents[1]
INDEX = "https://paulgraham.com/articles.html"
MONTHS = "January February March April May June July August September October November December".split()


def now():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def canonical(url):
    parts = urlsplit(url)
    host = parts.netloc.lower()
    if host in ('www.paulgraham.com', 'paulgraham.com'):
        return urlunsplit(('https', 'paulgraham.com', parts.path, parts.query, ''))
    return urlunsplit((parts.scheme, host, parts.path, parts.query, ''))


def identity(url):
    stable = canonical(url)
    parts = urlsplit(stable)
    # The index adds changing cache timestamps to these two fixed chapter URLs.
    if parts.hostname == 'sep.turbifycdn.com' and parts.path in ('/ty/cdn/paulgraham/acl1.txt', '/ty/cdn/paulgraham/acl2.txt'):
        stable = urlunsplit((parts.scheme, parts.netloc, parts.path, '', ''))
    return hashlib.sha256(stable.encode()).hexdigest()[:20]


def decorative(img, title):
    src = urlsplit(img.get('src', ''))
    footer_icon = src.hostname in ('ycombinator.com', 'www.ycombinator.com') and src.path == '/images/y18.gif'
    return footer_icon or int(img.get('width', 100) or 100) <= 15 or (title is not None and img.get('alt') == title)


def discover(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    entries, seen, duplicates = [], set(), []
    for td in soup.select('table > tr > td > table > tr > td'):
        img = td.find('img')
        if not img or not (0 < int(img.get('width', 0)) <= 15 and 0 < int(img.get('height', 0)) <= 15):
            continue
        font = td.find('font')
        a = font.find('a', href=True) if font else None
        if not a:
            continue
        url = canonical(urljoin(INDEX, a['href']))
        if url in seen:
            duplicates.append(url)
            continue
        seen.add(url)
        entries.append(dict(id=identity(url), url=url, title=a.get_text(' ', strip=True), source_order=len(entries)))
    if not entries:
        raise ValueError('No essay rows found; the index structure needs review.')
    return entries, duplicates


def extract(raw, url):
    if urlsplit(url).path.endswith('.txt'):
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('windows-1252')
        if len(text) < 80:
            raise ValueError('Text source is unexpectedly short.')
        return dict(title=None, date=None, date_status='missing — review', text=text,
                    html='<pre>' + html.escape(text) + '</pre>',
                    features={tag: int(tag == 'pre') for tag in ('i', 'em', 'b', 'strong', 'a', 'img', 'table', 'pre')})
    soup = BeautifulSoup(raw, 'html.parser')
    fonts = soup.find_all('font', face=re.compile('verdana', re.I))
    if not fonts:
        raise ValueError('No recognised essay body; original saved for review.')
    font = max(fonts, key=lambda tag: len(tag.get_text()))
    body = font.find_parent('td') or font
    # Some article pages put their full-text download and related links in
    # sibling rows. Preserve those text links without importing site navigation.
    column = list(font.find_parents('td'))[-1] if font.find_parent('td') else body
    extra_links = [str(a) for a in column.find_all('a', href=True)
                   if a not in body.descendants and a.get_text(strip=True)]
    if extra_links:
        aside = soup.new_tag('aside')
        aside['data-source-links'] = 'true'
        for link in extra_links:
            aside.append(BeautifulSoup(link, 'html.parser'))
            aside.append(soup.new_tag('br'))
        body.append(aside)
    text = body.get_text(' ', strip=True)
    if len(text) < 80:
        raise ValueError('Essay body is unexpectedly short; inspect original.')
    # Only explicit opening dates; never infer a publication day or use footer years.
    opening = body.get_text('\n', strip=True)[:1500]
    match = re.search(r'^(' + '|'.join(MONTHS) + r')\s+(?:(\d{1,2}),?\s+)?((?:19|20)\d{2})(?=\s*(?:$|\n|,|\())', opening, re.M)
    date = None
    if match:
        date = f'{match[3]}-{MONTHS.index(match[1]) + 1:02d}'
        if match[2]:
            date += f'-{int(match[2]):02d}'
    else:
        year = re.match(r'((?:19|20)\d{2})\s*\n', opening)
        if year:
            date = year[1]
    title = soup.title.get_text(' ', strip=True) if soup.title else None
    for tag in body.find_all(['script', 'style']):
        tag.decompose()
    for tag in body.find_all(True):
        for attr in list(tag.attrs):
            if attr.lower().startswith('on'):
                del tag[attr]
        for attr in ('href', 'src'):
            if tag.get(attr) and not tag[attr].startswith('#'):
                tag[attr] = urljoin(url, tag[attr])
    features = {tag: len(body.find_all(tag)) for tag in ('i', 'em', 'b', 'strong', 'a', 'img', 'table', 'pre')}
    return dict(title=title, date=date, date_status='explicit' if date else 'missing — review',
                text=text, html=str(body), features=features)


class Fetcher:
    def __init__(self, delay=1.0, attempts=3):
        self.delay, self.attempts, self.last = delay, attempts, 0
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'PersonalReadingEdition/0.2 (paced local archive)'

    def get(self, url):
        for attempt in range(self.attempts):
            time.sleep(max(0, self.delay - (time.monotonic() - self.last)))
            try:
                response = self.session.get(url, timeout=(15, 45))
                response.raise_for_status()
                return response.content, response.url
            except requests.RequestException:
                if attempt + 1 == self.attempts:
                    raise
                time.sleep(2 ** (attempt + 1))
            finally:
                self.last = time.monotonic()


def archive(root, raw, suffix):
    digest = hashlib.sha256(raw).hexdigest()
    path = root / 'data/sources' / (digest + suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(raw)
    return path.relative_to(root).as_posix(), digest


def collect(root=ROOT, refresh=False, fetcher=None):
    fetcher = fetcher or Fetcher()
    path = root / 'data/catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'schema_version': 1, 'essays': []}
    if refresh or not catalog.get('index'):
        raw, resolved = fetcher.get(INDEX)
        entries, duplicates = discover(raw)
        source, digest = archive(root, raw, '.html')
        catalog['index'] = dict(url=INDEX, resolved_url=resolved, retrieved_at=now(), source=source, sha256=digest, duplicates=duplicates)
        old = {r['id']: r for r in catalog['essays']}
        records = []
        for entry in entries:
            record = old.pop(entry['id'], {})
            if record.get('title') and record['title'] != entry['title']:
                record.setdefault('title_history', []).append(record['title'])
            record.update(entry, on_index=True)
            record.setdefault('status', 'pending')
            records.append(record)
        for record in old.values():
            record['on_index'] = False
            records.append(record)
        catalog['essays'] = records
        save_json(path, catalog)
    for n, record in enumerate(catalog['essays'], 1):
        if record['status'] == 'success' and not refresh and not any(a['status'] == 'failed' for a in record.get('assets', [])):
            continue
        record['last_attempt_at'] = now()
        try:
            raw, resolved = fetcher.get(record['url'])
            source, digest = archive(root, raw, '.html')
            if record.get('sha256') and record['sha256'] != digest:
                record.setdefault('versions', []).append({k: record[k] for k in ('source', 'sha256', 'retrieved_at', 'content') if k in record})
            record.update(source=source, sha256=digest, retrieved_at=now(), resolved_url=resolved)
            parsed = extract(raw, resolved)
            assets = []
            body = BeautifulSoup(parsed['html'], 'html.parser')
            for img in body.find_all('img', src=True):
                asset = dict(url=img['src'])
                # Tiny spacers and the image-based title remain in the source;
                # meaningful illustrations are downloaded, including unknown sizes.
                if decorative(img, parsed['title']):
                    asset['status'] = 'decorative — source only'
                else:
                    try:
                        payload, final = fetcher.get(asset['url'])
                        asset_path, fingerprint = archive(root, payload, '.asset')
                        asset.update(status='success', source=asset_path, sha256=fingerprint, resolved_url=final)
                    except requests.RequestException as error:
                        asset.update(status='failed', error=str(error))
                assets.append(asset)
            content, _ = archive(root, parsed.pop('html').encode('utf-8'), '.content.html')
            parsed.pop('text')
            record.update(date=parsed['date'], date_status=parsed['date_status'], page_title=parsed['title'], features=parsed['features'], content=content, assets=assets, status='success', error=None)
        except (requests.RequestException, ValueError) as error:
            record.update(status='failed', error=str(error))
        save_json(path, catalog)
        print(f"{n}/{len(catalog['essays'])} {record['status']}: {record['title']}", flush=True)
    return catalog


def reprocess(root=ROOT):
    """Rebuild reading fragments from saved originals without network access."""
    path = root / 'data/catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    for record in catalog['essays']:
        if not record.get('source'):
            continue
        try:
            raw = (root / record['source']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != record['sha256']:
                raise ValueError('Saved source fingerprint differs; original needs review.')
            parsed = extract(raw, record['resolved_url'])
            content, _ = archive(root, parsed['html'].encode('utf-8'), '.content.html')
            body = BeautifulSoup(parsed['html'], 'html.parser')
            for asset in record.get('assets', []):
                img = body.find('img', src=asset['url'])
                if img and decorative(img, parsed['title']):
                    asset.update(status='decorative — source only')
                    asset.pop('error', None)
            record.update(content=content, date=parsed['date'], date_status=parsed['date_status'],
                          page_title=parsed['title'], features=parsed['features'], status='success', error=None)
        except ValueError as error:
            record.update(status='failed', error=str(error))
    save_json(path, catalog)
    return catalog


def collect_attachments(root=ROOT, fetcher=None):
    """Save author-hosted companion documents referenced by collected pages."""
    fetcher = fetcher or Fetcher()
    path = root / 'data/catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    for record in catalog['essays']:
        if not record.get('content'):
            continue
        soup = BeautifulSoup((root / record['content']).read_text(encoding='utf-8'), 'html.parser')
        previous = {a['url']: a for a in record.get('attachments', [])}
        for a in soup.find_all('a', href=True):
            url = a['href']
            parts = urlsplit(url)
            suffix = Path(parts.path).suffix.lower()
            if parts.hostname != 'sep.turbifycdn.com' or not parts.path.startswith('/ty/cdn/paulgraham/') or suffix not in ('.txt', '.ps', '.pdf', '.lisp'):
                continue
            attachment = previous.setdefault(url, dict(url=url, title=a.get_text(' ', strip=True), format=suffix[1:], status='pending'))
            if re.search(r'Complete Article|BBN Talk Excerpts', attachment['title'], re.I):
                record['content_scope'] = 'Introduction only in main page; full text is a companion document.'
            if attachment['status'] == 'success':
                continue
            try:
                raw, resolved = fetcher.get(url)
                source, digest = archive(root, raw, suffix)
                attachment.update(source=source, sha256=digest, retrieved_at=now(), resolved_url=resolved, status='success', error=None)
                if suffix in ('.txt', '.lisp'):
                    parsed = extract(raw, 'https://local.example/document.txt')
                    content, _ = archive(root, parsed['html'].encode('utf-8'), '.content.html')
                    attachment.update(content=content, content_status='ready')
                else:
                    attachment['content_status'] = 'saved; conversion review required before full export'
            except (requests.RequestException, ValueError) as error:
                attachment.update(status='failed', error=str(error))
            print(f"Companion: {record['title']}: {attachment['title']}: {attachment['status']}", flush=True)
        record['attachments'] = list(previous.values())
        save_json(path, catalog)
    return catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Explicitly fetch index and sources again; preserve previous bytes.')
    parser.add_argument('--reprocess', action='store_true', help='Rebuild reading fragments offline from saved originals.')
    args = parser.parse_args()
    if args.refresh and args.reprocess:
        parser.error('Choose --refresh or --reprocess, not both.')
    try:
        catalog = reprocess() if args.reprocess else collect(refresh=args.refresh)
        if not args.reprocess:
            catalog = collect_attachments()
    except (requests.RequestException, ValueError) as error:
        print(f'Collection stopped: {error}. Saved successes remain available.')
        return 1
    failed = sum(r['status'] != 'success' for r in catalog['essays'])
    assets = sum(a['status'] == 'failed' for r in catalog['essays'] for a in r.get('assets', []))
    attachments = sum(a['status'] != 'success' for r in catalog['essays'] for a in r.get('attachments', []))
    print(f"Sources: {len(catalog['essays'])}; successful: {len(catalog['essays']) - failed}; failed/pending: {failed}; failed images: {assets}; failed companions: {attachments}.")
    return int(bool(failed or assets or attachments))


if __name__ == '__main__':
    raise SystemExit(main())
