# -*- coding: utf-8 -*-
"""Build structured markdown report _ppt_eu_map.txt from extracted JSON."""
import json

JSON_PATH = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_raw.json'
OUT_PATH = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_eu_map.txt'

with open(JSON_PATH, encoding='utf-8') as f:
    slides = json.load(f)

lines = []
W = lines.append

W('# EU 화장품 수출 절차 PPT 추출 맵')
W('')
W('## Source')
W('')
W('- PPTX: `html2/5개국 도식화(최종)_261023/5개국 도식화(최종)_261023/EU/EU 화장품 수출 절차 도식화_5차 보완_261012_수정.pptx`')
W('- 첨부자료 폴더: `.../EU/첨부자료/`')
W('- 슬라이드 수: 14')
W('- 추출 방식: PPTX unzip + slide XML / relationships 파싱 (visible `a:t` 텍스트 + `a:hlinkClick` + External hyperlink rels)')
W('')

W('## Step flow (inferred)')
W('')
W('Overview(슬라이드 2) 배너와 본문 슬라이드 번호를 합치면 **5단계** (+ overview 배너의 "사후관리"는 상세 슬라이드 없음):')
W('')
W('| # | Step key (suggested) | 제목 (PPT) | 상세 슬라이드 | 하위 섹션 |')
W('|---|----------------------|------------|---------------|-----------|')
W('| 01 | `eu-export-contract-trademark` | 수출계약 및 상표등록 | 3–6 | 수출계약 및 신고필증 / 상표등록(EUIPO) / 상표등록(WIPO) / 상표등록(개별국·BOIP) |')
W('| 02 | `eu-responsible-person` | 유럽 책임자(RP, Responsible Person) 선임 | 7 | RP 선임 |')
W('| 03 | `eu-product-notification` | 제품 신고/ 서류 구비 | 8–11 | PIF / CPSR / CPNP 신고(+주의) |')
W('| 04 | `eu-export-customs` | 수출통관/선적 | 12 | 수출통관 |')
W('| 05 | `eu-local-customs` | 현지통관 | 13–14 | 현지통관 |')
W('')
W('슬라이드 2 overview 배너 문구(좌→우):')
W('')
W('1. 수출 계약 및 상표등록')
W('2. 유럽 책임자(RP) 선임')
W('3. 제품 신고/ 서류 구비 — 하위: `PIF  및 CPSR 구축` / `CPNP 신고`')
W('4. 통관')
W('5. 사후관리  ← **상세 슬라이드 없음** (01–05만 존재; 04·05가 통관을 수출/현지로 분리)')
W('')

W('## Slide index')
W('')
W('| Slide | 대주제 | 소주제/타이틀 |')
W('|-------|--------|---------------|')
W('| 1 | 표지 | 유럽연합(EU) 화장품 수출 절차 |')
W('| 2 | overview | 화장품 수출 규제 주요 절차 |')
W('| 3 | 01. 수출계약 및 상표등록 | 수출계약 및 신고필증 |')
W('| 4 | 01. 수출계약 및 상표등록 | 상표등록 (EUIPO) |')
W('| 5 | 01. 수출계약 및 상표등록 | 상표등록 (WIPO) |')
W('| 6 | 01. 수출계약 및 상표등록 | 상표등록 (개별 회원국 / BOIP) |')
W('| 7 | 02. 유럽 책임자(RP) 선임 | (단일 표) |')
W('| 8 | 03. 제품 신고/ 서류 구비 | PIF(제품정보파일) |')
W('| 9 | 03. 제품 신고/ 서류 구비 | CPSR 구축 |')
W('| 10 | 03. 제품 신고/ 서류 구비 | CPNP 신고 |')
W('| 11 | 03. 제품 신고/ 서류 구비 | CPNP 신고 — 주의사항 |')
W('| 12 | 04. 수출통관/선적 | 수출통관 |')
W('| 13 | 05. 현지통관 | 현지통관 (서류) |')
W('| 14 | 05. 현지통관 | 현지통관 (절차·주의) |')
W('')


def cell_md(s):
    """Preserve newlines as <br> for markdown table cells; escape pipes."""
    if s is None:
        return ''
    return s.replace('|', '\\|').replace('\n', '<br>')


