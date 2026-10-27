# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit, unquote

ROOT = Path(__file__).resolve().parent


def strip_utm(u: str) -> str:
    u = u.replace("&amp;", "&")
    parts = urlsplit(u)
    if parts.scheme == "mailto":
        return u
    q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.lower().startswith("utm_")]
    # drop ephemeral csrf-like noise for comparison optionally later
    return urlunsplit((parts.scheme, parts.netloc, unquote(parts.path), urlencode(q), parts.fragment))


def audit(prefix: str, folder: str) -> None:
    pages = sorted(ROOT.glob(f"law-export-{prefix}*.html"))
    lines = [f"# {prefix.upper()} HTML inventory", ""]
    all_urls: set[str] = set()
    all_dls: set[str] = set()
    for p in pages:
        html = p.read_text(encoding="utf-8")
        m = re.search(r'<div class="sub-doc law-export">([\s\S]*?)</div>\s*</div>\s*</main>', html)
        block = m.group(1) if m else html
        hrefs = re.findall(r'href="([^"]+)"', block)
        urls = []
        dls = []
        for h in hrefs:
            h = h.replace("&amp;", "&")
            if h.startswith(f"files/{folder}/"):
                dls.append(h)
                all_dls.add(h)
            elif h.startswith("http") or h.startswith("mailto:"):
                u = strip_utm(h)
                urls.append(u)
                all_urls.add(u)
            elif h.startswith("#"):
                pass
        lines.append(f"## {p.name}")
        for u in urls:
            lines.append(f"  URL {u}")
        for d in dls:
            lines.append(f"  DL  {d}")
        lines.append("")
    lines.append("## UNIQUE URLS")
    for u in sorted(all_urls):
        lines.append(f"- {u}")
    lines.append("")
    lines.append("## UNIQUE DLS")
    for d in sorted(all_dls):
        lines.append(f"- {d}")
    disk = sorted(x.name for x in (ROOT / "files" / folder).iterdir() if x.is_file())
    lines.append("")
    lines.append("## DISK FILES")
    for n in disk:
        lines.append(f"- {n}")
    out = ROOT / f"_{prefix}_html_inventory.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)


audit("jp", "japan")
audit("cn", "china")
