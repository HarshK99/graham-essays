"""Offline checks of source fingerprints and preserved reading content."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from bs4 import BeautifulSoup
from src.collection import extract
from src.catalog import validate


def main():
    catalog = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
    local = ROOT / 'config/book.local.json'
    book = json.loads((local if local.exists() else ROOT / 'config/book.json').read_text(encoding='utf-8'))
    validate(book, catalog)
    errors, checked = [], 0
    for record in catalog['essays']:
        if record['status'] != 'success':
            errors.append(f"{record['title']}: {record['status']}")
            continue
        raw = (ROOT / record['source']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != record['sha256']:
            errors.append(f"{record['title']}: source fingerprint mismatch")
        expected = BeautifulSoup(extract(raw, record['resolved_url'])['html'], 'html.parser')
        saved = BeautifulSoup((ROOT / record['content']).read_text(encoding='utf-8'), 'html.parser')
        if saved.get_text() != expected.get_text() or '\ufffd' in saved.get_text():
            errors.append(f"{record['title']}: text differs or contains replacement characters")
        if [(a.get('href'), a.get('name'), a.get('id')) for a in saved.find_all('a')] != [(a.get('href'), a.get('name'), a.get('id')) for a in expected.find_all('a')]:
            errors.append(f"{record['title']}: links or note anchors differ")
        for tag in ('i', 'em', 'b', 'strong', 'a', 'img', 'table', 'pre'):
            if len(saved.find_all(tag)) != len(expected.find_all(tag)):
                errors.append(f"{record['title']}: {tag} count differs")
        for asset in record.get('assets', []):
            if asset['status'] == 'failed':
                errors.append(f"{record['title']}: image failed: {asset['url']}")
            elif asset['status'] == 'success' and hashlib.sha256((ROOT / asset['source']).read_bytes()).hexdigest() != asset['sha256']:
                errors.append(f"{record['title']}: image fingerprint mismatch")
        for attachment in record.get('attachments', []):
            if attachment['status'] != 'success':
                errors.append(f"{record['title']}: companion download failed")
            elif hashlib.sha256((ROOT / attachment['source']).read_bytes()).hexdigest() != attachment['sha256']:
                errors.append(f"{record['title']}: companion fingerprint mismatch")
        checked += 1
    print(f'Checked {checked}/{len(catalog["essays"])} sources, text, structure, and saved images; {len(errors)} issues.')
    for error in errors:
        print(error)
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
