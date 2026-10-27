# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit, urlunsplit, urlencode, unquote

ROOT = Path(__file__).resolve().parent

# From PPT (_ppt_us_map.txt) — external + mailto + drive/docs
PPT_URLS = [
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863913",
    "https://webaccess.wipo.int/mgs/?lang=kr",
    "https://www.uspto.gov/trademarks/laws/specimen-refusal-and-how-overcome-refusal?",
    "https://www.uspto.gov/trademarks/basics/drawings-and-specimens?",
    "https://www.uspto.gov/trademarks/apply?",
    "https://www.fda.gov/cosmetics/cosmetics-news-events/fda-issues-final-guidance-registration-and-listing-cosmetic-product-facilities-and-products?",
    "https://www.fda.gov/cosmetics/registration-listing-cosmetic-product-facilities-and-products?",
    "https://www.fda.gov/cosmetics/registration-listing-cosmetic-product-facilities-and-products/form-fda-5067-cosmetic-product-listing?",
    "mailto:RLC-PaperSubmissions@fda.hhs.gov",
    "https://helpcosmetic.or.kr/pc/license/license02.php?code=foreign&idx=5735&page=17&ptype=view",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863877",
    "https://kcia.or.kr/cert/main/",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1720212",
    "https://kcia.or.kr/cert/main/?utm_source=chatgpt.com",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1720224&ContentsID=KI_cmmrcFormat_1720224&query=%EC%88%98%EC%B6%9C%EC%8B%A0%EA%B3%A0%EC%84%9C",
    "https://unipass.customs.go.kr/clip/index.do",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1719028&ContentsID=KI_cmmrcFormat_1719028&query=%ED%95%AD%EA%B3%B5%ED%99%94%EB%AC%BC%EC%9A%B4%EC%86%A1%EC%9E%A5",
    "https://kcia.or.kr/home/law/%EA%B8%B0%ED%83%80%20%EC%88%98%EC%B6%9C%ED%86%B5%EA%B4%80%EC%97%90%20%ED%95%84%EC%9A%94%ED%95%9C%20%EC%84%9C%EB%A5%98.pdf",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1719002&ContentsID=KI_cmmrcFormat_1719002&query=%EC%84%A0%ED%95%98%EC%A6%9D%EA%B6%8C",
]

# Drive/Docs in PPT → must become local lex-dl (or remain as link if not localized)
PPT_DRIVE = {
    "https://drive.google.com/file/d/1FVVIiIQFvBJ_HHMnbGXJP4PtRB01l7At/view?usp=drive_link": "MM2 (slide4) → us-1-3/1-4",
    "https://drive.google.com/file/d/1c5j6lX6eE0-h1X_JTk49R2l5frt3IrA7/view?usp=drive_link": "FDA Direct (slide7) → us-2-1",
    "https://drive.google.com/file/d/1d9ReG0jCgj3U_vDVSNs-cFNnFc_PJryu/view?usp=drive_link": "5066 (slide8) → us-3-1",
    "https://drive.google.com/file/d/1VjqmtjNOSoJVKksrceRHDOc0zc3_dkK8/view?usp=drive_link": "5067 (slide10) → us-3-2",
    "https://drive.google.com/file/d/1Pflv1cuBiXUmLbbz17OvSntnEyxyTmCJ/view?usp=drive_link": "packing (slide12) → us-4-1",
    "https://docs.google.com/document/d/1Aqnjtkio3aGGJG_ZAcq19FwoYq1whC1Y/edit?usp=drive_link&ouid=116757525496572029278&rtpof=true&sd=true": "packing docs (slide14) → us-4-1 reuse?",
    "https://drive.google.com/file/d/1TZ-xY1Svvr0soNyZs8mkz7uk_6JUn5Ca/view?usp=drive_link": "CBP 301 (slide14) → us-5-1",
}

# Local files that SHOULD appear as downloads (per PPT Drive mapping + confirmed policy)
PPT_ATTACH_EXPECTED = {
    "files/usa/us-1-1-export-agency-ko.pdf",  # with KITA link for 수출대행계약서
    "files/usa/us-1-2-export-agency-en.pdf",
    "files/usa/us-1-3-mm2-ko.pdf",
    "files/usa/us-1-4-mm2-en.pdf",
    "files/usa/us-2-1-fda-direct-guide.pdf",
    "files/usa/us-3-1-fda-5066.pdf",
    "files/usa/us-3-2-fda-5067.pdf",
    "files/usa/us-4-1-packing-list.pdf",  # slide12 + slide14
    "files/usa/us-5-1-cbp-301.pdf",
}

# Explicitly NOT to link (prior decisions / not in PPT body as download)
PPT_ATTACH_FORBIDDEN = {
    "files/usa/us-3-3-cfr-701-3.pdf",  # CFR is helpcosmetic lex-link only
    "files/usa/us-5-2-signature-register.pdf",  # PPT에 없음
}


def strip_utm(u: str) -> str:
    u = u.replace("&amp;", "&")
    parts = urlsplit(u)
    if parts.scheme == "mailto":
        return u.lower()
    q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q), parts.fragment))


