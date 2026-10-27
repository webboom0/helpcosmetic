# -*- coding: utf-8 -*-
from .shell import COUNTRY_TABS, ICO, dl, lex, step_nav

KITA_CONTRACT = "https://www.kita.net/board/format/formatDetail.do?postIndex=1863913"
TIPO_SEARCH = "https://cloud.tipo.gov.tw/S282/S282WV1/"

BODY = f"""{COUNTRY_TABS}
{step_nav(1)}
          <h3 class="law-sub-tit">수출계약</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">설명 또는<br>정의</th>
                  <td>대만 수출을 위해 수출자와 대만 구매자 또는 수입자 간 제품, 가격, 수량, 결제조건, 인도조건, 납기, 통관·인허가 책임 등 주요 거래조건을 확정하는 단계</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">계약 방식</th>
                  <td>{lex(KITA_CONTRACT, "수출계약서")}, 발주서(PO), 주문확인서, 견적송장/형식송장(Proforma Invoice) 등을 통해 거래조건 확정</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">관련 기관</th>
                  <td>
                    <p><strong>국내 (계약 서식·보험·중재):</strong></p>
                    <ul>
                      <li>한국무역협회(KITA) / 통합무역정보서비스(TradeNAVI) / KOTRA: 표준 수출계약서 서식 제공 및 법률 자문 지원</li>
                      <li>한국무역보험공사(K-SURE): 대금 미회수 리스크 대비 무역보험/신용보증 가입</li>
                      <li>대한상사중재원(KCAB): 수출계약 분쟁 발생 시 중재 관할 기관</li>
                    </ul>
                    <p><strong>대만 (상표 출원 주무관청):</strong> 대만 경제부 지혜재산국(TIPO) - 대만 현지 상표(영문·중문·로고) 출원 및 심사 관할</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">계약서 서식<br>참고</th>
                  <td>
                    <p>{ICO} {lex(KITA_CONTRACT, "한국무역협회")}</p>
                    <ul class="law-file-list">
                      <li>{dl("files/taiwan/tw-1-1-export-agency-ko.pdf", "수출대행계약서(국문)")}</li>
                      <li>{dl("files/taiwan/tw-1-1-export-agency-en.pdf", "수출대행계약서(영문)")}</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">절차</th>
                  <td>① 대만 거래상대방 및 수입업자 정보 확인 → ② 제품의 대만 수입 가능 여부, HS Code, 관세율, 수입규제, 인증·허가·라벨링 요건 확인 → ③ 제품명·브랜드명·규격·수량·단가·통화 확정 → ④ 결제조건·Incoterms·선적조건·납기 확정 → ⑤ 수입허가·라벨링·통관 책임 주체 확인 → ⑥ 발주서(PO)/견적송장 또는 형식송장 확인 → ⑦ 수출계약 체결 → ⑧ 계약내용과 상업송장·포장명세서 기재정보의 정합성 확인</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항<br>또는<br>확인사항</th>
                  <td>
                    <ul>
                      <li>계약상 매수인, 수하인, 대만 수입업자 정보 구분 및 정합성 확인 필요.</li>
                      <li>제품명, 브랜드명, 규격, 수량, 단가 등 계약정보와 상업송장·포장명세서 기재정보 일치 필요. Incoterms 2020 기준 비용·위험 이전 시점 명확화 필요.</li>
                      <li>결제조건, 납기, 운송방식, 클레임 처리 기준 명확화 필요. 대만 수입허가, 인증, 라벨링 및 통관 책임 주체를 계약 단계에서 확인 필요.</li>
                      <li>현지 수입업자 또는 대리점의 상표 임의 출원을 방지하기 위해 상표권 귀속 및 사용제한 조항 검토 필요.</li>
                      <li>신규 거래처는 선금, 신용장, 지급보증, 무역보험 등 대금 회수 안전장치 검토 필요.</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 class="law-sub-tit">상표등록</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">설명 또는<br>정의</th>
                  <td>
                    <p>대만은 ‘선출원주의’를 채택하고 있어 동일·유사 상표가 먼저 출원될 경우 후출원자의 등록이 제한될 수 있음. 화장품 수출 전 브랜드명, 로고, 중문명에 대한 사전 출원이 권장됨.</p>
                    <p>대만 내 브랜드명, 로고, 제품명 등에 대한 상표권을 확보하고 현지 제3자 또는 거래상대방의 상표 선점을 방지하기 위해 선행상표 검색 및 상표출원을 검토하는 단계</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">방식</th>
                  <td>대만 경제부 지혜재산국, TIPO에 선행상표 검색 후 상표출원. 필요 시 현지 대리인을 통해 진행</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">기관</th>
                  <td>대만 경제부 지혜재산국(TIPO, Taiwan Intellectual Property Office / 經濟部智慧財產局)</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">참고 또는<br>필요서류</th>
                  <td>
                    <p>대만은 마드리드 국제상표 출원의 지정국이 아니므로 TIPO에 개별 출원 필요</p>
                    <p><strong>[필요 서류]</strong></p>
                    <ul>
                      <li>출원인 정보</li>
                      <li>상표 견본</li>
                      <li>지정상품·서비스 목록</li>
                      <li>법인 또는 사업자 정보</li>
                      <li>위임장, 대리인을 선임하는 경우(출원일로부터 3개월 이내)</li>
                      <li>우선권 주장서류, 해당 시</li>
                      <li>중문 상표명 후보, 해당 시</li>
                      <li>실제 판매 제품 목록 또는 제품 카테고리</li>
                      <li>기존 한국 또는 해외 상표등록증, 참고용</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">절차</th>
                  <td>
                    <p>① 수출 제품 및 사용 상표 확정 → ② 영문·한글·중문 브랜드명 및 로고 검토 → ③{lex(TIPO_SEARCH, "대만 내 선행 상표 검색")} → ④ 지정상품·서비스류 확정 → ⑤ 출원인 명의 및 대리인 선임 여부 결정 → ⑥ TIPO 상표출원 → ⑦ 심사 및 보정 대응 → ⑧ 공고 및 이의신청 기간 경과 → ⑨ 등록 및 갱신기한 관리</p>
                    <p class="law-hint">{ICO} 예상 소요기간: 통상 출원부터 등록까지 약 8~12개월 내외 소요될 수 있으며, 보정·거절이유 통지·이의신청 발생 시 기간이 연장될 수 있음</p>
                    <p class="law-hint">{ICO} 상표권 존속기간은 등록 후 10년이며, 만료 전 6개월 이내 갱신 신청 가능</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항<br>또는<br>확인사항</th>
                  <td>
                    <ul>
                      <li>한국 또는 다른 국가에 등록된 상표라도 대만에서 자동으로 보호되는 것은 아니므로, 대만 내 별도 상표출원 필요 여부 확인 필요</li>
                      <li>현지 수입업자, 대리점, 총판 명의로 상표를 출원할 경우 계약 종료 후 분쟁이 발생할 수 있으므로 브랜드 권리자 명의 출원 권장</li>
                      <li>영문 브랜드명뿐 아니라 중문 브랜드명, 음역명, 의역명, 로고, 제품명도 별도 보호 필요성 검토</li>
                      <li>수출계약, 총판계약 또는 대리점계약에 상표권 귀속, 사용허락 범위, 계약 종료 후 상표 사용중지 조항 반영 필요</li>
                      <li>등록상표가 정당한 사유 없이 3년 이상 사용되지 않을 경우 불사용 취소 대상이 될 수 있으므로, 등록 후 실제 사용 및 사용증거 관리 필요</li>
                      <li>화장품 관련 TFDA 절차는 상표등록 완료가 일반적으로 필수 요건은 아니므로, 상표출원 후 TFDA 관련 제품등록·신고 절차를 병행할 수 있음</li>
                      <li>등록 후에도 갱신기한 및 유사상표 모니터링 필요</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <a class="law-back" href="law-export-tw.html"><i class="ri-arrow-left-line" aria-hidden="true"></i> 전체 수출절차로 돌아가기</a>"""
