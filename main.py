from fastapi import FastAPI, Query, Request
from typing import Optional
import json
import difflib
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# JSON 데이터 로딩
with open("trademark_sample.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# 날짜 비교를 위한 헬퍼 함수
def parse_date(date_str: str) -> Optional[datetime]:
    try:
        if len(date_str) == 8 and date_str.isdigit():
            # 하이픈 없는 날짜 처리
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
def search_trademarks(
    request: Request,
    query: Optional[str] = Query(None, description="검색어"),
    status: Optional[str] = Query(None, description="등록 상태"),
    product_code: Optional[str] = Query(None, description="상품 코드"),
    start_date: Optional[str] = Query(None, description="시작 등록일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료 등록일 (YYYY-MM-DD)"),
    sort_by: Optional[str] = Query(None, description="정렬 기준 (registerDate, productCode)"),
    sort_order: Optional[str] = Query("asc", description="정렬 순서 (asc, desc)")
):
    try:
        start_dt = parse_date(start_date) if start_date else None
        end_dt = parse_date(end_date) if end_date else None

        def match(item):
            # 키워드 검색 (정확/유사)
            name_kor = item.get("productName", "")
            name_eng = item.get("productNameEng", "")
            keyword_match = True
            if query:
                target_text = f"{name_kor} {name_eng}".lower()
                keyword_match = (
                    query.lower() in target_text or
                    any(q in target_text for q in difflib.get_close_matches(query.lower(), [target_text], n=1, cutoff=0.6))
                )

            # 등록 상태 필터
            status_match = True
            if status:
                status_match = item.get("registerStatus", "").lower() == status.lower()

            # 상품 코드 필터
            code_match = True
            if product_code:
                # 상품 코드가 숫자로 입력되어 있을 경우 숫자로 처리
                if product_code.isdigit():
                    code_match = product_code in str(item.get("applicationNumber", ""))
                else:
                    code_match = str(item.get("applicationNumber", "")) == product_code

            # 날짜 필터
            date_match = True
            if start_dt or end_dt:
                reg_date = parse_date(item.get("applicationDate", ""))
                if reg_date:
                    if start_dt and reg_date < start_dt:
                        return False
                    if end_dt and reg_date > end_dt:
                        return False
                else:
                    return False

            return keyword_match and status_match and code_match and date_match

        # 필터링된 결과 리스트
        filtered_results = [item for item in raw_data if match(item)]

        # 정렬
        if sort_by:
            reverse_order = True if sort_order == "desc" else False
            if sort_by == "applicationDate":
                filtered_results.sort(key=lambda x: parse_date(x.get("applicationDate", "1970-01-01")), reverse=reverse_order)
            elif sort_by == "applicationNumber":
                filtered_results.sort(key=lambda x: x.get("applicationNumber", ""), reverse=reverse_order)

        # 디버깅 로그
        print(f"Filtered Results Count: {len(filtered_results)}")
        print(f"Filtered Results: {filtered_results[:5]}")  # 처음 5개 결과만 확인

        # 템플릿 렌더링
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "status": status,
                "product_code": product_code,
                "start_date": start_date,
                "end_date": end_date,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "count": len(filtered_results),
                "results": filtered_results
            }
        )

    except Exception as e:
        return {"error": str(e)}
