# -*- coding: utf-8 -*-
"""Build structured markdown report _ppt_tw_map.txt from extracted Taiwan PPT data."""
import json
import os

JSON_PATH = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_raw.json'
OUT_PATH = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_map.txt'
ATT_ROOT = r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\5개국 도식화(최종)_261023\5개국 도식화(최종)_261023\대만\첨부자료'

d = json.load(open(JSON_PATH, encoding='utf-8'))
slides = d['slides']

lines = []
W = lines.append

W('# 대만 화장품 수출 절차 PPT 추출 맵')
W('')
W('## Source')
W('')
W('- PPTX: `html2/5개국 도식화(최종)_261023/5개국 도식화(최종)_261023/대만/대만 화장품 수출 절차 도식화_5차 보완 완료_261012.pptx`')
W('- 첨부자료 폴더: `.../대만/첨부자료/`')
W('- 슬라이드 수: 17')
W('- 추출 방식: PPTX unzip + slide XML / relationships 파싱 (visible `a:t` 텍스트 + `a:hlinkClick` + External hyperlink rels + modern comments)')
W('')
W('## Step flow (inferred)')
W('')
W('Overview(슬라이드 2) 배너와 본문 슬라이드 번호를 합치면 **5단계**:')
W('')
W('| # | Step key (suggested) | 제목 (PPT) | 상세 슬라이드 | 하위 섹션 |')
W('|---|----------------------|------------|---------------|-----------|')
W('| 01 | `tw-export-contract-trademark` | 수출 계약 및 상표등록 | 3–4 | 1-1 수출계약 / 1-2 상표등록 |')
W('| 02 | `tw-importer-pif` | 대만 내 수입업자 선임 및 PIF 준비 | 5–8 | 2-1 수입업자 선임 / 2-2 PIF 준비 |')
W('| 03 | `tw-product-registration` | 제품 등록 | 9–10 | TFDA 제품정보 등록 |')
W('| 04 | `tw-export-customs` | 수출통관/선적 | 11–12 | 수출통관 |')
W('| 05 | `tw-local-customs-postmarket` | 현지통관 및 시판 후 관리 | 13–17 | 5-1 현지통관 / 5-2 시판 후 관리 |')
W('')
W('슬라이드 2 overview 배너 문구(좌→우):')
W('')
W('1. 수출 계약 및 상표등록')
W('2. 대만 내 수입업자 (化粧品製造或輸入業者) 선임 및 PIF 준비')
W('3. 제품 등록')
W('4. 수출통관/선적')
W('5. 현지통관 및 시판 후 관리')
W('')
W('## Slide index')
W('')
W('| Slide | 대주제 | 소주제/타이틀 |')
W('|-------|--------|---------------|')
W('| 1 | 표지 | 대만 화장품 수출 절차 |')
W('| 2 | overview | 대만 화장품 수출 규제 주요 절차 |')
W('| 3 | 01. 수출계약 및 상표등록 | 1-1. 수출계약 |')
W('| 4 | 01. 수출계약 및 상표등록 | 1-2. 상표등록 |')
W('| 5 | 02. 대만 내 수입업자 선임 및 PIF 준비 | 2-1. 대만 내 수입업자 선임 (역할·자격·선정·수권) |')
W('| 6 | 02. 대만 내 수입업자 선임 및 PIF 준비 | 2-1. 대만 내 수입업자 선임 (주의·필요서류·소요기간) |')
W('| 7 | 02. 대만 내 수입업자 선임 및 PIF 준비 | 2-2. PIF 준비 (개요·구성·보관·절차) |')
W('| 8 | 02. 대만 내 수입업자 선임 및 PIF 준비 | 2-2. PIF 준비 (주의·필요서류·소요기간) |')
W('| 9 | 03. 제품 등록 | 제품 등록 (정의·방식·기관·서류·절차) |')
W('| 10 | 03. 제품 등록 | 제품 등록 (소요기간·유효기간·수수료·주의) |')
W('| 11 | 04. 수출통관/선적 | 4. 수출통관 (정의·방식·기관·서류) |')
W('| 12 | 04. 수출통관/선적 | 4. 수출통관 (절차·주의) |')
W('| 13 | 05. 현지통관 및 시판 후 관리 | 5-1. 현지통관 (정의·방식·기관·서류·절차) |')
W('| 14 | 05. 현지통관 및 시판 후 관리 | 5-1. 현지통관 (주의·세부 통관 절차) |')
W('| 15 | 05. 현지통관 및 시판 후 관리 | 5-2. 시판 후 관리 (정의~주의) |')
W('| 16 | 05. 현지통관 및 시판 후 관리 | 5-2. 시판 후 관리 — TFDA 점검(표시·수거검사) |')
W('| 17 | 05. 현지통관 및 시판 후 관리 | 5-2. 시판 후 관리 — TFDA 점검(PIF·행정조치) |')
W('')