def emit_table(tbl, title=None):
    rows = tbl['rows']
    if not rows:
        return
    # detect column count
    ncols = max(len(r) for r in rows)
    # If first col looks like labels and 2+ content cols, keep as-is
    if title:
        W(f'**{title}**')
        W('')
    # Header: use C0.. or treat row0 specially? Better: Label | Content... based on actual first row labels
    # Always render as markdown with synthetic header Col0..ColN-1, then all data rows
    # Prefer: if ncols==2: | 항목 | 내용 |
    # if ncols==3: | 항목 | 내용1 | 내용2 |
    if ncols == 2:
        W('| 항목 | 내용 |')
        W('|------|------|')
        for r in rows:
            c0 = cell_md(r[0] if len(r) > 0 else '')
            c1 = cell_md(r[1] if len(r) > 1 else '')
            W(f'| {c0} | {c1} |')
    elif ncols == 3:
        W('| 항목 | 내용 A | 내용 B |')
        W('|------|--------|--------|')
        for r in rows:
            c0 = cell_md(r[0] if len(r) > 0 else '')
            c1 = cell_md(r[1] if len(r) > 1 else '')
            c2 = cell_md(r[2] if len(r) > 2 else '')
            W(f'| {c0} | {c1} | {c2} |')
    else:
        header = '| ' + ' | '.join(f'C{i}' for i in range(ncols)) + ' |'
        sep = '| ' + ' | '.join(['---'] * ncols) + ' |'
        W(header)
        W(sep)
        for r in rows:
            cells = [cell_md(r[i] if i < len(r) else '') for i in range(ncols)]
            W('| ' + ' | '.join(cells) + ' |')
    W('')


def slide_title_bits(s):
    shapes = s.get('shapes') or []
    # topmost few textboxes
    titles = []
    for sh in shapes:
        for p in sh['paras']:
            titles.append(p)
    return titles


# ---- Per-step content ----
W('## Per-step content (verbatim Korean)')
W('')

# Step 0 cover/overview
W('### Cover & Overview')
W('')
W('#### Slide 1 — 표지')
W('')
W('- 유럽연합(EU) 화장품 수출 절차')
W('')
W('#### Slide 2 — 화장품 수출 규제 주요 절차')
W('')
W('- 수출 계약 및 상표등록')
W('- 유럽 책임자(RP) / 선임')
W('- 제품 신고/ 서류 구비')
W('- `PIF  및 CPSR 구축CPNP 신고` (텍스트박스에 PIF/CPSR와 CPNP가 이어 붙음; 시각적으로는 분리된 배너로 보임)')
W('- 통관')
W('- 사후관리')
W('')

# Group slides by step
step_groups = [
    ('01. 수출계약 및 상표등록', [3, 4, 5, 6]),
    ('02. 유럽 책임자(RP, Responsible Person) 선임', [7]),
    ('03. 제품 신고/ 서류 구비', [8, 9, 10, 11]),
    ('04. 수출통관/선적', [12]),
    ('05. 현지통관', [13, 14]),
]

by_num = {s['slide']: s for s in slides}

for step_title, nums in step_groups:
    W(f'### {step_title}')
    W('')
    for n in nums:
        s = by_num[n]
        titles = slide_title_bits(s)
        # first two title-like shapes
        big = titles[0] if titles else f'Slide {n}'
        sub = titles[1] if len(titles) > 1 else ''
        # filter "다음 페이지에 이어서"
        extras = [t for t in titles[2:] if t != '다음 페이지에 이어서']
        W(f'#### Slide {n} — {big}' + (f' / {sub}' if sub and sub != '다음 페이지에 이어서' else ''))
        W('')
        if any(t == '다음 페이지에 이어서' for t in titles):
            W('- (하단 메모: 다음 페이지에 이어서)')
            W('')
        for tbl_i, tbl in enumerate(s.get('tables') or []):
            emit_table(tbl, title=None if len(s.get('tables') or []) == 1 else f'Table {tbl_i+1}')
        if not s.get('tables'):
            W('_표 없음_')
            W('')
        # links on this slide
        gl = s.get('grouped_links') or []
        if gl:
            W('Hyperlinks on this slide:')
            W('')
            for L in gl:
                W(f"- anchor: `{L['text']}`")
                W(f"  - URL: `{L['url']}`")
            W('')

W('## All hyperlinks (complete inventory)')
W('')
W('Exact relationship Target URLs. Do not shorten.')
W('')
W('| Slide | Step | Anchor text (verbatim) | Full URL |')
W('|-------|------|------------------------|----------|')

