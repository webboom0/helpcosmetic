# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent


def strip(u: str) -> str:
    u = u.replace("&amp;", "&")
    p = urlsplit(u)
    if p.scheme == "mailto":
        return u
    q = [
        (k, v)
        for k, v in parse_qsl(p.query, keep_blank_values=True)
        if not k.lower().startswith("utm_") and k not in {"_csrf", "DSCTOKEN", "searchopt", "searchkey"}
    ]
    return urlunsplit((p.scheme, p.netloc, unquote(p.path), urlencode(q), p.fragment))


def html_set(prefix: str, folder: str) -> tuple[set[str], set[str]]:
    urls: set[str] = set()
    dls: set[str] = set()
    for p in ROOT.glob(f"law-export-{prefix}*.html"):
        html = p.read_text(encoding="utf-8")
        m = re.search(r'<div class="sub-doc law-export">([\s\S]*?)</div>\s*</div>\s*</main>', html)
        block = m.group(1) if m else html
        for h in re.findall(r'href="([^"]+)"', block):
            h = h.replace("&amp;", "&")
            if h.startswith(f"files/{folder}/"):
                dls.add(h)
            elif h.startswith("http") or h.startswith("mailto:"):
                urls.add(strip(h))
    return urls, dls


def ppt_urls(extract: str, skip_drive: bool = True, skip_kcia_pdf: bool = False) -> set[str]:
    out: set[str] = set()
    for line in (ROOT / extract).read_text(encoding="utf-8").splitlines():
        if not (line.startswith("  http") or line.startswith("  mailto")):
            continue
        u = line.strip()
        if skip_drive and "drive.google.com" in u:
            continue
        if skip_kcia_pdf and "kcia.or.kr/home/law/" in u and u.lower().endswith(".pdf"):
            continue
        out.add(strip(u))
    return out


jp_ppt = ppt_urls("_ppt_jp_extract.txt")
# broken fragment fixed in HTML
jp_ppt.discard(
    strip(
        "https://www.law.go.kr/lsSc.do?section=&menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060101&query=%ED%99%94%EC%9E%A5%ED%92%88%EB%B2%95#undefined"
    )
)
jp_ppt.add(
    strip(
        "https://www.law.go.kr/lsSc.do?section=&menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060101&query=%ED%99%94%EC%9E%A5%ED%92%88%EB%B2%95#J16:0"
    )
)
jp_u, jp_d = html_set("jp", "japan")
print("JP missing URLs:", sorted(jp_ppt - jp_u))
print("JP extra URLs:", sorted(jp_u - jp_ppt))
for need in [
    "files/japan/jp-1-1-agency-contract.zip",
    "files/japan/jp-5-1-cosmetic-label.png",
    "files/japan/jp-5-2-quasi-label.png",
]:
    print(f"JP has {need}:", need in jp_d)

cn_ppt = ppt_urls("_ppt_cn_extract.txt", skip_kcia_pdf=True)
cn_u, cn_d = html_set("cn", "china")
print("CN missing URLs:", sorted(cn_ppt - cn_u))
print("CN extra URLs:", sorted(cn_u - cn_ppt))
print("CN has att1/att3:", "files/china/cn-att1-annex14.hwp" in cn_d, "files/china/cn-att3-ingredient-guide.hwp" in cn_d)
print("CN no romarin/unipass:", not any("romarin" in u for u in cn_u), not any("unipass" in u for u in cn_u))
