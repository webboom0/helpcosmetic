# -*- coding: utf-8 -*-
from .shell import COUNTRY_TABS, lex, step_nav

LAW = "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5668&page=1&code=foreign&searchopt=&searchkey=%EC%9C%84%EC%83%9D%EC%95%88%EC%A0%84"
TCAL = "https://cos.fda.gov.tw/TCAL/"

BODY = f"""{COUNTRY_TABS}
{step_nav(3)}
          <h3 class="law-sub-tit">제품 등록</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">설명 또는<br>정의</th>
                  <td>대만은 『{lex(LAW, "화장품위생안전관리법")}』에 따라 화장품의 시판 전 제품정보 등록제도를 운영하고 있으며, 대만 내 수입업자 또는 책임주체가 TFDA 시스템에 제품정보를 등록·관리해야 함</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">방식</th>
                  <td>{lex(TCAL, "TFDA 온라인 시스템을 통한 제품정보 등록")} (Online Registration)</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">기관</th>
                  <td>대만 위생복리부 식품약물관리서 (TFDA, Taiwan Food and Drug Administration)</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">참고 또는<br>필요서류</th>
                  <td>
                    <p><strong>[제품 등록 필요서류]</strong></p>
                    <ol>
                      <li>제품명, 중문·영문</li>
                      <li>제품 유형 및 용도</li>
                      <li>전성분 정보, INCI명, 함량 또는 함량범위, 제한성분 해당 여부</li>
                      <li>제조업체 및 제조소 정보</li>
                      <li>대만 내 수입업자 또는 책임주체 정보</li>
                      <li>제품 라벨 및 표시사항 정보</li>
                      <li>제품정보파일, PIF, 또는 PIF 구축 확인자료</li>
                      <li>GMP 또는 ISO 22716 관련 자료, 해당 시 또는 적용 대상 제품</li>
                      <li>제품 사진 또는 포장 도안, 필요 시</li>
                      <li>기타 TFDA 시스템 입력 또는 확인에 필요한 자료</li>
                    </ol>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">절차</th>
                  <td>① 대만 내 수입업자 또는 책임주체 TFDA 계정 로그인 → ② 제품 기본정보, 성분, 제조소, 라벨 정보 입력 → ③ PIF 구축 여부 및 관련 정보 확인 → ④ 등록 수수료 납부 → ⑤ 등록번호 발급 → ⑥ 등록정보와 실제 판매제품, 라벨, PIF 정합성 확인 → ⑦ 제품 판매</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">소요기간</th>
                  <td>등록정보 제출 및 수수료 납부 후 시스템 처리 기준으로 등록번호가 발급될 수 있음. 단, 자료 준비, 계정 개설, 입력정보 검토, 수수료 처리 상황에 따라 실제 준비기간은 달라질 수 있음</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">등록<br>유효기간</th>
                  <td>등록일로부터 3년 (유효기간 만료 3개월 전 등록 연장 필요)</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">등록 수수료</th>
                  <td>제품당 NT$800 (2026.07.01 이후) 단, 최신 TFDA 고시 또는 시스템 기준 확인 필요</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항<br>또는<br>확인사항</th>
                  <td>
                    <ul>
                      <li>대만은 기존 특정용도화장품 허가제를 폐지하고 모든 화장품에 대해 제품정보 등록제도를 운영함</li>
                      <li>제품 등록은 사전 심사·허가가 아니라 TFDA 시스템상 제품정보 등록 성격이므로, 등록정보의 정확성과 사후 점검 대응이 중요함</li>
                      <li>제품 등록 전 또는 늦어도 제품 시판 전 PIF 구축·보관이 완료되어야 함</li>
                      <li>등록정보, 전성분, 라벨, 제조소 정보 및 PIF 내용은 실제 판매제품과 일치해야 함</li>
                      <li>등록정보 변경 시 수정 등록이 필요하며, 전성분 변경 등 제품 동일성에 영향을 주는 변경은 재등록 필요 여부를 검토해야 함</li>
                      <li>등록 유효기간 만료 전 갱신 필요, 만료 3개월 전 갱신기한 관리 권장</li>
                      <li>수입업자 또는 책임주체 변경 시 등록정보 이전 또는 재등록 필요 여부를 사전에 확인해야 함</li>
                      <li>제품명, 효능·효과 표현 및 광고 문구가 화장품 범위를 벗어나 의약품적 효능으로 해석되지 않도록 확인 필요</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <a class="law-back" href="law-export-tw.html"><i class="ri-arrow-left-line" aria-hidden="true"></i> 전체 수출절차로 돌아가기</a>"""
