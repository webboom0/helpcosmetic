# -*- coding: utf-8 -*-
import json
import re
from xml.etree import ElementTree as ET
import zipfile

PPTX = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\5개국 도식화(최종)_261023\5개국 도식화(최종)_261023\대만\대만 화장품 수출 절차 도식화_5차 보완 완료_261012.pptx'
OUT = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_comments.txt'

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'


def get_texts(el):
    paras = []
    for p in el.iter(f'{{{A_NS}}}p'):
        runs = []
        for t in p.iter(f'{{{A_NS}}}t'):
            if t.text is not None:
                runs.append(t.text)
        if runs:
            paras.append(''.join(runs))
    return paras


def local(tag):
    return tag.split('}')[-1] if '}' in tag else tag


z = zipfile.ZipFile(PPTX)
lines = []

# Map comment file -> slide via slide rels
comment_to_slide = {}
for i in range(1, 18):
    rels = f'ppt/slides/_rels/slide{i}.xml.rels'
    if rels not in z.namelist():
        continue
    root = ET.fromstring(z.read(rels))
    for rel in root:
        target = rel.attrib.get('Target', '')
        if 'comment' in target.lower():
            comment_to_slide[target.split('/')[-1]] = i

for name in sorted(z.namelist()):
    if not name.startswith('ppt/comments/'):
        continue
    fname = name.split('/')[-1]
    slide = comment_to_slide.get(fname, '?')
    root = ET.fromstring(z.read(name))
    xml = z.read(name).decode('utf-8', errors='replace')
    urls = re.findall(r'https?://[^\s<>"\']+', xml)
    # strip xmlns noise
    urls = [u for u in urls if 'schemas.' not in u and 'w3.org' not in u and 'purl.org' not in u]
    paras = get_texts(root)
    # also grab pc:comment attributes / authors if any
    authors = []
    for el in root.iter():
        if 'author' in el.attrib:
            authors.append(el.attrib.get('author'))
        for k, v in el.attrib.items():
            if 'author' in k.lower() or 'name' in local(k).lower():
                if v and v not in authors:
                    authors.append(v)

    lines.append('=' * 60)
    lines.append(f'SLIDE {slide} | {fname}')
    lines.append('=' * 60)
    for p in paras:
        lines.append(f'| {p}')
    for u in urls:
        lines.append(f'URL: {u}')
    # Also extract any mentions of attachments / drive / 첨부
    for m in re.finditer(r'.{0,40}(첨부|드라이브|drive\.google|파일|양식|계약서).{0,80}', xml, re.I):
        snippet = re.sub(r'<[^>]+>', '', m.group(0))
        snippet = re.sub(r'\s+', ' ', snippet).strip()
        if snippet:
            lines.append(f'SNIP: {snippet}')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Wrote', OUT)
print('Comment->slide map:', comment_to_slide)
