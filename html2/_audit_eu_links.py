# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parent

PPT_URLS_RAW = [
    "https://www.kyungnam.ac.kr/bbs/kuit/314/46382/artclView.do",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863913",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863914",
    "https://unipass.customs.go.kr/csp/index.do?utm_source=chatgpt.com",
    "https://euipo.europa.eu/ec2/",
    "https://www.tmdn.org/tmview/#/tmview",
    "https://euipo.europa.eu/eSearch/",
    "https://www.wipo.int/en/web/madrid-system",
    "https://tmdn.org/#/members",
    "https://www.boip.int/nl",
    "https://www.boip.int/en/entrepreneurs/trademarks/register-a-benelux-trademark#step-3",
    "https://webgate.ec.europa.eu/cpnp/",
    "https://trade.ec.europa.eu/access-to-markets/en/content/customs-clearance-documents-and-procedures-0",
    "https://trade.ec.europa.eu/access-to-markets/en/home",
]

PPT_ATTACH = [
    "eu-1-1-export-contract-example.hwp",
    "eu-1-2-export-agency-ko.pdf",
    "eu-1-2-export-agency-en.pdf",
    "eu-1-3-export-declaration.pdf",
    "eu-2-cpnp-guide.pdf",
    "eu-3-1-bl.pdf",
    "eu-3-2-awb.pdf",
    "eu-3-3-commercial-invoice.pdf",
    "eu-3-3-proforma-invoice.pdf",
    "eu-3-4-packing-list.pdf",
    "eu-3-5-customs-docs.pdf",
]


def strip_utm(u: str) -> str:
    u = u.replace("&amp;", "&")
    parts = urlsplit(u)
    q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(q), parts.fragment))


def norm_key(u: str) -> str:
    """Compare ignoring utm and trailing slash differences on path-only."""
    u = strip_utm(u)
    if u.endswith("/") and u.count("/") > 3 and "?" not in u and "#" not in u:
        # keep as-is for directories like ec2/
        pass
    return u


def main() -> None:
    pages = sorted(ROOT.glob("law-export-eu*.html"))
    by_page = {p.name: p.read_text(encoding="utf-8") for p in pages}

    ppt_set = {norm_key(u) for u in PPT_URLS_RAW}
    # also allow stripped UNI-PASS without utm as matching PPT intent
    ppt_set.add(norm_key("https://unipass.customs.go.kr/csp/index.do"))

    ppt_files = {f"files/eu/{n}" for n in PPT_ATTACH}

    content_urls: set[str] = set()
    content_dls: set[str] = set()
    per: dict[str, tuple[set[str], set[str]]] = {}

    for name, html in by_page.items():
        m = re.search(r'<div class="sub-doc law-export">([\s\S]*?)</div>\s*</div>\s*</main>', html)
        block = m.group(1) if m else html
        urls = {norm_key(u) for u in re.findall(r'href="(https?://[^"]+)"', block)}
        # exclude mailto
        urls = {u for u in urls if not u.startswith("mailto:")}
        dls = set(re.findall(r'href="(files/eu/[^"]+)"', block))
        content_urls |= urls
        content_dls |= dls
        per[name] = (urls, dls)

    missing_urls = sorted(ppt_set - content_urls - {norm_key("https://unipass.customs.go.kr/csp/index.do?utm_source=chatgpt.com")})
    # if stripped unipass present, don't count utm version as missing
    if norm_key("https://unipass.customs.go.kr/csp/index.do") in content_urls:
        missing_urls = [u for u in missing_urls if "unipass.customs.go.kr/csp/index.do" not in u]

    extra_urls = sorted(content_urls - ppt_set)
    missing_dl = sorted(ppt_files - content_dls)
    extra_dl = sorted(content_dls - ppt_files)

    lines = ["# EU PPT vs HTML link/download audit", ""]
    lines.append(f"Pages: {', '.join(by_page)}")
    lines.append(f"PPT unique URLs (raw 14 + stripped UNI-PASS): compare set size {len(ppt_set)}")
    lines.append(f"HTML content URLs: {len(content_urls)}")
    lines.append(f"PPT attachments: {len(ppt_files)}")
    lines.append(f"HTML downloads: {len(content_dls)}")
    lines.append("")
    lines.append("## Missing external URLs")
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
    lines.append("## Missing downloads")
    lines += [f"- {d}" for d in missing_dl] or ["- (none)"]
    lines.append("")
    lines.append("## Extra downloads")
    lines += [f"- {d}" for d in extra_dl] or ["- (none)"]
    lines.append("")
    lines.append("## Per-page")
    for name, (urls, dls) in per.items():
        lines.append(f"### {name}")
        for u in sorted(urls):
            tag = "PPT" if u in ppt_set else "EXTRA"
            lines.append(f"  [{tag}] URL {u}")
        for d in sorted(dls):
            tag = "PPT" if d in ppt_files else "EXTRA"
            lines.append(f"  [{tag}] DL  {d}")
        lines.append("")

    disk = {p.name for p in (ROOT / "files" / "eu").iterdir() if p.is_file()}
    lines.append("## Disk files (top-level only)")
    lines.append(f"disk: {sorted(disk)}")
    lines.append(f"disk only vs inventory: {sorted(disk - set(PPT_ATTACH))}")
    lines.append(f"inventory missing on disk: {sorted(set(PPT_ATTACH) - disk)}")

    out = ROOT / "_eu_link_audit.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
