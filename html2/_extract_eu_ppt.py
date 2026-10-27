# -*- coding: utf-8 -*-
"""Extract all visible text + hyperlinks from EU cosmetics export PPTX."""
import zipfile
import os
import json
from xml.etree import ElementTree as ET

PPTX = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\5개국 도식화(최종)_261023\5개국 도식화(최종)_261023\EU\EU 화장품 수출 절차 도식화_5차 보완_261012_수정.pptx'
OUT_JSON = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_raw.json'
OUT_TXT = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_raw.txt'

A_NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'


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
        else:
            # empty para may still matter for spacing; skip
            pass
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
        rels[rid] = {'target': target, 'type': rtype.split('/')[-1], 'mode': mode}
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
        rels_path = slide_path.replace('ppt/slides/', 'ppt/slides/_rels/') + '.rels'
        # also handle slides/slideN.xml -> slides/_rels/slideN.xml.rels
        if not rels_path.endswith('.rels'):
            rels_path = rels_path + '.rels'
        # Fix: slide_path is ppt/slides/slide1.xml
        # rels should be ppt/slides/_rels/slide1.xml.rels
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

        # Also catch hlinkClick anywhere (defensive)
        any_hlinks = []
        for el in slide_root.iter(f'{{{A_NS}}}hlinkClick'):
            rid = el.attrib.get(f'{{{R_NS}}}id')
            tip = el.attrib.get('tooltip')
            action = el.attrib.get('action')
            target = rels.get(rid, {}).get('target') if rid else None
            any_hlinks.append({'rid': rid, 'url': target, 'tooltip': tip, 'action': action})

        notes_text = []
        for rid, info in rels.items():
            if info['type'] == 'notesSlide':
                npath = 'ppt/notesSlides/' + os.path.basename(info['target'])
                if npath in z.namelist():
                    nroot = ET.fromstring(z.read(npath))
                    notes_text = get_texts_by_para(nroot)

        def sort_key(s):
            b = s['bbox'] or (0, 0, 0, 0)
            return (b[1], b[0])

        shapes_sorted = sorted(shapes, key=sort_key)

        slide_info = {
            'slide': i,
            'path': slide_path,
            'shapes': shapes_sorted,
            'tables': tables,
            'grouped_links': grouped,
            'shape_links': shape_links,
            'any_hlinks': any_hlinks,
            'all_rels': rels,
            'notes': notes_text,
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
        out_lines.append('--- ALL RELS ---')
        for rid, info in rels.items():
            out_lines.append(
                f"  {rid}: type={info['type']} mode={info['mode']} target={info['target']}"
            )
        if notes_text:
            out_lines.append('--- NOTES ---')
            for p in notes_text:
                out_lines.append(f"  | {p}")

    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(OUT_TXT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))

    # Summary of unique URLs
    urls = []
    for s in results:
        for L in s['grouped_links']:
            urls.append((s['slide'], L['text'], L['url'], 'text'))
        for L in s['shape_links']:
            urls.append((s['slide'], L['text'], L['url'], 'shape'))
    print(f'Slides: {len(results)}')
    print(f'Hyperlink instances: {len(urls)}')
    print('Unique URLs:')
    seen = set()
    for slide, text, url, kind in urls:
        if url not in seen:
            seen.add(url)
            print(f'  [{kind}] slide{slide}: {text!r}')
            print(f'         {url}')
    print(f'\nWrote {OUT_TXT}')
    print(f'Wrote {OUT_JSON}')


if __name__ == '__main__':
    main()
