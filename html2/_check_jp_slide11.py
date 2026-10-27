# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
pptx = next((ROOT / "5개국 도식화(최종)_261023" / "5개국 도식화(최종)_261023" / "일본").glob("*.pptx"))
td = Path(tempfile.mkdtemp())
with zipfile.ZipFile(pptx) as z:
    z.extractall(td)
xml = (td / "ppt" / "slides" / "slide11.xml").read_text(encoding="utf-8")
texts = re.findall(r"<a:t[^>]*>([^<]*)</a:t>", xml)
joined = "".join(texts)
out = ROOT / "_jp_slide11_text.txt"
out.write_text(joined, encoding="utf-8")
print("wrote", out, "len", len(joined))
print("제16" in joined, "제30" in joined, "J16" in joined, "J30" in joined)
# near each hlink
rels_xml = (td / "ppt" / "slides" / "_rels" / "slide11.xml.rels").read_text(encoding="utf-8")
for rid, url in re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels_xml):
    if "law.go.kr" not in url:
        continue
    # find runs with this rid and surrounding paragraph texts
    paras = re.findall(r"<a:p[\s>][\s\S]*?</a:p>", xml)
    for para in paras:
        if f'r:id="{rid}"' in para:
            pt = "".join(re.findall(r"<a:t[^>]*>([^<]*)</a:t>", para))
            print(rid, url[-20:], "PARA:", pt[:200])
shutil.rmtree(td, ignore_errors=True)
