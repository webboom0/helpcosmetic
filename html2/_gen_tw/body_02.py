# -*- coding: utf-8 -*-
from .shell import COUNTRY_TABS, ICO, dl, lex, step_nav

FDA_AUTH = "https://www.fda.gov.tw/ENG/siteListContent.aspx?sid=10334&id=41180"
LAW = "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5668&page=1&code=foreign&searchopt=&searchkey=%EC%9C%84%EC%83%9D%EC%95%88%EC%A0%84"
PIF1 = "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5629&page=1&code=foreign&searchopt=&searchkey=%EB%A7%A4%EB%89%B4%EC%96%BC"
PIF2 = "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5630&page=1&code=foreign&searchopt=&searchkey=%ED%99%94%EC%9E%A5%ED%92%88%20%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4%20%EB%AC%B8%EC%84%9C%EC%9E%91%EC%84%B1%20%EB%A7%A4%EB%89%B4%EC%96%BC"
PIF_EX = "https://helpcosmetic.or.kr/pc/license/license02.php?ptype=view&idx=5823&page=1&code=foreign&searchopt=&searchkey=%ED%99%94%EC%9E%A5%ED%92%88%20%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4%20%EB%AC%B8%EC%84%9C"
PIF_DOCX = "https://kcia.or.kr/inc/down.php?dir=BOARD&file_name=202310_169640754590651_1.docx&rename=%ED%99%94%EC%9E%A5%ED%92%88+%EC%A0%9C%ED%92%88%EC%A0%95%EB%B3%B4+%EB%AC%B8%EC%84%9C%EC%9E%91%EC%84%B1+%EB%A7%A4%EB%89%B4%EC%96%BC_%EA%B5%AD%EB%AC%B8.docx"

