import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="사과게임 (10 만들기)",
    page_icon="🍎",
    layout="centered"
)

st.title("🍎 10 만들기 사과게임")
st.write("드래그하여 상자 안의 숫자의 합을 **10**으로 만드세요!")

# HTML, CSS, JavaScript 코드 전체 정의
# (f-string 파이썬 중괄호 이슈 방지를 위해 일반 멀티라인 문자열 사용)
apple_game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>사과게임</title>
    <style>
        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
        }
        body {
            font-family: 'Pretendard', sans-serif;
            background-color: #f8fafc;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .scoreboard {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 600px;
            background: white;
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        .stat-box {
            text-align: center;
        }
        .stat-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 4px;
        }
        .stat-value {
            font-size: 20px;
            font-weight: bold;
            color: #1e293b;
        }
        #game-board {
            position: relative;
            display: grid;
            grid-template-columns: repeat(17, 1fr);
            gap: 2px;
            background: #e2e8f0;
            padding: 5px;
            border-radius: 10px;
            width: 100%;
            max-width: 600px;
            aspect-ratio: 17/10;
            touch-action: none;
        }
        .apple {
            background-color: #ef4444;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            box-shadow: inset -2px -2px 4px rgba(0,0,0,0.2);
            cursor: pointer;
            position: relative;
        }
        .apple.selected {
            background-color: #fbbf24;
            transform: scale(0.95);
        }
        .apple.cleared {
            visibility: hidden;
        }
        #drag-box {
            position: absolute;
            border: 2px dashed #3b82f6;
            background-color: rgba(59, 130, 246, 0.2);
            pointer-events: none;
            display: none;
            border-radius: 6px;
        }
        .btn-reset {
            margin-top: 15px;
            background-color: #ef4444;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
        }
        .btn-reset:hover {
            background-color: #dc2626;
        }
    </style>
</head>
<body>

    <div class="scoreboard">
        <div class="stat-box">
            <div class="stat-label">점수</div>
            <div class="stat-value" id="score">0</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">남은 시간</div>
            <div class="stat-value" id="timer">120</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">최고 점수</div>
            <div class="stat-value" id="high-score">0</div>
        </div>
    </div>

    <div id="game-board">
        <div id="drag-box"></div>
    </div>

    <button class="btn-reset" onclick="initGame()">다시 시작</button>

    <script>
        const ROWS = 10;
        const COLS = 17;
        const GAME_TIME = 120;

        let score = 0;
        let timeLeft = GAME_TIME;
        let timerInterval = null;
        let apples = [];
        let isDragging = false;
        let startPos = { x: 0, y: 0 };

        const board = document.getElementById('game-board');
        const dragBox = document.getElementById('drag-box');
        const scoreEl = document.getElementById('score');
        const timerEl = document.getElementById('timer');
        const highScoreEl = document.getElementById('high-score');

        // 최고 점수 불러오기
        let highScore = localStorage.getItem('apple_game_high_score') || 0;
        highScoreEl.innerText = highScore;

        function initGame() {
            clearInterval(timerInterval);
            score = 0;
            timeLeft = GAME_TIME;
            scoreEl.innerText = score;
            timerEl.innerText = timeLeft;
            
            // 기존 사과 제거
            const existingApples = board.querySelectorAll('.apple');
            existingApples.forEach(el => el.remove());

            apples = [];
            
            // 사과 생성 (1~9 랜덤)
            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    const num = Math.floor(Math.random() * 9) + 1;
                    const apple = document.createElement('div');
                    apple.className = 'apple';
                    apple.innerText = num;
                    apple.dataset.row = r;
                    apple.dataset.col = c;
                    apple.dataset.val = num;
                    board.appendChild(apple);
                    apples.push(apple);
                }
            }

            // 타이머 시작
            timerInterval = setInterval(() => {
                timeLeft--;
                timerEl.innerText = timeLeft;
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    alert(`게임 종료! 최종 점수: ${score}점`);
                    if (score > highScore) {
                        highScore = score;
                        localStorage.setItem('apple_game_high_score', highScore);
                        highScoreEl.innerText = highScore;
                    }
                }
            }, 1000);
        }

        // 드래그 이벤트 (마우스/터치)
        function getPos(e) {
            const rect = board.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        }

        function onStart(e) {
            if (timeLeft <= 0) return;
            isDragging = true;
            startPos = getPos(e);
            dragBox.style.display = 'block';
            dragBox.style.left = startPos.x + 'px';
            dragBox.style.top = startPos.y + 'px';
            dragBox.style.width = '0px';
            dragBox.style.height = '0px';
        }

        function onMove(e) {
            if (!isDragging) return;
            const currentPos = getPos(e);

            const x = Math.min(startPos.x, currentPos.x);
            const y = Math.min(startPos.y, currentPos.y);
            const width = Math.abs(currentPos.x - startPos.x);
            const height = Math.abs(currentPos.y - startPos.y);

            dragBox.style.left = x + 'px';
            dragBox.style.top = y + 'px';
            dragBox.style.width = width + 'px';
            dragBox.style.height = height + 'px';

            // 선택 영역에 들어온 사과 하이라이트
            const boxRect = { left: x, top: y, right: x + width, bottom: y + height };
            
            apples.forEach(apple => {
                if (apple.classList.contains('cleared')) return;
                
                const aLeft = apple.offsetLeft;
                const aTop = apple.offsetTop;
                const aRight = aLeft + apple.offsetWidth;
                const aBottom = aTop + apple.offsetHeight;

                const isOverlap = !(aRight < boxRect.left || 
                                    aLeft > boxRect.right || 
                                    aBottom < boxRect.top || 
                                    aTop > boxRect.bottom);

                if (isOverlap) {
                    apple.classList.add('selected');
                } else {
                    apple.classList.remove('selected');
                }
            });
        }

        function onEnd() {
            if (!isDragging) return;
            isDragging = false;
            dragBox.style.display = 'none';

            const selectedApples = apples.filter(a => a.classList.contains('selected') && !a.classList.contains('cleared'));
            
            // 합계 계산
            const sum = selectedApples.reduce((acc, a) => acc + parseInt(a.dataset.val), 0);

            if (sum === 10) {
                selectedApples.forEach(a => {
                    a.classList.remove('selected');
                    a.classList.add('cleared');
                });
                score += selectedApples.length;
                scoreEl.innerText = score;
            } else {
                selectedApples.forEach(a => a.classList.remove('selected'));
            }
        }

        board.addEventListener('mousedown', onStart);
        window.addEventListener('mousemove', onMove);
        window.addEventListener('mouseup', onEnd);

        board.addEventListener('touchstart', onStart, {passive: false});
        window.addEventListener('touchmove', onMove, {passive: false});
        window.addEventListener('touchend', onEnd);

        initGame();
    </script>
</body>
</html>
"""

# Streamlit에 컴포넌트로 HTML 삽입
components.html(apple_game_html, height=520, scrolling=False)
