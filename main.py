import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="음악 장르별 노래 추천", page_icon="🎵", layout="centered")

# 심플하고 밝은 푸른 계열 커스텀 CSS 적용
st.markdown("""
    <style>
    /* 전체 배경 및 메인 레이아웃 */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }
    
    /* 메인 타이틀 및 헤더 */
    h1 {
        color: #1E3A8A !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #2563EB !important;
    }
    
    /* 셀렉트박스 및 폼 요소 강조 스타일 */
    .stSelectbox label, .stTextInput label {
        color: #1E3A8A !important;
        font-weight: 600 !important;
    }
    
    /* 추천 노래 카드 디자인 */
    .song-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        padding: 18px 22px;
        border-radius: 10px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06);
    }
    .song-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .song-artist {
        font-size: 0.95rem;
        color: #2563EB;
        font-weight: 600;
        margin-left: 6px;
    }
    .song-desc {
        font-size: 0.88rem;
        color: #64748B;
        margin-top: 6px;
    }

    /* 구분선 및 버튼 스타일 */
    hr {
        border-top: 1px dashed #CBD5E1 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 취향 저격 음악 추천 앱")
st.write("좋아하는 음악 장르를 선택하시면 푸른 감성에 어울리는 명곡들을 추천해 드려요!")

# 1. 음악 장르별 추천 데이터
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

st.markdown("---")

# 2. 장르 선택
selected_genre = st.selectbox(
    "🎧 어떤 장르의 음악을 듣고 싶으신가요?",
    options=list(RECOMMENDATIONS.keys())
)

# 3. 추천 카드 출력
if selected_genre:
    st.subheader(f"✨ '{selected_genre}' 추천 리스트")
    
    songs = RECOMMENDATIONS[selected_genre]
    
    for idx, song in enumerate(songs, 1):
        st.markdown(f"""
            <div class="song-card">
                <span class="song-title">{idx}. {song['title']}</span>
                <span class="song-artist">- {song['artist']}</span>
                <div class="song-desc">💡 {song['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 4. 사용자 추천곡 제안 폼
st.subheader("📝 나만의 추천곡 제안하기")

with st.form("suggestion_form", clear_on_submit=True):
    user_genre = st.selectbox("장르", options=list(RECOMMENDATIONS.keys()), key="user_genre")
    user_song = st.text_input("노래 제목")
    user_artist = st.text_input("가수 이름")
    submitted = st.form_submit_button("추천곡 제출하기")

    if submitted:
        if user_song and user_artist:
            st.success(f"감사합니다! [{user_genre}] 장르에 '{user_artist} - {user_song}' 곡이 제안되었습니다.")
        else:
            st.warning("노래 제목과 가수 이름을 모두 입력해 주세요.")
