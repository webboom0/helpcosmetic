# -*- coding: utf-8 -*-
import pathlib
import re
p = pathlib.Path(r'e:\SynologyDrive\working\2026\화장품글로벌규제조화지원센터\html2\_ppt_tw_map.txt')
t = p.read_text(encoding='utf-8')
print('bytes', p.stat().st_size)
print('chars', len(t))
print('has HLINK master', 'External hyperlinks (complete master list)' in t)
print('has raw dump', 'Raw slide text dump' in t)
print('slide markers', t.count('===== SLIDE'))
urls = re.findall(r'`(https?://[^`]+)`', t)
# from master table only roughly
print('backticked http urls (all sections)', len(urls))
print('unique urls sample count', len(set(urls)))
# Check required anchors
required = [
    'https://www.kita.net/board/format/formatDetail.do?postIndex=1863913',
    'https://cloud.tipo.gov.tw/S282/S282WV1/',
    'https://www.fda.gov.tw/ENG/siteListContent.aspx?sid=10334&id=41180',
    'https://cos.fda.gov.tw/TCAL/',
    'https://unipass.customs.go.kr/clip/index.do',
    'https://web.customs.gov.tw/en/singlehtml/3333?cntId=ef481d6f272c42ac98dca2c33502bb7c',
    'https://kcia.or.kr/inc/down.php?dir=BOARD&file_name=202310_169640754590651_1.docx&rename=%ED%99%94%EC%9E%A5%ED%92%88+%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4+%EB%AC%B8%EC%84%9C%EC%9E%91%EC%84%B1+%EB%A7%A4%EB%89%B4%EC%96%BC_%EA%B5%AD%EB%AC%B8.docx',
]
for u in required:
    print('OK' if u in t else 'MISSING', u[:80])
print('--- first 60 lines ---')
print('\n'.join(t.splitlines()[:60]))
