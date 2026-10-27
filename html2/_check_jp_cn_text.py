# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "5개국 도식화(최종)_261023" / "5개국 도식화(최종)_261023"


def slide_text(pptx: Path, n: int) -> str:
    td = Path(tempfile.mkdtemp())
    try:
        with zipfile.ZipFile(pptx) as z:
            z.extractall(td)
        xml = (td / "ppt" / "slides" / f"slide{n}.xml").read_text(encoding="utf-8")
        return "".join(re.findall(r"<a:t[^>]*>([^<]*)</a:t>", xml))
    finally:
        shutil.rmtree(td, ignore_errors=True)


jp = next((BASE / "일본").glob("*.pptx"))
cn = next((BASE / "중국").glob("*.pptx"))

print("=== JP slide3 has 첨부/계약 ===")
t = slide_text(jp, 3)
print("수출대행" in t, "계약서" in t)
print(t[t.find("계약서") : t.find("계약서") + 200] if "계약서" in t else t[:400])

print("\n=== JP slide11 law fragments context ===")
t = slide_text(jp, 11)
for key in ["제16", "제30", "화장품법", "판매"]:
    i = t.find(key)
    print(key, "->", t[i : i + 80] if i >= 0 else "ABSENT")

print("\n=== JP slide14/15 labels ===")
for n in (14, 15):
    t = slide_text(jp, n)
    print(f"S{n}", "라벨" in t, "필수 표시" in t, "의약부외품" in t)
    if "필수" in t:
        print(t[t.find("필수") - 20 : t.find("필수") + 100])

print("\n=== CN slide4 romarin/wipo ===")
t = slide_text(cn, 4)
print("romarin" in t.lower(), "wipo" in t.lower())
# show around madrid
for key in ["romarin", "마드리드", "기초출원", "WIPO", "wipo"]:
    i = t.lower().find(key.lower()) if key != "마드리드" else t.find(key)
    if i < 0:
        i = t.find(key)
    print(key, "->", repr(t[max(0, i - 30) : i + 80]) if i >= 0 else "ABSENT")

print("\n=== CN customs slides UNI-PASS ===")
for n in range(1, 16):
    t = slide_text(cn, n)
    if "UNI-PASS" in t or "unipass" in t.lower() or "유니패스" in t:
        print("found on slide", n)
        i = t.find("UNI")
        print(repr(t[max(0, i - 40) : i + 80]))

# check image paths
print("\n=== JP image paths ===")
for p in [
    ROOT / "files/japan/jp-5-1-cosmetic-label.png",
    ROOT / "files/japan/jp-5-2-quasi-label.png",
    ROOT / "images/law/jp-5-1-cosmetic-label.png",
    ROOT / "images/law/jp-5-2-quasi-label.png",
    ROOT / "files/japan/jp-1-1-agency-contract.zip",
]:
    print(p.exists(), p)