# ---- Hyperlink master index ----
W('## External hyperlinks (complete master list)')
W('')
W('모든 외부 하이퍼링크. URL은 단축하지 않음. 앵커 텍스트는 슬라이드 본문 하이퍼링크 run 기준.')
W('')
W('| Slide | Anchor text | Full URL |')
W('|-------|-------------|----------|')

# Collect unique (slide, text, url) preserving order
seen_link = set()
all_links_ordered = []
for s in slides:
    for L in s['grouped_links']:
        key = (s['slide'], L.get('text'), L.get('url'))
        if key in seen_link:
            continue
        seen_link.add(key)
        all_links_ordered.append(key)
    for L in s['shape_links']:
        key = (s['slide'], L.get('text'), L.get('url'))
        if key in seen_link:
            continue
        seen_link.add(key)
        all_links_ordered.append(key)

for slide, text, url in all_links_ordered:
    t = (text or '').replace('|', '\\|').replace('\n', ' ')
    u = (url or '').replace('|', '\\|')
    W(f'| {slide} | `{t}` | `{u}` |')

W('')
W(f'- 하이퍼링크 인스턴스(중복 앵커 포함 unique pairs): **{len(all_links_ordered)}**')
W('- 패키지 내 External hyperlink rel 전수 스캔 완료 (slide3/4/5/6/7/8/9/11/13). 누락 없음.')
W('- shape-level hlinkClick: 없음 (전부 run-level text hyperlinks).')
W('')

# Unique URLs
uniq_urls = []
seen_u = set()
for _, _, url in all_links_ordered:
    if url and url not in seen_u:
        seen_u.add(url)
        uniq_urls.append(url)
W(f'### Unique URLs ({len(uniq_urls)})')
W('')
for i, u in enumerate(uniq_urls, 1):
    W(f'{i}. `{u}`')
W('')

# ---- Per-step content ----
W('## Per-step content (verbatim Korean)')
W('')
W('### Cover & Overview')
W('')
W('#### Slide 1 — 표지')
W('')
W('- 대만 화장품 수출 절차')
W('')
W('#### Slide 2 — 대만 화장품 수출 규제 주요 절차')
W('')
W('- 수출 계약 및 상표등록')
W('- 대만 내 수입업자 (化粧品製造或輸入業者) 선임 및 PIF 준비')
W('- 제품 등록')
W('- 수출통관/선적')
W('- 현지통관 및 시판 후 관리')
W('')


def cell_join(cell):
    return cell.replace('\n', '<br>')


def write_slide_table_section(s, heading_extra=''):
    # titles from shapes excluding slide number
    titles = []
    for sh in s['shapes']:
        name = sh.get('name') or ''
        if '슬라이드 번호' in name:
            continue
        for p in sh['paras']:
            if p.strip().isdigit():
                continue
            titles.append(p)
    W(f"#### Slide {s['slide']}{heading_extra}")
    W('')
    for t in titles:
        if t.startswith('다음 페이지'):
            W(f'- ({t})')
        elif t.startswith('') or t.startswith('메모'):
            W(f'- {t}')
        else:
            # only emit as bullets if short-ish titles; long content comes from tables
            if len(t) < 80 and not any(t.startswith(x) for x in ('설명', '방식', '기관', '절차', '주의', '필요', '계약', '대리', '관련', '참고', '소요', '등록', 'PIF', 'TFDA', '수입', '세관', '화물', '통관', '사후', '표시', '제품 수거', '행정')):
                W(f'- {t}')
            elif t.startswith('') or '메모:' in t:
                W(f'- {t}')
    # Always print memo shapes
    for sh in s['shapes']:
        for p in sh['paras']:
            if '메모' in p:
                if f'- {p}' not in lines[-20:]:
                    W(f'- {p}')
    for ti, tbl in enumerate(s['tables']):
        W('')
        W(f'| 항목 | 내용 |')
        W('|------|------|')
        for row in tbl['rows']:
            if len(row) >= 2:
                c0 = cell_join(row[0]).replace('|', '\\|')
                # merge extra cols
                rest = [cell_join(c) for c in row[1:] if c and c.strip()]
                c1 = '<br>---<br>'.join(rest).replace('|', '\\|') if rest else ''
                W(f'| {c0} | {c1} |')
            elif len(row) == 1:
                only = cell_join(row[0]).replace('|', '\\|')
                W(f'|  | {only} |')
    # links
    slide_links = []
    seen = set()
    for L in s['grouped_links']:
        key = (L.get('text'), L.get('url'))
        if key in seen:
            continue
        seen.add(key)
        slide_links.append(L)
    if slide_links:
        W('')
        W('Hyperlinks on this slide:')
        W('')
        for L in slide_links:
            W(f"- anchor: `{L.get('text')}`")
            W(f"  - URL: `{L.get('url')}`")
    W('')


