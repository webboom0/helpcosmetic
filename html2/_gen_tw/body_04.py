# -*- coding: utf-8 -*-
from .shell import COUNTRY_TABS, ICO, dl, lex, step_nav

U_DECL = "https://www.kita.net/board/format/formatDetail.do?postIndex=1863914"
U_INV = "https://www.kita.net/board/format/formatDetail.do?postIndex=1720212"
U_PRO = "https://www.kita.net/board/format/formatDetail.do?postIndex=1863877"
U_PL = "https://www.kita.net/board/format/formatDetail.do?postIndex=1863940"
U_BL = "https://kcia.or.kr/home/law/%EC%84%A0%ED%95%98%EC%A6%9D%EA%B6%8C.pdf"
U_AWB = "https://www.kita.net/board/format/formatDetail.do?postIndex=1719028&ContentsID=KI_cmmrcFormat_1719028&query=AWB"
U_CFS = "https://kcia.or.kr/cert/main/"
U_OTHER = "https://kcia.or.kr/home/law/%EA%B8%B0%ED%83%80%20%EC%88%98%EC%B6%9C%ED%86%B5%EA%B4%80%EC%97%90%20%ED%95%84%EC%9A%94%ED%95%9C%20%EC%84%9C%EB%A5%98.pdf"
U_CLIP = "https://unipass.customs.go.kr/clip/index.do"

BODY = f"""{COUNTRY_TABS}
{step_nav(4)}
          <h3 class="law-sub-tit">수출통관</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">설명 또는<br>정의</th>
                  <td>
                    <p>수출통관: 한국에서 대만으로 수출되는 화장품에 대해 관세청에 수출신고를 진행하고 수출신고 수리를 받는 절차</p>
                    <p>선적: 수출신고 수리 후 화물을 선박 또는 항공기에 적재하여 대만으로 운송하는 절차</p>
                    <p>자유판매증명서(CFS): 대만 바이어 또는 대만 내 수입업자가 요구하는 경우 국내에서 정상적으로 판매 가능한 제품임을 증명하기 위해 발급받는 서류</p>
                    <p class="law-hint">{ICO} 대만은 아포스티유 미가맹국이므로, 대만 세관/TFDA 또는 바이어가 공증 서류를 요구할 경우 [외교부 영사확인 → 주한국타이페이대표부 인증] 절차를 거쳐 제출</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">방식</th>
                  <td>한국 관세청 전자통관시스템, UNI-PASS를 통한 전자 수출신고 후 수출신고 수리일로부터 30일 이내 해상운송, B/L 또는 항공운송, AWB 방식으로 대만행 화물 선적</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">기관</th>
                  <td>
                    <ul>
                      <li>관세청 및 지역본부세관</li>
                      <li>대한화장품협회(KCA), CFS 등 화장품 관련 증명서 발급 시</li>
                      <li>선사, 항공사, 포워더, 관세사</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">참고 또는<br>필요서류</th>
                  <td>
                    <p><strong>[수출 신고 시 제출 서류]</strong></p>
                    <ul>
                      <li>{lex(U_DECL, "수출 신고서")} — {dl("files/taiwan/tw-4-1-export-declaration.pdf", "수출신고서, 수출신고필증")}</li>
                      <li>송장
                        <ul>
                          <li>{lex(U_INV, "상업 송장")} — {dl("files/taiwan/tw-4-2-commercial-invoice.pdf", "상업송장")}</li>
                          <li>{lex(U_PRO, "견적 송장")} — {dl("files/taiwan/tw-4-3-proforma-invoice.pdf", "견적송장")}</li>
                        </ul>
                      </li>
                      <li>{lex(U_PL, "포장명세서")} — {dl("files/taiwan/tw-4-4-packing-list.pdf", "포장명세서")}</li>
                      <li>{lex(U_BL, "선하증권")} (B/L) — {dl("files/taiwan/tw-4-5-bl.pdf", "선하증권")} 또는 {lex(U_AWB, "항공화물운송장")} (AWB) — {dl("files/taiwan/tw-4-6-awb.pdf", "항공화물 운송장")}</li>
                      <li>{lex(U_CFS, "자유판매증명서")} (CFS) (필요 시)</li>
                      <li>{lex(U_CFS, "원산지증명서")} (거래조건에 따라 필요)</li>
                      <li>{lex(U_OTHER, "기타 수출통관에 필요한 서류")} — {dl("files/taiwan/tw-4-7-customs-docs.pdf", "기타 수출통관에 필요한 서류")}</li>
                      <li>{lex(U_CLIP, "관세율 조회 사이트")}</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">절차</th>
                  <td>① 선적 전 제품 등록정보, 라벨, 수입업자 정보 확인 → ② 수출서류 작성, 상업송장·포장명세서 등 → ③ UNI-PASS 수출신고 → ④ 수출신고 수리 → ⑤ 선사·항공사 또는 포워더 부킹 → ⑥ 화물 반입 및 선적 → ⑦ B/L 또는 AWB 발급 → ⑧ 대만 수입업자에게 통관서류 송부</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항<br>또는<br>확인사항</th>
                  <td>
                    <ul>
                      <li>제품 등록 완료 여부 또는 대만 내 판매 가능 상태를 확인한 후 선적 진행</li>
                      <li>상업송장, 포장명세서, B/L 또는 AWB 등 선적서류의 제품명, 수량, 중량, 제조소, 수입업자 정보가 제품 등록정보 및 실제 제품과 일치해야 함</li>
                      <li>대만 내 수입업자, 수하인, 통지처, 실제 구매자 정보가 정확하게 기재되어야 함</li>
                      <li>자유판매증명서, CFS, 원산지증명서 등 바이어 또는 대만 수입통관에서 요구하는 서류를 사전에 확인할 것</li>
                      <li>Incoterms 조건에 따라 운임, 보험, 수입통관, 관세·세금 부담 주체를 명확히 확인할 것</li>
                      <li>제품 라벨의 번체중문 표시사항이 대만 등록정보와 일치하는지 선적 전 확인 필요</li>
                      <li>HS Code, 수출신고 가격, 통화, 원산지, 포장단위 등 통관정보의 정합성 확인 필요</li>
                      <li>수출신고 수리 후 30일 이내 선적 원칙을 준수하고, 지연 시 정정 또는 취하 필요 여부를 관세사와 확인할 것</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <a class="law-back" href="law-export-tw.html"><i class="ri-arrow-left-line" aria-hidden="true"></i> 전체 수출절차로 돌아가기</a>"""
