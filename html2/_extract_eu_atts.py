# -*- coding: utf-8 -*-
import zipfile
import os

base = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\5개국 도식화(최종)_261023\5개국 도식화(최종)_261023\EU\첨부자료'
out = []
for root, dirs, files in os.walk(base):
    for f in sorted(files):
        fp = os.path.join(root, f)
        out.append(f'{os.path.getsize(fp):10d}  {f}')
        if f.lower().endswith('.zip'):
            z = zipfile.ZipFile(fp)
            for info in z.infolist():
                # decode zip name carefully
                name = info.filename
                try:
                    name2 = name.encode('cp437').decode('euc-kr')
                except Exception:
                    try:
                        name2 = name.encode('cp437').decode('utf-8')
                    except Exception:
                        name2 = name
                out.append(f'           -> {name2}  (raw={name!r})')

audit = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_links_audit.txt'
with open(audit, encoding='utf-8') as f:
    out.append('\n\n===== LINKS AUDIT =====\n')
    out.append(f.read())

path = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_atts.txt'
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('wrote', path)