link_rows = [
    (3, '01 수출계약', '수출계약서 예시', 'https://www.kyungnam.ac.kr/bbs/kuit/314/46382/artclView.do'),
    (3, '01 수출계약', '수출대행계약서 예시', 'https://www.kita.net/board/format/formatDetail.do?postIndex=1863913'),
    (3, '01 수출계약', '수출신고서 양식', 'https://www.kita.net/board/format/formatDetail.do?postIndex=1863914'),
    (3, '01 수출계약', 'UNI-PASS 포털', 'https://unipass.customs.go.kr/csp/index.do?utm_source=chatgpt.com'),
    (4, '01 상표 EUIPO', 'TMclass', 'https://euipo.europa.eu/ec2/'),
    (4, '01 상표 EUIPO', 'TMview', 'https://www.tmdn.org/tmview/#/tmview'),
    (4, '01 상표 EUIPO', 'eSearch plus', 'https://euipo.europa.eu/eSearch/'),
    (5, '01 상표 WIPO', '* WIPO 마드리드 홈페이지 ', 'https://www.wipo.int/en/web/madrid-system'),
    (6, '01 상표 개별/BOIP', '각국 상표청의 전체 목록', 'https://tmdn.org/#/members'),
    (6, '01 상표 개별/BOIP', 'BOIP 상표 출원 홈페이지', 'https://www.boip.int/nl'),
    (6, '01 상표 개별/BOIP', '[베네룩스 상표 등록 절차]', 'https://www.boip.int/en/entrepreneurs/trademarks/register-a-benelux-trademark#step-3'),
    (10, '03 CPNP', 'CPNP (Cosmetic Products Notification Portal)', 'https://webgate.ec.europa.eu/cpnp/'),
    (13, '05 현지통관', '[EU 세관 통관에 필요한 서류]', 'https://trade.ec.europa.eu/access-to-markets/en/content/customs-clearance-documents-and-procedures-0'),
    (14, '05 현지통관', 'Access2Markets', 'https://trade.ec.europa.eu/access-to-markets/en/home'),
]

for slide, step, anchor, url in link_rows:
    anchor_esc = anchor.replace('|', '\\|')
    W(f'| {slide} | {step} | {anchor_esc} | `{url}` |')

W('')
W('**Total unique External hyperlink targets in PPT relationships: 14**')
W('')
W('Cross-check: every External hyperlink in `ppt/slides/_rels/slide*.xml.rels` is listed above. No Google Drive / mailto / embedded OLE attachment links exist in this EU PPT (unlike the US PPT).')
W('')

W('## Attachment file inventory')
W('')
W('Folder: `.../EU/첨부자료/`')
W('')
W('PPT 본문에는 첨부파일 Drive 링크가 없고, **모던 코멘트**에 `첨부파일 1-1` 등으로만 매핑이 남아 있음.')
W('')
W('| 원본 파일명 | 코멘트/추정 매핑 | Step | 관련 슬라이드 | Suggested web filename |')
W('|-------------|------------------|------|---------------|------------------------|')
W('| `1-1. 수출계약서예시.hwp` | 첨부파일 1-1 (slide3 comment) | 01 수출계약 | 3 | `eu-1-1-export-contract-example.hwp` |')
W('| `1-2. 수출대행계약서.zip` → `1-1. 수출대행계약서_국문.pdf` | 첨부파일 1-2 | 01 수출계약 | 3 | `eu-1-2-export-agency-ko.pdf` |')
W('| `1-2. 수출대행계약서.zip` → `1-1. 수출대행계약서_영문.pdf` | 첨부파일 1-2 | 01 수출계약 | 3 | `eu-1-2-export-agency-en.pdf` |')
W('| `1-3. 수출신고서, 수출신고필증.pdf` | 첨부파일 1-3 | 01 수출계약 | 3 | `eu-1-3-export-declaration.pdf` |')
W('| `2. CPNP 신고 가이드라인.pdf` | 첨부파일 2 (slide10 comment); 표 문구 `* CPNP 신고 가이드라인` | 03 CPNP | 10 | `eu-2-cpnp-guide.pdf` |')
W('| `3-1. 선하증권.pdf` | 첨부파일 3-1 (slide12 comment) | 04 수출통관 | 12 | `eu-3-1-bl.pdf` |')
W('| `3-2. 항공화물 운송장(Air Waybill).pdf` | 첨부파일 3-2 | 04 수출통관 | 12 | `eu-3-2-awb.pdf` |')
W('| `3-3. 송장.zip` → `상업송장.pdf` | 첨부파일 3-3 | 04 수출통관 | 12 | `eu-3-3-commercial-invoice.pdf` |')
W('| `3-3. 송장.zip` → `견적송장.pdf` | 첨부파일 3-3 | 04 수출통관 | 12 | `eu-3-3-proforma-invoice.pdf` |')
W('| `3-4. 포장명세서.pdf` | 첨부파일 3-4 | 04 수출통관 | 12 | `eu-3-4-packing-list.pdf` |')
W('| `3-5. 기타 수출통관에 필요한 서류.pdf` | 첨부파일 3-5 | 04 수출통관 | 12 | `eu-3-5-customs-docs.pdf` |')
W('')
W('Slide 12 표의 참고서류 라벨과의 대응:')
W('')
W('- 수출 신고서 → (첨부 1-3에도 관련; 슬라이드 3에서도 다룸)')
W('- 송장 (invoice) → 3-3 상업/견적송장')
W('- 포장명세서 → 3-4')
W('- 기타 수출통관에 필요한 서류 → 3-5')
W('- 선하증권 / 항공화물운송장 → 본문 slide12에는 명시적 행이 약하지만 comment·첨부 3-1/3-2 및 slide13 수입서류에 등장')
W('')

