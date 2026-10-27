# -*- coding: utf-8 -*-
import json
p = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_raw.json'
d = json.load(open(p, encoding='utf-8'))
print('SLIDES', len(d['slides']))
print('COMMENTS', len(d['comments']))
print('---LINKS BY SLIDE---')
for s in d['slides']:
    links = []
    seen = set()
    for L in s['grouped_links'] + s['shape_links']:
        key = (L.get('text'), L.get('url'))
        if key in seen:
            continue
        seen.add(key)
        links.append(L)
    if links:
        print(f"Slide {s['slide']}:")
        for L in links:
            print(f"  ANCHOR: {L.get('text')!r}")
            print(f"  URL: {L.get('url')}")
print('---SLIDE TITLES---')
for s in d['slides']:
    titles = []
    for sh in s['shapes']:
        for para in sh['paras'][:3]:
            if any(x in para for x in ('0', '수출', '대만', '제품', 'PIF', '등록', '통관', '상표', '시판', '라벨', '주의')):
                titles.append(para)
    print(f"S{s['slide']}: {' | '.join(titles[:4])}")
print('---COMMENT PARAS---')
for c in d['comments']:
    print(c['file'])
    for p in c['paras']:
        print(' |', p)
    for u in c['urls']:
        print(' URL:', u)
print('---PKG UNIQUE EXTERNAL URLS---')
seen = set()
for name, u in d['pkg_urls']:
    if u.startswith('http') or u.startswith('mailto'):
        if 'schemas.' in u or 'w3.org' in u or 'purl.org' in u:
            continue
        if u not in seen:
            seen.add(u)
            print(u)
            print('  from', name)
