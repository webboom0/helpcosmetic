# -*- coding: utf-8 -*-
"""Extract all visible text + hyperlinks + comments from Taiwan cosmetics export PPTX."""
import zipfile
import os
import json
import re
from xml.etree import ElementTree as ET

PPTX = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\5개국 도식화(최종)_261023\5개국 도식화(최종)_261023\대만\대만 화장품 수출 절차 도식화_5차 보완 완료_261012.pptx'
OUT_JSON = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_raw.json'
OUT_TXT = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_raw.txt'

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
REL_HYPER = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink'


def local(tag):
    return tag.split('}')[-1] if '}' in tag else tag


def get_texts_by_para(el):
    paras = []
    for p in el.iter(f'{{{A_NS}}}p'):
        runs = []
        for t in p.iter(f'{{{A_NS}}}t'):
            if t.text is not None:
                runs.append(t.text)
        if runs:
            paras.append(''.join(runs))
    return paras


def parse_rels(z, path):
    rels = {}
    if path not in z.namelist():
        return rels
    root = ET.fromstring(z.read(path))
    for rel in root:
        rid = rel.attrib.get('Id')
        target = rel.attrib.get('Target')
        rtype = rel.attrib.get('Type', '')
        mode = rel.attrib.get(f'{{{R_NS}}}TargetMode') or rel.attrib.get('TargetMode')
        rels[rid] = {'target': target, 'type': rtype.split('/')[-1], 'mode': mode, 'full_type': rtype}
    return rels


def shape_bbox(sp):
    for el in sp.iter():
        if local(el.tag) == 'xfrm':
            off = None
            ext = None
            for c in el:
                if local(c.tag) == 'off':
                    off = c
                elif local(c.tag) == 'ext':
                    ext = c
            if off is not None:
                return (
                    int(off.attrib.get('x', 0)),
                    int(off.attrib.get('y', 0)),
                    int(ext.attrib.get('cx', 0)) if ext is not None else 0,
                    int(ext.attrib.get('cy', 0)) if ext is not None else 0,
                )
    return None


def extract_table(tbl):
    rows = []
    for tr in tbl.findall(f'.//{{{A_NS}}}tr'):
        cells = []
        for tc in tr.findall(f'{{{A_NS}}}tc'):
            paras = get_texts_by_para(tc)
            cells.append('\n'.join(paras))
        rows.append(cells)
    return rows


def shape_hyperlinks(slide_root, rels):
    links = []
    for tag in (f'{{{P_NS}}}sp', f'{{{P_NS}}}pic', f'{{{P_NS}}}cxnSp', f'{{{P_NS}}}graphicFrame'):
        for sp in slide_root.iter(tag):
            cNvPr = None
            for el in sp.iter():
                if local(el.tag) == 'cNvPr':
                    cNvPr = el
                    break
            if cNvPr is None:
                continue
            h = None
            for child in cNvPr:
                if local(child.tag) == 'hlinkClick':
                    h = child
                    break
            if h is None:
                continue
            rid = h.attrib.get(f'{{{R_NS}}}id')
            tip = h.attrib.get('tooltip')
            txt_paras = get_texts_by_para(sp)
            txt = ' / '.join(txt_paras) if txt_paras else f"[shape:{cNvPr.attrib.get('name', '')}]"
            target = rels.get(rid, {}).get('target') if rid else None
            links.append({
                'rid': rid,
                'text': txt,
                'url': target,
                'tooltip': tip,
                'kind': 'shape-hlink',
                'name': cNvPr.attrib.get('name'),
            })
    return links


def grouped_hyperlinks(slide_root, rels):
    grouped = []
    for p in slide_root.iter(f'{{{A_NS}}}p'):
        current = None
        for child in p:
            if local(child.tag) != 'r':
                if current:
                    grouped.append(current)
                    current = None
                continue
            rPr = child.find(f'{{{A_NS}}}rPr')
            h = rPr.find(f'{{{A_NS}}}hlinkClick') if rPr is not None else None
            t_el = child.find(f'{{{A_NS}}}t')
            txt = t_el.text if t_el is not None and t_el.text else ''
            if h is not None:
                rid = h.attrib.get(f'{{{R_NS}}}id')
                tip = h.attrib.get('tooltip')
                action = h.attrib.get('action')
                target = rels.get(rid, {}).get('target') if rid else None
                if current and current['rid'] == rid:
                    current['text'] += txt
                else:
                    if current:
                        grouped.append(current)
                    current = {
                        'rid': rid,
                        'text': txt,
                        'url': target,
                        'tooltip': tip,
                        'action': action,
                    }
            else:
                if current:
                    grouped.append(current)
                    current = None
        if current:
            grouped.append(current)
    return grouped