BODY = f"""{COUNTRY_TABS}
{step_nav(2)}
          <h3 class="law-sub-tit">대만 내 수입업자 선임</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">대리인 역할</th>
                  <td>
                    <ol>
                      <li>TFDA 시스템상 제품 등록·신고 및 제품정보 관리</li>
                      <li>PIF 구축 자료 수집·검토, 대만 내 보관 및 TFDA 요청 시 제출 대응</li>
                      <li>제품 표시사항, 라벨 및 광고·홍보 문구의 적합성 관리</li>
                      <li>이상사례 수집·평가·보고, 제품 회수·소비자 공지 등 시판 후 안전관리</li>
                      <li>TFDA 감독·점검 및 조사 대응, 관련 자료 제출 협조</li>
                    </ol>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">대리인<br>자격 요건</th>
                  <td>
                    <ol>
                      <li>대만 내 관련 법령에 따라 설립·등록된 법인 또는 사업자일 것</li>
                      <li>화장품 수입·유통 또는 관련 영업 범위를 보유할 것</li>
                      <li>TFDA 시스템 계정 개설 및 제품 등록·신고, 자료 관리가 가능할 것</li>
                      <li>대만 내 연락 가능한 담당자와 PIF 보관·제출 대응 체계를 갖출 것</li>
                      <li>이상사례, 회수, 소비자 불만 등 시판 후 관리 대응이 가능할 것</li>
                    </ol>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">선정 요령/<br>체크포인트</th>
                  <td>
                    <p><strong>[대만지사(자사 법인)]</strong><br>등록정보, PIF, 라벨, 광고, 사후관리 권한을 직접 통제 가능하나 설립·운영비 및 현지 규제 대응 인력 필요</p>
                    <p><strong>[수입·유통업체]</strong><br>초기 진입과 유통망 확보에 유리하나 제품 등록정보, PIF, 고객·유통채널 권한이 수입업체에 집중될 수 있으므로 계약상 권한·이전 조건 명확화 필요</p>
                    <p><strong>[규제 대행사(전문 컨설팅/대행 업체)]</strong><br>전문성·보안성은 높을 수 있으나 실제 수입자 또는 제품 책임주체 역할 수행 가능 여부, 물류·통관·판매 역할 분리 여부 확인 필요</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">수권 계약서</th>
                  <td>
                    <p>{lex(FDA_AUTH, "화장품 수입업자 위임계약서 또는 수권서")}</p>
                    <p>{dl("files/taiwan/tw-2-1-importer-auth.pdf", "화장품 수입업자 위임계약서 또는 수권서")}</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항</th>
                  <td>
                    <ul>
                      <li>대만 내 수입업자 선임 전 역할·권한·비용·계약 해지 조건 등을 명확히 계약서에 기재할 것</li>
                      <li>TFDA 시스템 계정, 제품 등록·신고 정보 및 PIF 접근권한을 사전에 확인할 것</li>
                      <li>PIF에는 제조공정, 성분자료 등 영업비밀이 포함될 수 있으므로 접근권한, 열람범위, 비밀유지의무를 계약서에 명시할 것</li>
                      <li>동일 제품을 여러 수입업체가 판매할 수 있으므로 각 대만 내 수입업자의 책임 범위를 명확히 설정할 것</li>
                      <li>대만 내 수입업자 변경 시 제품 등록 및 관리정보 이전 가능 여부를 사전에 검토할 것</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">필요서류</th>
                  <td>
                    <ol>
                      <li>{lex(FDA_AUTH, "화장품 대만 내 수입업자 위임계약서 또는 수권서")} / {dl("files/taiwan/tw-2-1-importer-auth.pdf", "수권서 양식")}</li>
                      <li>대만 내 수입업자 회사설립등기자료, 사업자등록 또는 상업등기 관련 서류</li>
                      <li>대만 내 수입업자 회사 기본정보, 회사명, 주소, 연락처, 담당자 정보</li>
                      <li>TFDA 시스템 계정 신청자료</li>
                      <li>대만 내 수입업자 법인 대표자 또는 등록 담당자 신분증 사본</li>
                      <li>수입업 허가 또는 관련 영업등록 서류, 해당 시</li>
                      <li>브랜드사 또는 제조사 위임장, 필요 시</li>
                      <li>PIF 보관장소 및 접근권한 확인자료, 필요 시</li>
                    </ol>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">소요기간</th>
                  <td>약 1~2주 소요, 단 대만 내 수입업자 확정 및 계약조건 합의가 완료된 경우 기준. 신규 수입업자 발굴, 계약 협상, TFDA 계정 개설 상황에 따라 기간 연장 가능</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 class="law-sub-tit">PIF 준비</h3>
          <div class="law-table-wrap">
            <table class="law-table">
              <tbody>
                <tr>
                  <th class="row-head" scope="row">PIF 개요</th>
                  <td>
                    <p>대만 『{lex(LAW, "화장품위생안전관리법")}』에 따라 화장품의 안전성 및 품질을 입증하기 위해 구축·보관해야 하는 기술문서로, 제품 등록·신고, TFDA 점검 대응 및 시판 후 관리의 기초 자료로 활용됨.</p>
                    <ul>
                      <li>{lex(PIF1, "[1] PIF 작성 입문 매뉴얼")}</li>
                      <li>{lex(PIF2, "[2] PIF 작성 매뉴얼")}</li>
                      <li>{lex(PIF_EX, "PIF 파일 예시")}</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">PIF 주요<br>구성 항목</th>
                  <td>
                    <ul>
                      <li>제품의 기본 정보: 제품명, 제품 유형, 제형, 용도, 제조공장의 이름 및 주소, 제조업자 또는 수입상의 정보</li>
                      <li>제품 등록·신고 또는 TFDA 시스템상 제품정보 제출 입증자료</li>
                      <li>전성분 명칭 및 함량 / 전성분 목록, 성분명, 함량, 배합목적 및 제한성분 해당 여부</li>
                      <li>제품 포장, 용기, 라벨 및 표시사항 자료</li>
                      <li>GMP 또는 ISO 22716 관련 자료, 해당 시 또는 적용 대상 제품</li>
                      <li>제조방법 및 절차 / 제조공정</li>
                      <li>제품 사용법, 적용부위, 사용량, 사용빈도, 사용대상</li>
                      <li>제품 사용으로 인한 이상사례 또는 알려진 부작용 정보</li>
                      <li>제품 및 개별 성분의 물리·화학적 특성</li>
                      <li>성분 독성학 자료</li>
                      <li>안전성 평가 보고서</li>
                      <li>미생물 검사 보고서</li>
                      <li>보존력 시험 또는 방부력 시험 보고서, 해당 시</li>
                      <li>효능·표방문구 입증자료, 해당 시</li>
                      <li>제품과 접촉하는 포장재 정보</li>
                      <li>제품 안전성 관련 정보 및 참고자료</li>
                    </ul>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">PIF 보관<br>요건</th>
                  <td>
                    <ol>
                      <li>대만 내 수입업자 또는 대만 내 책임주체 소재지에 상시 보관</li>
                      <li>TFDA 요청 시 정해진 기한 내 제출 가능해야 함</li>
                      <li>제품 성분, 제조소, 라벨, 포장, 안전성 자료 등 제품정보 변경 시 업데이트 필요</li>
                      <li>제품의 최종 시판 또는 판매 종료 후 법정 보관기간 동안 보관 필요, 최소 5년 기준 여부는 최신 TFDA 규정 확인 권장</li>
                    </ol>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">준비 절차</th>
                  <td>① 제품 정보 수집 → ② 원료·성분 자료 확보 → ③ 제조·품질시험 자료 확보 → ④ 라벨 및 표방문구 검토 → ⑤ 안전성 평가 수행 → ⑥ PIF 작성 및 자료 누락 검토 → ⑦ 제품 등록·신고 정보와 PIF 정합성 확인 → ⑧ 대만 내 수입업자 또는 책임주체 보관 → ⑨ 변경사항 발생 시 업데이트</td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">주의사항</th>
                  <td>
                    <ul>
                      <li>PIF는 원칙적으로 TFDA에 사전 제출하는 서류가 아니라, 대만 내 보관 후 요청 시 제출하는 기술문서임</li>
                      <li>제품 시판 전 PIF 구축·보관을 완료하고, TFDA 요청 시 제출 가능해야 함</li>
                      <li>모든 자료는 최신 상태로 유지해야 하며, 제품정보 변경 시 즉시 업데이트 필요</li>
                      <li>TFDA 시스템상 제품 등록·신고 정보, 라벨, 전성분, PIF 자료 간 정합성 확인 필요</li>
                      <li>원료 안전성 자료 및 안전성 평가 보고서의 누락 여부를 사전에 확인할 것</li>
                      <li>안전성 평가 보고서는 요구되는 자격요건을 갖춘 평가자가 작성했는지 확인 필요</li>
                      <li>TFDA 제출 대응을 위해 주요 자료의 중문 또는 영문 번역 필요 여부 확인 필요</li>
                    </ul>
                    <p>[참조] {dl(PIF_DOCX, "화장품 제품정보 문서작성 매뉴얼", "DOCX")}</p>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">필요서류</th>
                  <td>
                    <ol>
                      <li>제품 설명서 및 제품 기본정보</li>
                      <li>전성분 목록, 성분명, 함량 및 배합목적</li>
                      <li>제조공정서 및 제조소 정보</li>
                      <li>제품 규격서 및 시험성적서</li>
                      <li>원료 COA, SDS 및 성분 안전성 자료</li>
                      <li>GMP 또는 ISO 22716 인증자료, 해당 시 또는 적용 대상 제품</li>
                      <li>제품 라벨, 포장 도안 및 표시사항 자료</li>
                      <li>안전성 평가 보고서</li>
                      <li>미생물 시험자료</li>
                      <li>안정성 및 보존력 시험자료, 해당 시</li>
                      <li>효능·표방문구 입증자료, 해당 시</li>
                      <li>제품과 접촉하는 포장재 정보, 해당 시</li>
                    </ol>
                  </td>
                </tr>
                <tr>
                  <th class="row-head" scope="row">소요기간</th>
                  <td>약 2~8주 소요, 단 제품 복잡도, 원료자료 확보 수준, 안전성 평가 및 추가 시험 필요 여부에 따라 기간 연장 가능</td>
                </tr>
              </tbody>
            </table>
          </div>
          <a class="law-back" href="law-export-tw.html"><i class="ri-arrow-left-line" aria-hidden="true"></i> 전체 수출절차로 돌아가기</a>"""
