import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="취향 저격 음악 추천",
    page_icon="🎵",
    layout="centered"
)

# 밝고 푸른 계열 커스텀 CSS 적용
st.markdown("""
    <style>
    /* 전체 배경 및 기본 폰트 색상 */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }
    
    /* 메인 타이틀 스타일 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E40AF;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-size: 1.05rem;
        color: #3B82F6;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 추천 노래 카드 스타일 */
    .song-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #3B82F6;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .song-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.12);
    }
    
    .song-number {
        font-size: 0.8rem;
        font-weight: 700;
        color: #2563EB;
        background-color: #EFF6FF;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .song-title-text {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
    }
    
    .song-artist-text {
        font-size: 0.95rem;
        font-weight: 600;
        color: #3B82F6;
        margin-bottom: 8px;
    }
    
    .song-desc-text {
        font-size: 0.9rem;
        color: #64748B;
        line-height: 1.4;
    }

    /* 구분선 스타일 */
    hr {
        border-top: 1px solid #E2E8F0;
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown('<div class="main-title">🎵 취향 저격 음악 추천</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">좋아하는 장르를 선택하고 오늘의 추천곡을 찾아보세요!</div>', unsafe_allow_html=True)

# 음악 장르별 추천 데이터
RECOMMENDATIONS = {
    "K-POP / 댄스": [
        {"title": "Hype Boy", "artist": "NewJeans", "desc": "트렌디하고 청량한 사운드가 돋보이는 팝 댄스 곡"},
        {"title": "Supernova", "artist": "aespa", "desc": "중독성 있는 훅과 강렬한 비트가 매력적인 곡"},
        {"title": "Dynamite", "artist": "방탄소년단 (BTS)", "desc": "경쾌하고 신나는 디스코 팝 장르의 명곡"}
    ],
    "발라드 (Ballad)": [
        {"title": "밤편지", "artist": "아이유 (IU)", "desc": "서정적인 서사와 잔잔한 기타 사운드가 돋보이는 발라드"},
        {"title": "모든 날, 모든 순간", "artist": "폴킴", "desc": "감미로운 음색과 감성적인 가사로 사랑받는 곡"},
        {"title": "첫눈처럼 너에게 가겠다", "artist": "에일리", "desc": "애절한 감정과 폭발적인 가창력이 인상적인 곡"}
    ],
    "R&B / Hip-Hop": [
        {"title": "TOMBOY", "artist": "혁오 (HYUKOH)", "desc": "청춘의 방황과 감성을 담아낸 독보적인 스타일의 곡"},
        {"title": "Square (2017)", "artist": "백예린", "desc": "세련된 R&B 사운드와 특유의 음색이 돋보이는 곡"},
        {"title": "시차 (We Are)", "artist": "우원재 (feat. 로꼬, Gray)", "desc": "진솔한 가사와 중독성 있는 비트의 히트 곡"}
    ],
    "인디 / 어쿠스틱": [
        {"title": "우주를 줄게", "artist": "볼빨간사춘기", "desc": "통통 튀는 음색과 사랑스러운 가사가 매력적인 곡"},
        {"title": "주저하는 연인들을 위해", "artist": "잔나비", "desc": "빈티지하고 아날로그적인 감성이 가득한 레트로 곡"},
        {"title": "스물다섯, 스물하나", "artist": "자우림", "desc": "아련한 추억과 아픔을 노래하는 록 발라드 명곡"}
    ],
    "팝 (Pop)": [
        {"title": "Shape of You", "artist": "Ed Sheeran", "desc": "리드미컬한 비트와 캐치한 멜로디의 세계적인 팝 트랙"},
        {"title": "As It Was", "artist": "Harry Styles", "desc": "신나는 신스팝 사운드에 쌉싸름한 감성을 담은 곡"},
        {"title": "Cruel Summer", "artist": "Taylor Swift", "desc": "시원한 가창력과 드라마틱한 전개가 일품인 곡"}
    ]
}

# 사용자 장르 선택
selected_genre = st.selectbox(
    "🎧 어떤 장르의 음악을 듣고 싶으신가요?",
    options=list(RECOMMENDATIONS.keys())
)

st.markdown("<br>", unsafe_allow_html=True)

# 추천 노래 리스트 출력
if selected_genre:
    st.markdown(f"### ✨ **'{selected_genre}'** 추천 리스트")
    
    songs = RECOMMENDATIONS[selected_genre]
    
    for idx, song in enumerate(songs, 1):
        st.markdown(f"""
            <div class="song-card">
                <span class="song-number">TRACK {idx:02d}</span>
                <div class="song-title-text">{song['title']}</div>
                <div class="song-artist-text">👤 {song['artist']}</div>
                <div class="song-desc-text">💡 {song['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 나만의 추천곡 제안 Form
st.markdown("### 📝 나만의 추천곡 제안하기")
st.write("목록에 없는 명곡이 있다면 추천해 주세요!")

with st.form("suggestion_form", clear_on_submit=True):
    user_genre = st.selectbox("장르 선택", options=list(RECOMMENDATIONS.keys()), key="user_genre")
    user_song = st.text_input("노래 제목", placeholder="예: Ditto")
    user_artist = st.text_input("가수 이름", placeholder="예: NewJeans")
    
    submitted = st.form_submit_button("추천곡 제출하기", type="primary")

    if submitted:
        if user_song and user_artist:
            st.success(f"🎉 감사합니다! [{user_genre}] 장르에 '{user_artist} - {user_song}' 추천이 등록되었습니다.")
        else:
            st.warning("⚠️ 노래 제목과 가수 이름을 모두 입력해 주세요.")
```eof

밝은 파스텔톤 블루(`#F8FAFC`, `#EFF6FF`, `#3B82F6`)와 깔끔한 카드 스타일 디자인을 적용했습니다. 추가로 수정하고 싶은 스타일이나 기능이 있으시면 말씀해 주세요!밝고 청량한 느낌을 주는 **심플 블루(Simple Blue)** 테마의 웹사이트 디자인 가이드입니다. 시원하면서도 눈이 편안한 색상 조합과 깔끔한 레이아웃을 중심으로 구성했습니다.

**컬러 팔레트**

* **Primary (주요 색상):** `#2B6CB0` (청량한 오션 블루 - 버튼, 중요 강조 요소를 위한 색상)
* **Secondary (포인트 색상):** `#4299E1` (밝은 맑은 하늘색 - 호버 효과, 아티클 하이라이트)
* **Background (배경색):** `#F7FAFC` (완전한 흰색보다 눈이 편안한 소프트 쿨 화이트)
* **Card/Surface (카드리뉴):** `#FFFFFF` (순백색 - 콘텐츠 분리를 위한 깔끔한 카드 배경)
* **Text (본문 텍스트):** `#2D3748` (부드러운 다크 그레이 - 완벽한 검정보다 세련된 느낌)

---

**디자인 핵심 포인트**

* **여백 활용 (White Space):** 글자와 요소 사이에 충분한 간격을 두어 시각적 답답함을 줄이고 심플함을 강조합니다.
* **둥근 모서리 (Border Radius):** 버튼과 카드 상자에 약 `8px~12px` 정도의 미세한 곡선을 적용해 부드러운 인상을 줍니다.
* **은은한 그림자:** 강한 테두리 대신 `box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);` 수준의 옅은 그림자로 입체감을 살립니다.

---

**HTML & CSS 코드 예시**
