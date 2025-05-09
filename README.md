# 프로젝트 이름: MarkCloud

# 상표 검색 프로젝트

이 프로젝트는 FastAPI와 HTML을 사용하여 상표를 검색하는 웹 애플리케이션입니다. 사용자는 다양한 필터와 검색 조건을 통해 상표 데이터를 검색하고 결과를 확인할 수 있습니다.


1. ## API 사용법 및 실행 방법

- **API데이터 소스**

- **trademark_sample.json**  
  - 샘플 상표 데이터가 담긴 JSON 파일입니다.  
  - `main.py`에서 이 파일을 로드하여 검색 API의 기본 데이터로 사용합니다.  
  - **컬럼명**
  `productName` (상표명(한글)), `productNameEng` (상표명(영문)), `applicationNumber` (출원 번호), `applicationDate` (출원일, YYYYMMDD 형식), `registerStatus` (상표 등록 상태: 등록, 실효, 거절, 출원 등), `publicationNumber` (공고 번호), 
  `publicationDate` (공고일, YYYYMMDD 형식), `registrationNumber` (등록 번호), `registrationDate` (등록일, YYYYMMDD 형식), `internationalRegNumbers` (국제 출원 번호), `internationalRegDate` (국제출원일, YYYYMMDD 형식), `priorityClaimNumList` (우선권 번호), `priorityClaimDateList` (우선권 일자, YYYYMMDD 형식), `asignProductMainCodeList` (상품 주 분류 코드 리스트), `asignProductSubCodeList` (상품 유사군 코드 리스트), `viennaCodeList` (비엔나 코드 리스트)

  - **사용된 컬럼명** 
  `applicationNumber`(상품 코드), `productName`, `productNameEng`, `registerStatus`, `applicationDate` 등의 필드가 포함되어 있습니다.


- **프로젝트 클론**
 
 깃허브에서 프로젝트를 클론합니다.

- **깃 주소**: git clone https://github.com/park967/MarkCloud.git

- **사용된 필수 패키지 목록및 의존성 설치**: pip install -r requirements.txt

- **웹 애플리케이션 접속**  
브라우저에서 `http://127.0.0.1:8000/search`에 접속

2. ## 구현된 기능 설명

- **상표 검색**: 상품 코드, 검색어, 등록 상태 등 다양한 조건으로 상표를 검색할 수 있습니다.
- **필터링**: 등록 상태, 날짜 범위, 정렬 기준 등을 필터링할 수 있습니다.
- **페이지네이션**: 검색 결과를 페이지 단위로 나누어 보여줍니다 (1페이지 당 20개씩, 10개씩 묶은 페이지 번호 제공 합니다).
- **디테일한 정보 제공**: 상품 코드, 상품명(한글/영문), 등록 상태, 등록일 등의 정보를 확인할 수 있습니다.



3. ## 기술적 의사결정에 대한 설명


- **요구사항 충족: FastAPI**: 회사의 필수 스펙(“Python 기반 FastAPI 프레임워크 사용”)을 준수하기 위해 FastAPI를 도입했습니다. FastAPI는 비동기 처리 성능과 자동 문서화(OpenAPI) 기능을 제공하므로, 안정적인 API 개발과 유지보수가 용이합니다.
- **Jinja2 템플릿**: 사용자 입력과 검색 결과를 서버 사이드에서 실시간 렌더링하여 직관적이고 편리한 UI 제공
- **페이지네이션**: 대량(10만 건 이상) 데이터를 효율적으로 처리하기 위해 확장성 확보


4. ## 문제 해결 과정에서 고민했던 점

1. **검색 성능**  
- 대량 데이터 필터링 최적화  
- null값 처리방식 (" " 공백처리)
- 데이터 검색기능에 퍼지 검색 기능 추가

2. **날짜 처리**  
- 다양한 형식(YYYYMMDD, YYYY-MM-DD) 파싱 후 범위 필터링

3. **페이지네이션 UX**  
- 데이터가 10만 건 이상으로 늘어날 경우, 페이지네이션은 시스템의 확장성을 고려한 방법입니다. 데이터를 페이지별로 나누어 처리하면 데이터 양에 관계없이 안정적인 성능을 유지할 수 있습니다. 또한, 필요에 따라 더 많은 페이지를 추가하거나, 다른 기준으로 페이지네이션을 조정할 수 있습니다.한 페이지에 너무 많은 결과가 표시되면 사용자가 원하는 정보를 찾기 어렵고, 스크롤이 매우 길어져서 불편할 수 있습니다. 페이지네이션을 통해 20개씩 나누어 보여주면 사용자는 쉽게 원하는 결과를 찾을 수 있습니다.

4. **필요 필드 선정**  
   - JSON에 여러 컬럼이 존재했지만, 검색·필터링과 결과 출력에 꼭 필요한 `productName`, `productNameEng`, `applicationNumber`, `applicationDate`, `registerStatus` 필드만 우선 선택하여 로직과 템플릿을 간소화했습니다.



