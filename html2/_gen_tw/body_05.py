# -*- coding: utf-8 -*-
from .shell import COUNTRY_TABS, ICO, dl, lex, step_nav

U_INV = "https://www.kita.net/board/format/formatDetail.do?postIndex=1720212"
U_PL = "https://www.kita.net/board/format/formatDetail.do?postIndex=1863940"
U_BL = "https://kcia.or.kr/home/law/%EC%84%A0%ED%95%98%EC%A6%9D%EA%B6%8C.pdf"
U_AWB = "https://www.kita.net/board/format/formatDetail.do?postIndex=1719028&ContentsID=KI_cmmrcFormat_1719028&query=AWB"
U_IMPORT = "https://web.customs.gov.tw/en/singlehtml/3333?cntId=ef481d6f272c42ac98dca2c33502bb7c"
U_CFS = "https://kcia.or.kr/cert/main/"

BODY = f"""{COUNTRY_TABS}
{step_nav(5)}
          <h3 class="law-sub-tit">현지통관</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">설명 또는<br>정의</th>
                  <td>대만으로 수입되는 화장품에 대해 대만 내 수입업자 또는 통관업자가 수입신고를 진행하고, 대만 세관의 서류심사·검사·과세 및 통관절차를 거쳐 반출하는 단계</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">방식</th>
                  <td>대만 내 수입업자 또는 그 위임을 받은 통관업자가 대만 세관 전자통관시스템을 통해 수입신고를 진행하며, 세관의 위험분류에 따라 C1·C2·C3 방식으로 통관 처리</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">기관</th>
                  <td>대만 재정부 관무서 (Customs Administration)</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">참고 또는<br>필요서류</th>
                  <td>
                    <p><strong>[수입신고 시 기본 서류]</strong></p>
                    <ul>
                      <li>{lex(U_INV, "상업송장")} (Commercial Invoice) — {dl("files/taiwan/tw-5-1-commercial-invoice.pdf", "상업송장")} {dl("files/taiwan/tw-4-guide-commercial-invoice.hwp", "상업송장 기재요령", "HWP")}</li>
                      <li>{lex(U_PL, "포장명세서")} (Packing List) — {dl("files/taiwan/tw-5-2-packing-list.pdf", "포장명세서")} {dl("files/taiwan/tw-4-guide-packing-list.xlsx", "포장명세서 양식", "XLSX")}</li>
                      <li>{lex(U_BL, "선하증권")} (B/L) — {dl("files/taiwan/tw-5-3-bl.pdf", "선하증권")} 또는 {lex(U_AWB, "항공장화물운송")} (AWB) — {dl("files/taiwan/tw-5-4-awb.pdf", "항공화물 운송장")} {dl("files/taiwan/tw-4-guide-awb.hwp", "항공화물운송장 기재요령", "HWP")}</li>
                      <li>제품 등록번호 및 등록정보</li>
                      <li>중문 라벨 자료</li>
                      <li>{lex(U_IMPORT, "수입신고서")} (Import Declaration) — {dl("files/taiwan/tw-5-5-import-declaration.pdf", "수입신고서")}</li>
                    </ul>
                    <p><strong>[필요 시 제출서류]</strong></p>
                    <ul>
                      <li>무역계약서 (Sales Contract)</li>
                      <li>제품정보파일, PIF 관련 자료, TFDA 또는 세관 요청 시</li>
                      <li>시험성적서 또는 안전성 관련 자료, 요청 시</li>
                      <li>{lex(U_CFS, "자유판매증명서")} (CFS)</li>
                      <li>{lex(U_CFS, "원산지증명서")}, 요청 시 또는 관세 적용상 필요 시</li>
                      <li>기타 세관 또는 관계기관 요청자료</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">절차</th>
                  <td>① 수입신고 → ② 세관심사, C1·C2·C3 → ③ 필요 시 서류보완 또는 실물검사 → ④ 관세·부가세 등 세금 납부 → ⑤ 통관 및 반출 → ⑥ 대만 내 유통</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항<br>또는<br>확인사항</th>
                  <td>
                    <ul>
                      <li>상업송장, 포장명세서, B/L 또는 AWB의 제품명, 수량, 중량, 제조소, 수입업자 정보가 실제 수입제품 및 등록정보와 일치해야 함</li>
                      <li>중문 표시사항, 라벨, 제품 외관 및 포장정보의 적합성 확인 필요</li>
                      <li>제품명, 성분, 제조소, 원산지, 용량 등 제품정보와 실제 수입제품의 일치 여부 확인 필요</li>
                      <li>세관 또는 관계기관 요청 시 제품 등록정보, 라벨, 시험성적서, CFS, PIF 관련 자료 등 증빙자료 제출 가능해야 함</li>
                      <li>HS Code, 과세가격, 원산지, 수량, 포장단위 등 통관신고 정보의 정합성 확인 필요</li>
                      <li>통관 보류, 검사, 서류보완 요청 발생 시 대만 내 수입업자와 제조사 간 신속한 자료제공 체계 필요</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">세부 통관<br>절차</th>
                  <td>
                    <p><strong>수입신고</strong></p>
                    <ul>
                      <li>대만 내 수입업자 또는 수입업자가 수입신고 진행</li>
                      <li>등록번호 및 제품정보 제출</li>
                      <li>관세 및 부가세 납부</li>
                    </ul>
                    <p><strong>세관심사</strong></p>
                    <ul>
                      <li>C1: 서류심사·검사 면제 또는 간이심사</li>
                      <li>C2: 서류심사</li>
                      <li>C3: 서류심사 + 실물검사</li>
                    </ul>
                    <p><strong>화물검사 (필요 시)</strong></p>
                    <ul>
                      <li>제품 표시사항 확인</li>
                      <li>제품 외관 확인</li>
                      <li>중문 라벨 적합성 검토</li>
                      <li>필요 시 샘플 검사 또는 추가자료 요청</li>
                    </ul>
                    <p><strong>통관 및 반출</strong></p>
                    <ul>
                      <li>세관 심사 완료 후 반출</li>
                      <li>대만 내 유통 가능</li>
                    </ul>
                    <p><strong>사후심사</strong></p>
                    <ul>
                      <li>세관이 가격, 품목분류, 원산지 등을 사후 검토할 수 있음</li>
                      <li>허위신고 또는 자료 불일치 적발 시 보정, 과태료, 추징 등 행정처분 가능</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 class="law-sub-tit">시판 후 관리</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">설명 또는<br>정의</th>
                  <td>화장품 판매 이후 TFDA 등 관할기관이 실시하는 시장감시, 표시·광고 점검, 안전성 확인, 이상사례 관리 및 회수 등 사후관리 제도</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">방식</th>
                  <td>제품 출시 후 대만 내 수입업자 또는 책임주체가 PIF, 제품 등록정보, 공급원·유통흐름 자료, 시험자료 및 이상사례 자료를 보관하고, TFDA의 시장감시·표시사항 점검·샘플링 검사·자료요청에 대응</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">기관</th>
                  <td>대만 위생복리부 식품약물관리서 (TFDA) 필요 시 지방 보건당국 및 세관</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">참고 또는<br>필요서류</th>
                  <td>
                    <ul>
                      <li>제품정보파일 (PIF)</li>
                      <li>안전성 평가 보고서 (Safety Assessment Report)</li>
                      <li>제품 등록정보 및 등록번호</li>
                      <li>제품 라벨, 포장 및 광고·홍보 자료</li>
                      <li>시험성적서, 미생물·보존력·안정성 자료 등</li>
                      <li>공급원 및 유통흐름 자료, 판매·출하 기록</li>
                      <li>이상사례, 소비자 불만 및 회수 관련 자료</li>
                      <li>제품 변경 이력 및 PIF 업데이트 기록</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">절차</th>
                  <td>① 시장감시 또는 자료요청 → ② 제품 수거 또는 샘플링 → ③ 표시사항·광고·라벨 점검 → ④ 시험검사 → ⑤ PIF 및 제품 등록정보 확인 → ⑥ 필요 시 시정명령, 판매중지, 회수 또는 행정처분</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항<br>또는<br>확인사항</th>
                  <td>
                    <ul>
                      <li>PIF는 대만 내 수입업자 또는 책임주체 소재지에 상시 보관해야 함</li>
                      <li>TFDA 요청 시 정해진 기한 내 PIF 및 관련 자료를 제출할 수 있어야 함</li>
                      <li>제품 등록정보, 라벨, PIF, 실제 판매제품 및 광고문구 간 정합성 유지 필요</li>
                      <li>이상사례, 소비자 불만, 품질문제 발생 시 평가·기록·보고 및 회수 대응 절차를 갖추어야 함</li>
                      <li>제품 정보, 성분, 제조소, 라벨, 포장, 광고문구 변경 시 등록정보 및 PIF 업데이트 필요</li>
                      <li>판매·출하 기록 및 유통흐름 자료를 보관하여 회수 발생 시 추적 가능해야 함</li>
                      <li>온라인몰, SNS, 인플루언서 광고 등 판매채널의 표시·광고 문구도 화장품 규정 준수 여부 확인 필요</li>
                      <li>안전성 평가 보고서, 시험성적서 등 주요 자료가 최신 상태인지 정기적으로 검토 필요</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">TFDA 주요<br>점검 항목</th>
                  <td>
                    <p><strong>표시사항 점검</strong></p>
                    <ul>
                      <li>제품명</li>
                      <li>대만 내 수입업자 또는 책임주체 정보</li>
                      <li>제조업체 정보 및 제조소 정보</li>
                      <li>전성분</li>
                      <li>내용량 또는 용량</li>
                      <li>제조번호 또는 로트번호</li>
                      <li>사용기한 또는 유통기한</li>
                      <li>사용방법 및 사용상 주의사항</li>
                      <li>원산지, 필요 시</li>
                      <li>효능·효과, 기능성 표현 및 광고문구의 적합성</li>
                    </ul>
                    <p><strong>제품 수거검사</strong></p>
                    <ul>
                      <li>미생물 기준</li>
                      <li>중금속 기준</li>
                      <li>금지성분 함유 여부</li>
                      <li>사용제한 성분 기준</li>
                      <li>보존제, 색소, 자외선차단제 등 허용성분 기준</li>
                      <li>표시사항과 실제 제품 성분의 일치 여부</li>
                      <li>제품 품질, 안정성 및 안전성 관련 시험자료 확인</li>
                    </ul>
                    <p><strong>PIF 점검</strong></p>
                    <ul>
                      <li>안전성 평가자료 보유 여부</li>
                      <li>원료 안전성 자료 보유 여부</li>
                      <li>시험성적서, 안정성·보존력 자료 보유 여부</li>
                      <li>제품 등록정보, 라벨, PIF 및 실제 판매제품 간 정합성</li>
                      <li>제품 변경사항 반영 및 최신 정보 유지 여부</li>
                    </ul>
                    <p><strong>행정조치 대응체계</strong></p>
                    <ul>
                      <li>이상사례 및 소비자 불만 접수·평가·기록 체계</li>
                      <li>판매·출하 기록 및 유통흐름 추적 가능 여부</li>
                      <li>회수 절차 및 책임자 지정 여부</li>
                      <li>수입업자, 제조사, 브랜드사 간 자료제공 및 비상연락 체계</li>
                    </ul>
                    <p><strong>행정조치</strong></p>
                    <ul>
                      <li>시정명령</li>
                      <li>판매중지 또는 판매금지</li>
                      <li>회수명령</li>
                      <li>제품 폐기 또는 개선명령</li>
                      <li>과태료 부과 또는 벌금 부과</li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <a class="law-back" href="law-export-tw.html"><i class="ri-arrow-left-line" aria-hidden="true"></i> 전체 수출절차로 돌아가기</a>"""