def extract_comments(z):
    comments = []
    for name in z.namelist():
        if not name.startswith('ppt/comments/'):
            continue
        root = ET.fromstring(z.read(name))
        texts = []
        for t in root.iter():
            if local(t.tag) in ('t', 'body', 'text'):
                if t.text and t.text.strip():
                    texts.append(t.text.strip())
            # also a:t
            if local(t.tag) == 't' and t.text:
                pass
        # Prefer a:t paragraphs
        paras = get_texts_by_para(root)
        # Also collect any plain text nodes that look useful
        all_text = []
        for el in root.iter():
            if el.text and el.text.strip() and local(el.tag) in ('t', 'sdtContent', 'txBody'):
                all_text.append(el.text.strip())
        # Get raw XML snippet for debugging attachments/drive links
        xml_str = z.read(name).decode('utf-8', errors='replace')
        urls = re.findall(r'https?://[^\s<>"\']+', xml_str)
        drive = re.findall(r'https?://drive\.google\.com/[^\s<>"\']+', xml_str)
        # Also look for Korean attachment references
        comments.append({
            'file': name,
            'paras': paras,
            'urls': urls,
            'drive_urls': drive,
            'raw_len': len(xml_str),
            'raw_preview': xml_str[:2000],
        })
    return comments


def main():
    z = zipfile.ZipFile(PPTX)
    pres = ET.fromstring(z.read('ppt/presentation.xml'))
    pres_rels = parse_rels(z, 'ppt/_rels/presentation.xml.rels')
    sld_ids = []
    for sldId in pres.findall(f'.//{{{P_NS}}}sldId'):
        rid = sldId.attrib.get(f'{{{R_NS}}}id')
        target = pres_rels[rid]['target']
        sld_ids.append(target if target.startswith('ppt/') else 'ppt/' + target.lstrip('/'))

    results = []
    out_lines = []

    for i, slide_path in enumerate(sld_ids, 1):
        slide_root = ET.fromstring(z.read(slide_path))
        base = os.path.basename(slide_path)
        rels_path = f'ppt/slides/_rels/{base}.rels'
        rels = parse_rels(z, rels_path)

        shapes = []
        for sp in slide_root.iter(f'{{{P_NS}}}sp'):
            paras = get_texts_by_para(sp)
            bbox = shape_bbox(sp)
            name = None
            for el in sp.iter():
                if local(el.tag) == 'cNvPr':
                    name = el.attrib.get('name')
                    break
            if paras:
                shapes.append({'name': name, 'bbox': bbox, 'paras': paras, 'kind': 'sp'})

        tables = []
        for gf in slide_root.iter(f'{{{P_NS}}}graphicFrame'):
            bbox = shape_bbox(gf)
            name = None
            for el in gf.iter():
                if local(el.tag) == 'cNvPr':
                    name = el.attrib.get('name')
                    break
            for tbl in gf.iter(f'{{{A_NS}}}tbl'):
                rows = extract_table(tbl)
                tables.append({'bbox': bbox, 'name': name, 'rows': rows})

        grouped = grouped_hyperlinks(slide_root, rels)
        shape_links = shape_hyperlinks(slide_root, rels)

        any_hlinks = []
        for el in slide_root.iter():
            if local(el.tag) == 'hlinkClick':
                rid = el.attrib.get(f'{{{R_NS}}}id')
                tip = el.attrib.get('tooltip')
                action = el.attrib.get('action')
                target = rels.get(rid, {}).get('target') if rid else None
                any_hlinks.append({'rid': rid, 'url': target, 'tooltip': tip, 'action': action})

        # External hyperlink rels even if not linked from text
        ext_rels = []
        for rid, info in rels.items():
            if info['type'] == 'hyperlink' or info.get('mode') == 'External':
                if 'hyperlink' in info.get('full_type', '') or info['type'] == 'hyperlink':
                    ext_rels.append({'rid': rid, 'url': info['target'], 'mode': info['mode']})

        notes_text = []
        for rid, info in rels.items():
            if info['type'] == 'notesSlide':
                npath = 'ppt/notesSlides/' + os.path.basename(info['target'])
                if npath not in z.namelist() and info['target'].startswith('../'):
                    npath = 'ppt/' + info['target'].replace('../', '')
                if npath in z.namelist():
                    nroot = ET.fromstring(z.read(npath))
                    notes_text = get_texts_by_para(nroot)

        # Comment relationships
        comment_refs = []
        for rid, info in rels.items():
            if 'comment' in info['type'].lower() or 'comment' in info['target'].lower():
                comment_refs.append({'rid': rid, 'target': info['target'], 'type': info['type']})

        def sort_key(s):
            b = s['bbox'] or (0, 0, 0, 0)
            return (b[1], b[0])

        shapes_sorted = sorted(shapes, key=sort_key)

        # Flat text dump
        flat = []
        for sh in shapes_sorted:
            flat.extend(sh['paras'])
        for tbl in tables:
            for row in tbl['rows']:
                for cell in row:
                    if cell.strip():
                        flat.append(cell)

        slide_info = {
            'slide': i,
            'path': slide_path,
            'shapes': shapes_sorted,
            'tables': tables,
            'grouped_links': grouped,
            'shape_links': shape_links,
            'any_hlinks': any_hlinks,
            'ext_rels': ext_rels,
            'all_rels': rels,
            'notes': notes_text,
            'comment_refs': comment_refs,
            'flat_text': flat,
        }
        results.append(slide_info)

        out_lines.append('=' * 80)
        out_lines.append(f"SLIDE {i} ({slide_path})")
        out_lines.append('=' * 80)
        out_lines.append('--- SHAPES (y,x sorted) ---')
        for sh in shapes_sorted:
            b = sh['bbox']
            pos = f"x={b[0]},y={b[1]},cx={b[2]},cy={b[3]}" if b else 'no-bbox'
            out_lines.append(f"[{sh['name']}] ({pos})")
            for p in sh['paras']:
                out_lines.append(f"  | {p}")
        out_lines.append('--- TABLES ---')
        for ti, tbl in enumerate(tables):
            out_lines.append(f"TABLE {ti + 1} name={tbl.get('name')} bbox={tbl['bbox']}")
            for ri, row in enumerate(tbl['rows']):
                out_lines.append(f"  ROW {ri}:")
                for ci, cell in enumerate(row):
                    cell_repr = cell.replace('\n', ' ¶ ')
                    out_lines.append(f"    C{ci}: {cell_repr}")
        out_lines.append('--- GROUPED HYPERLINKS ---')
        for L in grouped:
            out_lines.append(
                f"  text={L['text']!r} url={L['url']!r} rid={L['rid']} tip={L.get('tooltip')!r} action={L.get('action')!r}"
            )
        out_lines.append('--- SHAPE HYPERLINKS ---')
        for L in shape_links:
            out_lines.append(
                f"  text={L['text']!r} url={L['url']!r} rid={L['rid']} name={L.get('name')!r} tip={L.get('tooltip')!r}"
            )
        out_lines.append('--- ANY hlinkClick ---')
        for L in any_hlinks:
            out_lines.append(
                f"  rid={L['rid']} url={L['url']!r} tip={L.get('tooltip')!r} action={L.get('action')!r}"
            )
        out_lines.append('--- EXT HYPERLINK RELS ---')
        for L in ext_rels:
            out_lines.append(f"  rid={L['rid']} url={L['url']!r} mode={L['mode']}")
        out_lines.append('--- ALL RELS ---')
        for rid, info in rels.items():
            out_lines.append(
                f"  {rid}: type={info['type']} mode={info['mode']} target={info['target']}"
            )
        if comment_refs:
            out_lines.append('--- COMMENT REFS ---')
            for c in comment_refs:
                out_lines.append(f"  {c}")
        if notes_text:
            out_lines.append('--- NOTES ---')
            for p in notes_text:
                out_lines.append(f"  | {p}")
        out_lines.append('--- FLAT TEXT ---')
        out_lines.append('\n'.join(flat))

    comments = extract_comments(z)

    # Also scan ALL files in pptx for http URLs (catch missing)
    all_urls_in_pkg = []
    for name in z.namelist():
        if name.endswith(('.xml', '.rels')):
            data = z.read(name).decode('utf-8', errors='replace')
            for m in re.finditer(r'Target="(https?://[^"]+|mailto:[^"]+)"', data):
                all_urls_in_pkg.append((name, m.group(1)))
            for m in re.finditer(r'(https?://[^\s<>"\']+)', data):
                # skip xmlns
                u = m.group(1)
                if 'schemas.openxmlformats' in u or 'schemas.microsoft' in u or 'purl.org' in u:
                    continue
                if 'w3.org' in u:
                    continue
                all_urls_in_pkg.append((name, u.rstrip(').,;]')))

    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({'slides': results, 'comments': comments, 'pkg_urls': all_urls_in_pkg}, f, ensure_ascii=False, indent=2)
    with open(OUT_TXT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))
        f.write('\n\n' + '=' * 80 + '\nCOMMENTS\n' + '=' * 80 + '\n')
        for c in comments:
            f.write(f"\n--- {c['file']} ---\n")
            for p in c['paras']:
                f.write(f"  | {p}\n")
            for u in c['urls']:
                f.write(f"  URL: {u}\n")
            f.write(f"  PREVIEW:\n{c['raw_preview']}\n")
        f.write('\n\n' + '=' * 80 + '\nALL PKG URL HITS\n' + '=' * 80 + '\n')
        seen = set()
        for name, u in all_urls_in_pkg:
            key = (name, u)
            if key in seen:
                continue
            seen.add(key)
            f.write(f"{name}: {u}\n")

    urls = []
    for s in results:
        for L in s['grouped_links']:
            urls.append((s['slide'], L['text'], L['url'], 'text'))
        for L in s['shape_links']:
            urls.append((s['slide'], L['text'], L['url'], 'shape'))
    print(f'Slides: {len(results)}')
    print(f'Hyperlink instances: {len(urls)}')
    print(f'Comments: {len(comments)}')
    print('Unique linked URLs:')
    seen = set()
    for slide, text, url, kind in urls:
        key = (url, text)
        if key not in seen:
            seen.add(key)
            print(f'  [{kind}] slide{slide}: {text!r}')
            print(f'         {url}')
    print(f'\nWrote {OUT_TXT}')
    print(f'Wrote {OUT_JSON}')


if __name__ == '__main__':
    main()
