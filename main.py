import streamlit as st

# 페이지 기본 설정 (타이틀, 아이콘, 레이아웃)
st.set_page_config(page_title="음악 장르별 노래 추천", page_icon="🎵", layout="centered")

st.title("🎵 취향 저격 음악 추천 앱")
st.write("좋아하는 음악 장르를 선택하시면 어울리는 노래들을 추천해 드려요!")

# 1. 음악 장르별 추천 데이터 정의
# 각 장르마다 추천할 곡의 정보(제목, 가수, 설명)를 담고 있습니다.
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

# 2. 사용자 입력 (장르 선택 박스)
selected_genre = st.selectbox(
    "🎧 어떤 장르의 음악을 듣고 싶으신가요?",
    options=list(RECOMMENDATIONS.keys())
)

# 3. 선택한 장르에 따른 노래 추천 결과 출력
if selected_genre:
    st.subheader(f"✨ '{selected_genre}' 추천 리스트")
    
    songs = RECOMMENDATIONS[selected_genre]
    
    # 곡 목록을 깔끔한 카드로 출력
    for idx, song in enumerate(songs, 1):
        with st.container():
            st.markdown(f"### {idx}. **{song['title']}** - {song['artist']}")
            st.caption(f"💡 {song['desc']}")
            st.write("")  # 간격 조절

st.markdown("---")

# 4. 사용자 취향 반영 기능 (추가곡 제안하기)
st.subheader("📝 나만의 추천곡 제안하기")
st.write("목록에 없는 좋은 노래가 있다면 공유해 주세요!")

with st.form("suggestion_form", clear_on_submit=True):
    user_genre = st.selectbox("장르", options=list(RECOMMENDATIONS.keys()), key="user_genre")
    user_song = st.text_input("노래 제목")
    user_artist = st.text_input("가수 이름")
    submitted = st.form_submit_button("추천곡 제출하기")

    if submitted:
        if user_song and user_artist:
            st.success(f"감사합니다! [{user_genre}] 장르에 '{user_artist} - {user_song}' 곡이 추천 목록에 제안되었습니다.")
        else:
            st.warning("노래 제목과 가수 이름을 모두 입력해 주세요.")
