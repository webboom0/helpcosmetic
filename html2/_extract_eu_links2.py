# -*- coding: utf-8 -*-
import zipfile
import re
from xml.etree import ElementTree as ET

PPTX = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\5개국 도식화(최종)_261023\5개국 도식화(최종)_261023\EU\EU 화장품 수출 절차 도식화_5차 보완_261012_수정.pptx'
OUT = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_links_audit.txt'

z = zipfile.ZipFile(PPTX)
lines = []

# All external targets from any .rels
lines.append('=== ALL EXTERNAL / HTTP TARGETS IN RELS ===')
all_urls = []
for name in sorted(z.namelist()):
    if not name.endswith('.rels'):
        continue
    data = z.read(name).decode('utf-8')
    if 'http' not in data and 'External' not in data:
        continue
    root = ET.fromstring(z.read(name))
    for rel in root:
        target = rel.attrib.get('Target', '')
        mode = rel.attrib.get('TargetMode') or rel.attrib.get(
            '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}TargetMode'
        )
        rtype = rel.attrib.get('Type', '').split('/')[-1]
        rid = rel.attrib.get('Id')
        if mode == 'External' or target.startswith('http') or 'hyperlink' in rtype.lower():
            lines.append(f'{name} | {rid} | {rtype} | {mode} | {target}')
            all_urls.append(target)

# Search entire zip for http URLs
lines.append('\n=== REGEX HTTP URLS IN ALL XML ===')
url_re = re.compile(r'https?://[^\s\"\'<>]+')
seen = set()
for name in sorted(z.namelist()):
    if not (name.endswith('.xml') or name.endswith('.rels')):
        continue
    data = z.read(name).decode('utf-8', errors='replace')
    for m in url_re.findall(data):
        # skip schema namespaces
        if 'schemas.openxmlformats.org' in m or 'schemas.microsoft.com' in m:
            continue
        if 'purl.org' in m or 'w3.org' in m:
            continue
        key = (name, m)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f'{name} | {m}')

# Comments text
lines.append('\n=== COMMENT TEXTS ===')
A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
for name in sorted(z.namelist()):
    if 'comment' not in name.lower():
        continue
    root = ET.fromstring(z.read(name))
    texts = []
    for t in root.iter(f'{{{A_NS}}}t'):
        if t.text:
            texts.append(t.text)
    # also any plain text nodes
    lines.append(f'{name}: {"".join(texts)!r}')
    urls = url_re.findall(z.read(name).decode('utf-8', errors='replace'))
    urls = [u for u in urls if 'schemas.' not in u and 'w3.org' not in u]
    if urls:
        lines.append(f'  urls: {urls}')

# Check for action= attributes (internal jumps, etc.)
lines.append('\n=== hlinkClick WITH action ATTR ===')
for name in sorted(z.namelist()):
    if not name.startswith('ppt/slides/slide'):
        continue
    if not name.endswith('.xml'):
        continue
    data = z.read(name).decode('utf-8')
    if 'hlinkClick' not in data and 'hlinkHover' not in data:
        continue
    root = ET.fromstring(z.read(name))
    for el in root.iter():
        tag = el.tag.split('}')[-1]
        if tag in ('hlinkClick', 'hlinkHover'):
            lines.append(f'{name}: {tag} attribs={dict(el.attrib)}')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Wrote {OUT}')
print(f'Unique external URL count: {len(set(all_urls))}')
for u in sorted(set(all_urls)):
    print(u)