def norm_key(u: str) -> str:
    u = strip_utm(u)
    # decode path for kcia pdf
    parts = urlsplit(u)
    path = unquote(parts.path)
    return urlunsplit((parts.scheme, parts.netloc.lower(), path, parts.query, parts.fragment))


def main() -> None:
    pages = sorted(ROOT.glob("law-export-us*.html"))
    by_page = {p.name: p.read_text(encoding="utf-8") for p in pages}

    ppt_set = {norm_key(u) for u in PPT_URLS}
    # allow both with/without utm for kcia cert
    ppt_set.add(norm_key("https://kcia.or.kr/cert/main/"))

    content_urls: set[str] = set()
    content_dls: set[str] = set()
    content_drive: set[str] = set()
    per: dict[str, tuple[set[str], set[str]]] = {}

    for name, html in by_page.items():
        m = re.search(r'<div class="sub-doc law-export">([\s\S]*?)</div>\s*</div>\s*</main>', html)
        block = m.group(1) if m else html
        raw_hrefs = re.findall(r'href="([^"]+)"', block)
        urls = set()
        dls = set()
        for h in raw_hrefs:
            h = h.replace("&amp;", "&")
            if h.startswith("files/usa/"):
                dls.add(h)
            elif h.startswith("http") or h.startswith("mailto:"):
                if "drive.google.com" in h or "docs.google.com" in h:
                    content_drive.add(norm_key(h))
                urls.add(norm_key(h))
        content_urls |= urls
        content_dls |= dls
        per[name] = (urls, dls)

    missing_urls = sorted(u for u in ppt_set if u not in content_urls)
    # drive URLs intentionally replaced by local files — not expected in HTML
    extra_urls = sorted(
        u
        for u in content_urls
        if u not in ppt_set
        and "drive.google.com" not in u
        and "docs.google.com" not in u
    )

    missing_dl = sorted(PPT_ATTACH_EXPECTED - content_dls)
    extra_dl = sorted(content_dls - PPT_ATTACH_EXPECTED)
    forbidden_present = sorted(content_dls & PPT_ATTACH_FORBIDDEN)

    lines = ["# US PPT vs HTML link/download audit", ""]
    lines.append(f"Pages: {', '.join(by_page)}")
    lines.append(f"HTML content URLs: {len(content_urls)}")
    lines.append(f"HTML downloads: {len(content_dls)}")
    lines.append("")
    lines.append("## Missing external/mailto URLs (vs PPT; Drive excluded)")
    lines += [f"- {u}" for u in missing_urls] or ["- (none)"]
    lines.append("")
    lines.append("## Extra external URLs")
    if extra_urls:
        for u in extra_urls:
            hits = [n for n, (uu, _) in per.items() if u in uu]
            lines.append(f"- {u}")
            lines.append(f"  pages: {', '.join(hits)}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Drive/Docs still in HTML (should be local DL)")
    lines += [f"- {u}" for u in sorted(content_drive)] or ["- (none)"]
    lines.append("")
    lines.append("## Missing expected downloads")
    lines += [f"- {d}" for d in missing_dl] or ["- (none)"]
    lines.append("")
    lines.append("## Extra downloads (not in expected PPT set)")
    lines += [f"- {d}" for d in extra_dl] or ["- (none)"]
    lines.append("")
    lines.append("## Forbidden downloads still linked")
    lines += [f"- {d}" for d in forbidden_present] or ["- (none)"]
    lines.append("")
    lines.append("## Per-page")
    for name, (urls, dls) in per.items():
        lines.append(f"### {name}")
        for u in sorted(urls):
            tag = "PPT" if u in ppt_set else "EXTRA"
            lines.append(f"  [{tag}] URL {u}")
        for d in sorted(dls):
            if d in PPT_ATTACH_FORBIDDEN:
                tag = "FORBIDDEN"
            elif d in PPT_ATTACH_EXPECTED:
                tag = "PPT"
            else:
                tag = "EXTRA"
            lines.append(f"  [{tag}] DL  {d}")
        lines.append("")

    disk = {p.name for p in (ROOT / "files" / "usa").iterdir() if p.is_file()}
    expected_names = {Path(x).name for x in PPT_ATTACH_EXPECTED}
    forbidden_names = {Path(x).name for x in PPT_ATTACH_FORBIDDEN}
    lines.append("## Disk")
    lines.append(f"all: {sorted(disk)}")
    lines.append(f"disk only (not expected/forbidden inventory): {sorted(disk - expected_names - forbidden_names)}")
    lines.append(f"expected missing on disk: {sorted(expected_names - disk)}")
    lines.append(f"forbidden still on disk (OK if unlinked): {sorted(disk & forbidden_names)}")

    # step placement quick check notes
    lines.append("")
    lines.append("## Placement notes (expected)")
    lines.append("- us-01: KITA 수출대행 + agency ko/en + USPTO/WIPO + MM2 ko/en")
    lines.append("- us-02: FDA Direct guide DL")
    lines.append("- us-03: 5066/5067 DL + MoCRA FDA links + mailto + helpcosmetic CFR only")
    lines.append("- us-04: KITA shipping docs + UNI-PASS + KCIA CFS + packing DL + other customs PDF URL")
    lines.append("- us-05: shipping KITA links + packing DL + CBP301 DL (no signature register)")

    out = ROOT / "_us_link_audit.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
