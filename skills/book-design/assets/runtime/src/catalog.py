import math

def validate(book, catalog):
    sections = book['sections']
    if len(sections) != len(set(sections)) or not sections or any(not isinstance(s, str) or not s.strip() for s in sections):
        raise ValueError('Give each manuscript section a unique, nonempty name.')
    records = catalog['essays']
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)) or len({r['url'] for r in records}) != len(ids):
        raise ValueError('Duplicate source identity or URL.')
    if set(book['essays']) != set(ids):
        raise ValueError('Every catalog essay must have exactly one book choice.')
    for key, choice in book['essays'].items():
        if choice['section'] not in sections or type(choice['included']) is not bool:
            raise ValueError(f'Invalid section or inclusion choice for {key}.')
        if 'order' in choice and (type(choice['order']) not in (int, float) or not math.isfinite(choice['order'])):
            raise ValueError(f'Essay order must be a finite number for {key}.')


def ordered(book, catalog, section):
    records = [r for r in catalog['essays'] if book['essays'][r['id']]['section'] == section]
    return sorted(records, key=lambda r: (book['essays'][r['id']].get('order', 10**9), r.get('date') is None, r.get('date') or '', r['source_order']))
