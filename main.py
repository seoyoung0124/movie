from datetime import datetime, timedelta
import zoneinfo
import pandas as pd
import requests
import streamlit as st

# 페이지 기본 설정 (타이틀 및 레이아웃)
st.set_page_config(page_title="어제 박스오피스", page_icon="🎬", layout="wide")

st.title("🎬 어제의 일별 박스오피스")


# 1. API 키 불러오기 (Streamlit Secrets 활용)
# Streamlit Cloud의 Secrets에 저장된 KOBIS_KEY를 가져옵니다.
try:
    API_KEY = st.secrets["KOBIS_KEY"]
except Exception:
    st.error(
        "🔑 **인증키 설정 필요**: Streamlit Cloud의 `Secrets` 설정에서 `KOBIS_KEY`를 등록해 주세요."
    )
    st.stop()


# 2. 한국 시간(Asia/Seoul) 기준 '어제' 날짜 계산하기
# 서버 시계가 해외 기준이어도 항상 한국 시간 기준으로 어제 날짜를 계산합니다.
korea_tz = zoneinfo.ZoneInfo("Asia/Seoul")
now_korea = datetime.now(korea_tz)
yesterday = now_korea - timedelta(days=1)
target_dt = yesterday.strftime("%Y%m%d")  # YYYYMMDD 형식 변환

st.caption(f"📅 조회 기준일: {yesterday.strftime('%Y년 %m월 %d일')} (한국 시간 기준)")


# 3. KOBIS API 데이터 요청하기
url = "https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
params = {"key": API_KEY, "targetDt": target_dt}

try:
    response = requests.get(url, timeout=10)
    # HTTP 상태 코드가 200이 아니면 예외 발생
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    st.error(
        "🚨 **네트워크 오류**: 영화진흥위원회 API 서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요."
    )
    st.caption(f"상세 오류: {e}")
    st.stop()


# 4. API 응답 에러 및 빈 데이터 예외 처리
# KOBIS API는 인증키가 틀려도 200 OK와 함께 faultInfo 객체를 반환합니다.
if "faultInfo" in data:
    st.error(
        "❌ **API 인증 오류**: 발급받은 KOBIS_KEY가 올바른지 확인해 주세요."
    )
    st.info(
        "💡 **확인 사항**:\n- KOBIS Open API 사이트에서 키가 정상 발급되었는지 확인\n- Streamlit Secrets에 입력한 키 이름이 `KOBIS_KEY`가 맞는지 확인"
    )
    st.stop()

# boxOfficeResult 및 dailyBoxOfficeList 존재 여부 확인
box_office_result = data.get("boxOfficeResult", {})
daily_list = box_office_result.get("dailyBoxOfficeList", [])

if not daily_list:
    st.warning("⚠️ **데이터 없음**: 해당 날짜의 박스오피스 정보가 존재하지 않습니다.")
    st.info(
        "💡 **확인 사항**:\n- 집계 지연으로 인해 아직 데이터가 등록되지 않았을 수 있습니다.\n- KOBIS 공식 홈페이지의 집계 현황을 확인해 주세요."
    )
    st.stop()


# 5. 데이터 가공 (문자열 -> 숫자 변환)
df = pd.DataFrame(daily_list)

# 숫자로 변환할 컬럼 지정 (KOBIS API는 숫자를 문자열 형태로 전달함)
numeric_cols = ["rank", "audiCnt", "audiAcc", "scrnCnt"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 보기 편한 컬럼명으로 변경 및 정렬
df = df.sort_values("rank")


# 6. 1위 영화 Highlight (지표 카드 3개)
top_movie = df.iloc[0]

st.subheader(f"🥇 어제 1위: {top_movie['movieNm']}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="당일 관객수", value=f"{top_movie['audiCnt']:,} 명")
with col2:
    st.metric(label="누적 관객수", value=f"{top_movie['audiAcc']:,} 명")
with col3:
    st.metric(label="스크린수", value=f"{top_movie['scrnCnt']:,} 개")

st.markdown("---")


# 7. 관객수 상위 5편 막대그래프
st.subheader("📊 관객수 TOP 5")

top5_df = df.head(5).copy()
# 시각화를 위해 관객수 단위 및 표시용 컬럼 준비
top5_df = top5_df.set_index("movieNm")

# Streamlit 기본 막대그래프 출력
st.bar_chart(top5_df["audiCnt"])

st.markdown("---")


# 8. 전체 박스오피스 순위 표 출력
st.subheader("📋 전체 순위 목록")

# 표에 보여줄 컬럼 선택 및 이름 변경
display_df = df[
    ["rank", "movieNm", "openDt", "audiCnt", "audiAcc", "scrnCnt"]
].copy()
display_df.columns = [
    "순위",
    "영화명",
    "개봉일",
    "관객수",
    "누적관객",
    "스크린수",
]

# 숫자에 쉼표(,) 포맷팅을 적용하여 출력
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "순위": st.column_config.NumberColumn(format="%d"),
        "관객수": st.column_config.NumberColumn(format="%d 명"),
        "누적관객": st.column_config.NumberColumn(format="%d 명"),
        "스크린수": st.column_config.NumberColumn(format="%d 개"),
    },
)
