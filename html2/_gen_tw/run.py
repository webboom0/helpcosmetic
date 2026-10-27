# -*- coding: utf-8 -*-
"""Generate Taiwan law-export HTML pages and verify PPT coverage."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from _gen_tw.shell import ROOT as HROOT, wrap_page  # noqa: E402
from _gen_tw import body_ov, body_01, body_02, body_03, body_04, body_05  # noqa: E402

TPL_OV = (HROOT / "law-export-eu.html").read_text(encoding="utf-8")
TPL_DET = (HROOT / "law-export-eu-01.html").read_text(encoding="utf-8")

PAGES = [
    {
        "out": "law-export-tw.html",
        "tpl": TPL_OV,
        "title": "수출절차 | 화장품글로벌규제조화지원센터",
        "desc": "대만 화장품 수출 규제 주요 절차 — 수출계약·상표등록, 수입업자 선임 및 PIF, 제품등록, 수출통관, 현지통관·시판후관리",
        "crumb": "수출절차",
        "page_tit": "수출절차",
        "body": body_ov.BODY,
    },
    {
        "out": "law-export-tw-01.html",
        "tpl": TPL_DET,
        "title": "수출 계약 및 상표등록 | 대만 수출절차",
        "desc": "대만 화장품 수출계약 및 TIPO 상표등록 절차",
        "crumb": "수출 계약 및 상표등록",
        "page_tit": "수출 계약 및 상표등록",
        "body": body_01.BODY,
    },
    {
        "out": "law-export-tw-02.html",
        "tpl": TPL_DET,
        "title": "대만 내 수입업자 선임 및 PIF 준비 | 대만 수출절차",
        "desc": "대만 내 수입업자 선임 및 PIF 준비 절차",
        "crumb": "대만 내 수입업자 선임 및 PIF 준비",
        "page_tit": "대만 내 수입업자 선임 및 PIF 준비",
        "body": body_02.BODY,
    },
    {
        "out": "law-export-tw-03.html",
        "tpl": TPL_DET,
        "title": "제품 등록 | 대만 수출절차",
        "desc": "대만 TFDA 화장품 제품정보 등록 절차",
        "crumb": "제품 등록",
        "page_tit": "제품 등록",
        "body": body_03.BODY,
    },
    {
        "out": "law-export-tw-04.html",
        "tpl": TPL_DET,
        "title": "수출통관/선적 | 대만 수출절차",
        "desc": "대만 화장품 수출통관 및 선적 절차",
        "crumb": "수출통관/선적",
        "page_tit": "수출통관/선적",
        "body": body_04.BODY,
    },
    {
        "out": "law-export-tw-05.html",
        "tpl": TPL_DET,
        "title": "현지통관 및 시판 후 관리 | 대만 수출절차",
        "desc": "대만 현지통관 및 TFDA 시판 후 관리 절차",
        "crumb": "현지통관 및 시판 후 관리",
        "page_tit": "현지통관 및 시판 후 관리",
        "body": body_05.BODY,
    },
]

PPT_URLS = [
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863913",
    "https://cloud.tipo.gov.tw/S282/S282WV1/",
    "https://www.fda.gov.tw/ENG/siteListContent.aspx?sid=10334&id=41180",
    "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5668&page=1&code=foreign&searchopt=&searchkey=%EC%9C%84%EC%83%9D%EC%95%88%EC%A0%84",
    "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5629&page=1&code=foreign&searchopt=&searchkey=%EB%A7%A4%EB%89%B4%EC%96%BC",
    "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5630&page=1&code=foreign&searchopt=&searchkey=%ED%99%94%EC%9E%A5%ED%92%88%20%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4%20%EB%AC%B8%EC%84%9C%EC%9E%91%EC%84%B1%20%EB%A7%A4%EB%89%B4%EC%96%BC",
    "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5823&page=1&code=foreign&searchopt=&searchkey=%ED%99%94%EC%9E%A5%ED%92%88%20%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4%20%EB%AC%B8%EC%84%9C",
    "https://kcia.or.kr/inc/down.php?dir=BOARD&file_name=202310_169640754590651_1.docx&rename=%ED%99%94%EC%9E%A5%ED%92%88+%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4+%EB%AC%B8%EC%84%9C%EC%9E%91%EC%84%B1+%EB%A7%A4%EB%89%B4%EC%96%BC_%EA%B5%AD%EB%AC%B8.docx",
    "https://cos.fda.gov.tw/TCAL/",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863914",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1720212",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863877",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1863940",
    "https://kcia.or.kr/home/law/%EC%84%A0%ED%95%98%EC%A6%9D%EA%B6%8C.pdf",
    "https://www.kita.net/board/format/formatDetail.do?postIndex=1719028&ContentsID=KI_cmmrcFormat_1719028&query=AWB",
    "https://kcia.or.kr/cert/main/",
    "https://kcia.or.kr/home/law/%EA%B8%B0%ED%83%80%20%EC%88%98%EC%B6%9C%ED%86%B5%EA%B4%80%EC%97%90%20%ED%95%84%EC%9A%94%ED%95%9C%20%EC%84%9C%EB%A5%98.pdf",
    "https://unipass.customs.go.kr/clip/index.do",
    "https://web.customs.gov.tw/en/singlehtml/3333?cntId=ef481d6f272c42ac98dca2c33502bb7c",
]

# PPT 본문 하이퍼링크에는 Drive 첨부 없음. 코멘트(첨부파일 N-N) + slide13 기재요령 메모만 HTML 다운로드로 연결.
# tw-1-2는 폴더에만 있고 코멘트/본문 링크 없음 → HTML 미연결.
ATTACH = [
    "tw-1-1-export-agency-ko.pdf",
    "tw-1-1-export-agency-en.pdf",
    "tw-2-1-importer-auth.pdf",
    "tw-4-1-export-declaration.pdf",
    "tw-4-2-commercial-invoice.pdf",
    "tw-4-3-proforma-invoice.pdf",
    "tw-4-4-packing-list.pdf",
    "tw-4-5-bl.pdf",
    "tw-4-6-awb.pdf",
    "tw-4-7-customs-docs.pdf",
    "tw-4-guide-commercial-invoice.hwp",  # slide13 메모 → tw-05만 링크
    "tw-4-guide-packing-list.xlsx",
    "tw-4-guide-awb.hwp",
    "tw-5-1-commercial-invoice.pdf",
    "tw-5-2-packing-list.pdf",
    "tw-5-3-bl.pdf",
    "tw-5-4-awb.pdf",
    "tw-5-5-import-declaration.pdf",
]


def main() -> None:
    written: list[Path] = []
    for p in PAGES:
        html = wrap_page(
            p["tpl"],
            title=p["title"],
            desc=p["desc"],
            crumb=p["crumb"],
            page_tit=p["page_tit"],
            body=p["body"],
        )
        # overview: fix breadcrumb parent if EU detail template left parent as 수출절차
        out = HROOT / p["out"]
        out.write_text(html, encoding="utf-8")
        written.append(out)
        print(f"Wrote {out.name}")

    all_html = "\n".join(f.read_text(encoding="utf-8") for f in written)
    lines: list[str] = []
    lines.append("# Taiwan export pages verification")
    lines.append("")
    lines.append(f"Generated pages: {len(written)}")
    for f in written:
        lines.append(f"- {f.name}")
    lines.append("")
    lines.append("## PPT unique URLs (19)")
    missing_urls = []
    for u in PPT_URLS:
        ok = u in all_html
        status = "OK" if ok else "MISSING"
        if not ok:
            missing_urls.append(u)
        lines.append(f"- [{status}] {u}")
    lines.append("")
    lines.append(f"URL coverage: {len(PPT_URLS) - len(missing_urls)}/{len(PPT_URLS)}")
    lines.append("")
    lines.append("## Attachment files (19)")
    files_dir = HROOT / "files" / "taiwan"
    missing_files = []
    missing_href = []
    for name in ATTACH:
        path = files_dir / name
        exists = path.is_file()
        href = f"files/taiwan/{name}"
        in_html = href in all_html
        if not exists:
            missing_files.append(name)
        if not in_html:
            missing_href.append(name)
        lines.append(
            f"- [{'OK' if exists else 'NOFILE'}][{'LINKED' if in_html else 'UNLINKED'}] {name}"
        )
    lines.append("")
    lines.append(
        f"File disk: {len(ATTACH) - len(missing_files)}/{len(ATTACH)}; "
        f"HTML linked: {len(ATTACH) - len(missing_href)}/{len(ATTACH)}"
    )
    # extra: lex-link / lex-dl counts
    lex_n = len(re.findall(r'class="lex-link"', all_html))
    dl_n = len(re.findall(r'class="lex-dl"', all_html))
    lines.append(f"lex-link count: {lex_n}")
    lines.append(f"lex-dl count: {dl_n}")
    lines.append("")
    if missing_urls or missing_files or missing_href:
        lines.append("## FAILURES")
        for u in missing_urls:
            lines.append(f"- missing URL: {u}")
        for n in missing_files:
            lines.append(f"- missing file: {n}")
        for n in missing_href:
            lines.append(f"- unlinked file: {n}")
        ok = False
    else:
        lines.append("## RESULT: ALL CHECKS PASSED")
        ok = True

    verify = HROOT / "_tw_verify.txt"
    verify.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(verify.read_text(encoding="utf-8"))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
