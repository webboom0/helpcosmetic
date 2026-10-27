# -*- coding: utf-8 -*-
"""Shared shell helpers for Taiwan export pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICO = '<i class="ri-asterisk law-hint-ico" aria-hidden="true"></i>'


def lex(url: str, text: str) -> str:
    return (
        f'<a class="lex-link" href="{url}" target="_blank" rel="noopener noreferrer">'
        f'{text}<i class="ri-external-link-line" aria-hidden="true"></i></a>'
    )


def dl(href: str, name: str, ext: str = "PDF") -> str:
    icos = {
        "PDF": "ri-file-pdf-2-fill",
        "HWP": "ri-file-text-fill",
        "XLS": "ri-file-excel-2-fill",
        "XLSX": "ri-file-excel-2-fill",
        "DOCX": "ri-file-word-2-fill",
        "DOC": "ri-file-word-2-fill",
    }
    ico = icos.get(ext.upper(), "ri-file-text-fill")
    # remote download endpoints (e.g. KCIA) should not force HTML download attr
    is_remote = href.startswith(("http://", "https://"))
    extra = ' target="_blank" rel="noopener noreferrer"' if is_remote else " download"
    return (
        f'<a class="lex-dl" href="{href}"{extra} data-ext="{ext}">'
        f'<i class="{ico}" aria-hidden="true"></i>'
        f'<span class="lex-dl__name">{name}</span>'
        f'<span class="lex-dl__tag"><i class="ri-download-2-line" aria-hidden="true"></i> {ext}</span></a>'
    )


COUNTRY_TABS = """          <nav class="law-country-tabs" aria-label="국가 선택">
            <a href="law-export.html"><img src="images/flags_bbs2/China.svg" alt="">중국</a>
            <a href="law-export-jp.html"><img src="images/flags_bbs2/Japan.svg" alt="">일본</a>
            <a href="law-export-us.html"><img src="images/flags_bbs2/USA.svg" alt="">미국</a>
            <a href="law-export-eu.html"><img src="images/flags_bbs2/EU.svg" alt="">EU</a>
            <a href="law-export-tw.html" class="is-active" aria-current="page"><img src="images/flags_bbs2/Taiwan.svg" alt="">대만</a>
          </nav>"""

STEP_NAV = """          <nav class="law-step-nav" aria-label="수출절차 단계">
            <a href="law-export-tw.html"{a0}>전체 절차</a>
            <a href="law-export-tw-01.html"{a1}>수출 계약 및 상표등록</a>
            <a href="law-export-tw-02.html"{a2}>대만 내 수입업자 선임 및 PIF 준비</a>
            <a href="law-export-tw-03.html"{a3}>제품 등록</a>
            <a href="law-export-tw-04.html"{a4}>수출통관/선적</a>
            <a href="law-export-tw-05.html"{a5}>현지통관 및 시판 후 관리</a>
          </nav>"""


def step_nav(active: int) -> str:
    attrs = {i: "" for i in range(6)}
    attrs[active] = ' class="is-active" aria-current="page"'
    return STEP_NAV.format(**{f"a{i}": attrs[i] for i in range(6)})


def wrap_page(template: str, *, title: str, desc: str, crumb: str, page_tit: str, body: str) -> str:
    html = template
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc}">',
        html,
        count=1,
    )
    html = re.sub(
        r'(<span class="current" aria-current="page">)[^<]*(</span>)',
        rf"\1{crumb}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<h2 class="page-tit">)[^<]*(</h2>)',
        rf"\1{page_tit}\2",
        html,
        count=1,
    )
    # detail breadcrumb parent link (EU → TW)
    html = html.replace(
        '<a href="law-export-eu.html">수출절차</a>',
        '<a href="law-export-tw.html">수출절차</a>',
    )
    # overview template may leave EU active tab markup outside replaced body; body already has TW tabs
    m = re.search(r'<div class="sub-doc law-export">[\s\S]*?</div>\s*</div>\s*</main>', html)
    if not m:
        raise SystemExit("sub-doc block not found")
    new_block = f'<div class="sub-doc law-export">\n{body}\n        </div>\n      </div>\n    </main>'
    return html[: m.start()] + new_block + html[m.end() :]