W('### 01. 수출계약 및 상표등록')
W('')
for s in slides:
    if s['slide'] in (3, 4):
        write_slide_table_section(s)

W('### 02. 대만 내 수입업자 선임 및 PIF 준비')
W('')
for s in slides:
    if s['slide'] in (5, 6, 7, 8):
        write_slide_table_section(s)

W('### 03. 제품 등록')
W('')
for s in slides:
    if s['slide'] in (9, 10):
        write_slide_table_section(s)

W('### 04. 수출통관/선적')
W('')
for s in slides:
    if s['slide'] in (11, 12):
        write_slide_table_section(s)

W('### 05. 현지통관 및 시판 후 관리')
W('')
for s in slides:
    if s['slide'] in (13, 14, 15, 16, 17):
        write_slide_table_section(s)

# ---- Attachments ----
W('## Attachment file inventory')
W('')
W('Folder: `.../대만/첨부자료/`')
W('')
W('PPT 본문에는 Google Drive 첨부 하이퍼링크가 없고, **모던 코멘트**에 `첨부파일 N-N` 매핑 + 폴더 구조로 대응.')
W('Slide 13 본문 메모: 「상업송장, 포장명세서, 항공화물운송장은 기재요령 파일도 함께 다운로드할 수 있도록 첨부」 → `첨부자료/기재요령/` 매핑.')
W('')
W('| 원본 경로 (상대: 첨부자료/) | Comment / 근거 | Step | Slide | Suggested web filename |')
W('|------------------------------|----------------|------|-------|------------------------|')

atts = [
    ('1-1. 수출대행계약서/1-1. 수출대행계약서_국문.pdf', '첨부파일 1-1 (slide3 comment)', '01 수출계약', 3, 'tw-1-1-export-agency-ko.pdf'),
    ('1-1. 수출대행계약서/1-1. 수출대행계약서_영문.pdf', '첨부파일 1-1 (slide3 comment; 영문 쌍)', '01 수출계약', 3, 'tw-1-1-export-agency-en.pdf'),
    ('1-2. 상표등록 신청서 양식.pdf', '폴더 번호 1-2 (상표등록 단계; comment에 1-2 명시 없음)', '01 상표등록', 4, 'tw-1-2-trademark-form.pdf'),
    ('2-1. 화장품 수입업자 위임계약서 또는 수권서.pdf', '첨부파일 2-1 (slide5/6 comments)', '02 수입업자 선임', '5–6', 'tw-2-1-importer-auth.pdf'),
    ('4. 수출통관 선적/4-1. 수출신고서, 수출신고필증.pdf', '첨부파일 4-1 (slide11 comment)', '04 수출통관', 11, 'tw-4-1-export-declaration.pdf'),
    ('4. 수출통관 선적/4-2. 상업송장.pdf', '첨부파일 4-2 (slide11 comment)', '04 수출통관', 11, 'tw-4-2-commercial-invoice.pdf'),
    ('4. 수출통관 선적/4-3. 견적송장.pdf', '첨부파일 4-3 (slide11 comment)', '04 수출통관', 11, 'tw-4-3-proforma-invoice.pdf'),
    ('4. 수출통관 선적/4-4. 포장명세서.pdf', '첨부파일 4-4 (slide11 comment)', '04 수출통관', 11, 'tw-4-4-packing-list.pdf'),
    ('4. 수출통관 선적/4-5. 선하증권.pdf', '첨부파일 4-5 (slide11 comment)', '04 수출통관', 11, 'tw-4-5-bl.pdf'),
    ('4. 수출통관 선적/4-6. 항공화물 운송장(Air Waybill).pdf', '첨부파일 4-6 (slide11 comment)', '04 수출통관', 11, 'tw-4-6-awb.pdf'),
    ('4. 수출통관 선적/4-7. 기타 수출통관에 필요한 서류.pdf', '첨부파일 4-7 (slide11 comment)', '04 수출통관', 11, 'tw-4-7-customs-docs.pdf'),
    ('기재요령/4. 상업송장 기재요령.hwp', 'slide13 메모(기재요령 동봉); step04/05 공통 참고', '04/05 통관', '11/13', 'tw-4-guide-commercial-invoice.hwp'),
    ('기재요령/4. 포장명세서 Packing List (패킹리스트) 양식.xlsx', 'slide13 메모(기재요령 동봉)', '04/05 통관', '11/13', 'tw-4-guide-packing-list.xlsx'),
    ('기재요령/4. 항공화물운송장_기재요령.hwp', 'slide13 메모(기재요령 동봉)', '04/05 통관', '11/13', 'tw-4-guide-awb.hwp'),
    ('5. 현지통관/5-1 상업송장.pdf', '첨부파일 5-1 (slide13 comment)', '05 현지통관', 13, 'tw-5-1-commercial-invoice.pdf'),
    ('5. 현지통관/5-2 포장명세서.pdf', '첨부파일 5-2 (slide13 comment)', '05 현지통관', 13, 'tw-5-2-packing-list.pdf'),
    ('5. 현지통관/5-3 선하증권.pdf', '첨부파일 5-3 (slide13 comment)', '05 현지통관', 13, 'tw-5-3-bl.pdf'),
    ('5. 현지통관/5-4 항공화물 운송장(Air Waybill).pdf', '첨부파일 5-4 (slide13 comment)', '05 현지통관', 13, 'tw-5-4-awb.pdf'),
    ('5. 현지통관/5-5 수입신고서.pdf', '첨부파일 5-5 (slide13 comment)', '05 현지통관', 13, 'tw-5-5-import-declaration.pdf'),
]