W('## Notes / ambiguities')
W('')
W('1. **사후관리**: overview(슬라이드 2)에 배너로 있으나 01–05 상세 슬라이드에 대응 페이지가 없음. 웹 구현 시 5단계만 쓰거나, 사후관리를 별도 placeholder로 둘지 결정 필요.')
W('2. **통관 분리**: overview는 "통관" 1칸이지만 본문은 `04. 수출통관/선적` + `05. 현지통관`으로 분리. CN/US와 같이 5-step으로 맞추면 이 분리가 자연스러움.')
W('3. **첨부 번호 ≠ 단계 번호**: 첨부는 1/2/3 체계(계약·CPNP·통관서류). 단계 04/05와 첨부 3-x가 혼동될 수 있음. 웹 파일명은 `eu-3-*`를 통관서류 묶음으로 유지하는 편이 PPT와 일치.')
W('4. **첨부 하이퍼링크 부재**: US PPT처럼 Google Drive 링크가 본문에 없음. `* CPNP 신고 가이드라인` 텍스트도 하이퍼링크 아님(코멘트만 "첨부파일 2"). 웹 이식 시 로컬 `files/eu/` 링크로 새로 걸어야 함.')
W('5. **UNI-PASS URL**에 `?utm_source=chatgpt.com` 쿼리가 그대로 들어 있음. PPT 원문 유지; 웹에서는 정제 여부 정책 결정 필요.')
W('6. **WIPO 링크 앵커**: 하이퍼링크 런 텍스트가 `* WIPO 마드리드 홈페이지 `(끝 공백 포함)이며, 같은 문장의 `수수료자동계산기에서 확인` 부분은 링크 밖.')
W('7. **Slide 6 표**: 3열(방식/개별국/BOIP). 행 라벨이 `방식|기관|참고 또는 필요서류|절차|주의사항` — `설명 또는 정의` 행 없음(이전 EUIPO/WIPO 슬라이드와 구조 다름).')
W('8. **Slide 7 RP 표**: 행 라벨이 `대리인 역할|대리인 자격 요건|선정 요령/체크포인트|수권 계약서|주의사항|필요서류` — 일반 `설명/방식/기관/...` 패턴과 다름. C2 열은 역할 행만 실질 내용, 나머지 C2는 비어 있음.')
W('9. **Slide 10**: `방식` 순서가 `RP선정 → CPSR 작성 → PIF 작성 → CPNP 등록`인데 slide 8은 `RP선정 → PIF 구비 → CPSR 작성 → CPNP 신고`. PIF/CPSR 순서 불일치 — 원문 그대로 보존.')
W('10. **Slide 13 수입서류 목록**: `특수 화장품 행정허가증 또는 일반화장품 등록증빙` 등은 중국 절차 표현과 유사해 보이며 EU 맥락에서 이질적일 수 있음(코멘트로 교정됐는지는 불명). 원문 유지.')
W('11. **Slide 3 외부 링크**: `수출계약서 예시`가 경남대 게시판 URL로 연결됨. 첨부 `1-1. 수출계약서예시.hwp`와 별개 소스. 코멘트에도 "한국무역협회로 이동되는데 맞을까요?" 논의 흔적.')
W('12. **Zip 내부 파일명**: `1-2` zip 안 PDF 파일명이 `1-1. 수출대행계약서_*.pdf`로 시작(zip 바깥 번호와 불일치).')
W('13. **Comments**: 편집 이력/오탈자 논의만 있으며 추가 URL 없음.')
W('')

W('## Raw slide text dump (shape order)')
W('')
for s in slides:
    W(f'### SLIDE {s["slide"]}')
    W('')
    for sh in s.get('shapes') or []:
        for p in sh['paras']:
            W(f'- {p}')
    for ti, tbl in enumerate(s.get('tables') or []):
        W(f'- [TABLE {ti+1}]')
        for ri, row in enumerate(tbl['rows']):
            for ci, cell in enumerate(row):
                one = cell.replace('\n', ' / ')
                W(f'  - R{ri}C{ci}: {one}')
    for L in s.get('grouped_links') or []:
        W(f'- HLINK: `{L["text"]}` => `{L["url"]}`')
    W('')

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Wrote {OUT_PATH} ({len(lines)} lines)')