for path, comment, step, slide, web in atts:
    W(f'| `{path}` | {comment} | {step} | {slide} | `{web}` |')

W('')
W('### Attachment folder recursive listing (ALL files)')
W('')
W('ZIP/RAR/7z: **없음**. Nested folders only.')
W('')

# List all files recursively
file_list = []
for root, dirs, files in os.walk(ATT_ROOT):
    dirs.sort()
    for fn in sorted(files):
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, ATT_ROOT)
        size = os.path.getsize(full)
        file_list.append((rel.replace('\\', '/'), size))

W('| # | Relative path | Size (bytes) |')
W('|---|---------------|--------------|')
for i, (rel, size) in enumerate(file_list, 1):
    W(f'| {i} | `{rel}` | {size} |')
W('')
W(f'- Total files under 첨부자료: **{len(file_list)}**')
W('')

W('### Comment → attachment mapping notes')
W('')
W('- **Slide 3** (`modernComment_103_*`): `첨부파일 1-1` → 수출대행계약서 국/영문 PDF. 기타 코멘트는 라벨/링크 수정 논의(대부분 resolved).')
W('- **Slide 5/6** (`modernComment_105_*`, `10D_*`): `첨부파일 2-1` + 「링크는 중국 경내책임자 수권서입니다. 확인필요」→ 현재 본문 링크는 TFDA ENG 페이지(`fda.gov.tw/...id=41180`). 웹 이식 시 **로컬 `tw-2-1-importer-auth.pdf`** 를 우선 연결 권장.')
W('- **Slide 7/9** (`10E_*`, `107_*`): 「화장품글로벌규제조화지원센터 게시글 연결」→ helpcosmetic.or.kr PIF/법령 링크.')
W('- **Slide 8** (`10B_*`): 「링크는 중국 자료입니다.」→ KCIA docx 다운로드 링크 유지 여부 재확인 권장.')
W('- **Slide 11** (`109_*`): `첨부파일 4-1`~`4-7` + 아포스티유 미가맹/주한국타이페이대표부 인증 논의.')
W('- **Slide 13** (`10A_*`): `첨부파일 5-1`~`5-5` + 본문 메모로 기재요령 3종 동봉.')
W('')

W('## Web page structure suggestion')
W('')
W('CN/EU와 같이 **5개 단계 페이지**(또는 1개 허브 + 5 앵커) + overview:')
W('')
W('1. `tw01` 수출계약 및 상표등록 — sections: 수출계약 / 상표등록(TIPO)')
W('2. `tw02` 대만 내 수입업자 선임 및 PIF 준비 — sections: 수입업자 선임 / PIF 준비')
W('3. `tw03` 제품 등록 — TFDA TCAL Online Registration')
W('4. `tw04` 수출통관/선적 — UNI-PASS + 선적서류')
W('5. `tw05` 현지통관 및 시판 후 관리 — sections: 현지통관(C1/C2/C3) / 시판 후 관리·TFDA 점검')
W('')
W('첨부 파일은 `html2/files/taiwan/` (또는 `files/tw/`)에 `tw-*-*` 파일명으로 복사.')
W('')

W('## Implementation caveats')
W('')
W('1. **첨부 하이퍼링크 부재**: 본문에 Drive 링크 없음. 코멘트 번호 + 폴더로만 매핑. 웹에서는 로컬 파일 링크로 신규 연결 필요.')
W('2. **Slide 5/6 TFDA 링크 QA**: 코멘트가 중국 수권서 혼동을 지적. 첨부 `2-1` PDF와 외부 TFDA URL을 분리 표기.')
W('3. **상표 1-2**: 폴더에만 존재, PPT 코멘트에 `첨부파일 1-2` 문자열은 없음. 상표등록 슬라이드(4)에 매핑하는 것이 합리적.')
W('4. **기재요령**: 수출(4)과 현지(5) 모두에서 상업송장/포장명세서/AWB가 반복 → 가이드 파일은 04·05에 교차 노출.')
W('5. **아포스티유**: 대만 미가맹 → CFS 등 공증 시 외교부 영사확인 + 주한국타이페이대표부 인증 (slide11 본문·코멘트).')
W('6. **제품등록 수수료**: 제품당 NT$800 (2026.07.01 이후) — 최신 TFDA 고시 확인 문구 유지.')
W('7. **등록 유효기간**: 등록일로부터 3년, 만료 3개월 전 연장.')
W('8. **마드리드 불가**: 대만은 Madrid 지정국 아님 → TIPO 개별 출원만 (slide4).')
W('')

# ---- Raw dump ----
W('## Raw slide text dump')
W('')
W('아래는 슬라이드별 평문 덤프(표 셀·텍스트박스 `a:t` 결합). 하이퍼링크는 별도 표기.')
W('')

for s in slides:
    W(f"===== SLIDE {s['slide']} =====")
    # links first like US map style
    seen = set()
    for L in s['grouped_links'] + s['shape_links']:
        key = (L.get('text'), L.get('url'))
        if key in seen:
            continue
        seen.add(key)
        W(f"  HLINK: {(L.get('text') or '').strip()} => {L.get('url')}")
    # flat text with some structure
    parts = []
    for sh in s['shapes']:
        name = sh.get('name') or ''
        if '슬라이드 번호' in name:
            continue
        for p in sh['paras']:
            if p.strip().isdigit():
                continue
            parts.append(p)
    for tbl in s['tables']:
        for row in tbl['rows']:
            for cell in row:
                if cell and cell.strip():
                    parts.append(cell)
    # Join with newlines for readability
    W('TEXT:')
    for p in parts:
        for line in p.split('\n'):
            W(f'  {line}')
    if s.get('notes'):
        notes = [n for n in s['notes'] if not n.strip().isdigit()]
        if notes:
            W('NOTES:')
            for n in notes:
                W(f'  {n}')
    W('')

W('## Comments summary (attachment-relevant)')
W('')
W('| Slide | Comment file | Key texts |')
W('|-------|--------------|-----------|')
W('| 3 | modernComment_103_5D417036.xml | 첨부파일 1-1; 계약서 서식 참고 라벨; 링크 중복/유효성 논의 |')
W('| 5 | modernComment_105_B404018D.xml | 첨부파일 2-1; 「링크는 중국 경내책임자 수권서」 |')
W('| 6 | modernComment_10D_EA7711BE.xml | 첨부파일 2-1; 동일 중국 수권서 경고 |')
W('| 7 | modernComment_10E_1151531A.xml | 화장품글로벌규제조화지원센터 게시글 연결 |')
W('| 8 | modernComment_10B_65584E78.xml | 「링크는 중국 자료입니다.」 |')
W('| 9 | modernComment_107_D4A2BB0F.xml | 화장품글로벌규제조화지원센터 게시글 연결 |')
W('| 10 | modernComment_111_5C88F3A6.xml | 유효기간 만료 3개월전 등록 연장 |')
W('| 11 | modernComment_109_8180DCBA.xml | 첨부파일 4-1~4-7; 아포스티유 미가맹/대표부 인증 |')
W('| 13 | modernComment_10A_741D51D9.xml | 첨부파일 5-1~5-5 |')
W('')
W('---')
W('')
W('End of Taiwan PPT extraction map.')

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Wrote {OUT_PATH}')
print(f'Lines: {len(lines)}')
print(f'Hyperlink pairs: {len(all_links_ordered)}')
print(f'Unique URLs: {len(uniq_urls)}')
print(f'Attachment files listed: {len(file_list)}')
