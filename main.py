<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>10 만들기 사과게임 (Fruit Box Game)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@500;700;800&display=swap');

        body {
            font-family: 'Jua', 'Noto Sans KR', sans-serif;
            user-select: none;
            -webkit-user-select: none;
            touch-action: none;
        }

        /* Apple Game Board Styling */
        .board-grid {
            display: grid;
            grid-template-columns: repeat(17, minmax(0, 1fr));
            gap: 2px;
            padding: 8px;
            background-color: #e2f1db;
            border: 4px solid #8ac76f;
            border-radius: 16px;
            box-shadow: inset 0 3px 6px rgba(0,0,0,0.1), 0 8px 20px rgba(0,0,0,0.15);
            position: relative;
        }

        @media (max-width: 640px) {
            .board-grid {
                grid-template-columns: repeat(10, minmax(0, 1fr));
            }
        }

        .apple-item {
            aspect-ratio: 1 / 1;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.15s ease;
        }

        .apple-item.cleared {
            visibility: hidden;
            pointer-events: none;
        }

        .apple-svg {
            width: 100%;
            height: 100%;
            filter: drop-shadow(0 2px 3px rgba(0,0,0,0.15));
            transition: filter 0.1s;
        }

        .apple-item.selected .apple-svg {
            filter: drop-shadow(0 0 6px #ffea00) brightness(1.1);
        }

        .apple-number {
            position: absolute;
            font-size: clamp(0.9rem, 2vw, 1.4rem);
            font-weight: 800;
            color: #ffffff;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.6);
            pointer-events: none;
            z-index: 2;
        }

        /* Drag Selection Box Overlay */
        #drag-box {
            position: absolute;
            border: 3px dashed #3b82f6;
            background-color: rgba(59, 130, 246, 0.25);
            border-radius: 8px;
            pointer-events: none;
            z-index: 10;
            display: none;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }

        #drag-box.valid {
            border-color: #22c55e;
            background-color: rgba(34, 197, 94, 0.3);
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.4);
        }

        /* Score Pop Float Animation */
        .score-pop {
            position: absolute;
            font-size: 1.5rem;
            font-weight: 800;
            color: #15803d;
            text-shadow: 0 0 5px #ffffff;
            pointer-events: none;
            animation: floatUp 0.8s ease-out forwards;
            z-index: 20;
        }

        @keyframes floatUp {
            0% { opacity: 1; transform: translateY(0) scale(1); }
            100% { opacity: 0; transform: translateY(-30px) scale(1.3); }
        }
    </style>
</head>
<body class="bg-gradient-to-br from-sky-100 via-blue-50 to-indigo-100 min-h-screen flex flex-col items-center justify-between p-3 sm:p-6 select-none">

    <!-- Header Controls & Title -->
    <header class="w-full max-w-4xl flex flex-col sm:flex-row justify-between items-center gap-3 mb-3">
        <div class="flex items-center gap-3">
            <div class="bg-red-500 text-white p-2 sm:p-3 rounded-2xl shadow-lg transform -rotate-3">
                <i class="fa-solid fa-apple-whole text-2xl sm:text-3xl"></i>
            </div>
            <div>
                <h1 class="text-2xl sm:text-4xl font-extrabold text-blue-900 tracking-tight">10 만들기 사과게임</h1>
                <p class="text-xs sm:text-sm text-blue-600 font-semibold">드래그해서 사과 숫자의 합을 10으로 만드세요!</p>
            </div>
        </div>

        <!-- Stat Cards -->
        <div class="flex items-center gap-2 sm:gap-4 w-full sm:w-auto justify-around">
            <!-- Timer Card -->
            <div class="bg-white px-4 py-2 rounded-2xl shadow-md border border-blue-100 flex items-center gap-2 min-w-[100px]">
                <i class="fa-solid fa-stopwatch text-red-500 text-xl"></i>
                <div>
                    <div class="text-[10px] text-gray-400 uppercase font-bold">시간</div>
                    <div id="timer-display" class="text-xl sm:text-2xl font-black text-gray-800">120s</div>
                </div>
            </div>

            <!-- Current Score -->
            <div class="bg-white px-4 py-2 rounded-2xl shadow-md border border-blue-100 flex items-center gap-2 min-w-[100px]">
                <i class="fa-solid fa-trophy text-amber-500 text-xl"></i>
                <div>
                    <div class="text-[10px] text-gray-400 uppercase font-bold">점수</div>
                    <div id="score-display" class="text-xl sm:text-2xl font-black text-blue-600">0</div>
                </div>
            </div>

            <!-- Best Score -->
            <div class="bg-white px-4 py-2 rounded-2xl shadow-md border border-blue-100 flex items-center gap-2 min-w-[100px]">
                <i class="fa-solid fa-crown text-yellow-400 text-xl"></i>
                <div>
                    <div class="text-[10px] text-gray-400 uppercase font-bold">최고점수</div>
                    <div id="high-score-display" class="text-xl sm:text-2xl font-black text-amber-600">0</div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Game Board Wrapper -->
    <main class="w-full max-w-4xl flex-1 flex flex-col justify-center items-center relative my-2">
        <div id="board-container" class="w-full relative touch-none">
            <!-- Board Grid -->
            <div id="board" class="board-grid w-full"></div>
            <!-- Selection Rectangle -->
            <div id="drag-box"></div>
        </div>
    </main>

    <!-- Footer Action Buttons -->
    <footer class="w-full max-w-4xl flex justify-between items-center mt-2 px-2">
        <button id="reset-btn" class="bg-white hover:bg-gray-50 text-blue-600 font-bold px-4 py-2.5 rounded-xl shadow border border-blue-200 flex items-center gap-2 transition active:scale-95 text-sm sm:text-base">
            <i class="fa-solid fa-rotate-right"></i> 새 게임
        </button>
        <div class="text-xs text-gray-500 font-bold hidden sm:block">
            💡 팁: 마우스나 손가락을 눌러 직사각형으로 사과들을 지우세요!
        </div>
    </footer>

    <!-- Start Screen Overlay -->
    <div id="start-modal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full text-center shadow-2xl border-4 border-emerald-400 transform transition-all">
            <div class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4 border-2 border-red-300">
                <i class="fa-solid fa-apple-whole text-red-500 text-4xl"></i>
            </div>
            <h2 class="text-3xl font-black text-gray-800 mb-2">10 만들기 사과게임</h2>
            <p class="text-gray-600 mb-6 leading-relaxed text-sm sm:text-base">
                드래그하여 사과들을 직사각형 모양으로 선택하세요.<br>
                선택한 사과 안의 <strong class="text-red-500 font-extrabold">숫자 합이 10</strong>이 되면 사과가 지워집니다!<br>
                120초 동안 최고의 점수에 도전해 보세요.
            </p>
            <button id="start-btn" class="w-full bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white font-extrabold py-3.5 px-6 rounded-2xl text-xl shadow-lg transform transition active:scale-95">
                게임 시작하기 🚀
            </button>
        </div>
    </div>

    <!-- Game Over Overlay -->
    <div id="gameover-modal" class="fixed inset-0 bg-slate-900/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full text-center shadow-2xl border-4 border-amber-400 transform transition-all">
            <div class="w-20 h-20 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4 border-2 border-amber-300">
                <i class="fa-solid fa-flag-checkered text-amber-500 text-4xl"></i>
            </div>
            <h2 class="text-3xl font-black text-gray-800 mb-1">게임 종료!</h2>
            <p class="text-gray-500 mb-4 text-sm">제한 시간이 모두 지나갔습니다.</p>

            <!-- Final Scores -->
            <div class="bg-sky-50 rounded-2xl p-4 mb-6 border border-sky-100 flex justify-around items-center">
                <div>
                    <div class="text-xs text-gray-500 mb-1 font-bold">최종 점수</div>
                    <div id="final-score" class="text-3xl font-black text-blue-600">0</div>
                </div>
                <div class="h-8 w-px bg-sky-200"></div>
                <div>
                    <div class="text-xs text-gray-500 mb-1 font-bold">최고 점수</div>
                    <div id="final-high-score" class="text-3xl font-black text-amber-500">0</div>
                </div>
            </div>

            <button id="restart-btn" class="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-extrabold py-3.5 px-6 rounded-2xl text-xl shadow-lg transform transition active:scale-95">
                다시 도전하기 🔄
            </button>
        </div>
    </div>

    <script>
        // Game Configuration
        const COLS = window.innerWidth <= 640 ? 10 : 17;
        const ROWS = 10;
        const GAME_DURATION = 120; // Seconds

        // State Variables
        let boardData = []; // { id, num, element, row, col, isCleared }
        let score = 0;
        let highScore = parseInt(localStorage.getItem('apple_game_high_score') || '0', 10);
        let timeLeft = GAME_DURATION;
        let timerInterval = null;
        let isGaming = false;

        // Drag Select State
        let isDragging = false;
        let startX = 0;
        let startY = 0;
        let selectedApples = [];

        // SVG Template for Apples
        const APPLE_SVG = `
        <svg class="apple-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 15 C45 5, 30 10, 35 25 C20 25, 10 40, 10 60 C10 85, 35 95, 50 90 C65 95, 90 85, 90 60 C90 40, 80 25, 65 25 C70 10, 55 5, 50 15 Z" fill="#ef4444"/>
            <path d="M50 15 C42 8, 32 12, 35 25 Z" fill="#dc2626"/>
            <!-- Leaf & Stem -->
            <path d="M50 20 Q52 10 58 5" stroke="#78350f" stroke-width="4" fill="none" stroke-linecap="round"/>
            <path d="M54 12 Q65 5 72 12 Q62 20 54 12 Z" fill="#22c55e"/>
            <!-- Highlight -->
            <ellipse cx="32" cy="40" rx="6" ry="12" transform="rotate(-25 32 40)" fill="#ffffff" opacity="0.3"/>
        </svg>
        `;

        // DOM Elements
        const boardEl = document.getElementById('board');
        const containerEl = document.getElementById('board-container');
        const dragBox = document.getElementById('drag-box');
        const timerEl = document.getElementById('timer-display');
        const scoreEl = document.getElementById('score-display');
        const highScoreEl = document.getElementById('high-score-display');
        const startModal = document.getElementById('start-modal');
        const gameoverModal = document.getElementById('gameover-modal');
        const startBtn = document.getElementById('start-btn');
        const restartBtn = document.getElementById('restart-btn');
        const resetBtn = document.getElementById('reset-btn');
        const finalScoreEl = document.getElementById('final-score');
        const finalHighScoreEl = document.getElementById('final-high-score');

        function initBoard() {
            boardEl.innerHTML = '';
            boardData = [];
            
            // Adjust grid columns dynamically
            boardEl.style.gridTemplateColumns = `repeat(${COLS}, minmax(0, 1fr))`;

            for (let r = 0; r < ROWS; r++) {
                for (let c = 0; c < COLS; c++) {
                    const num = Math.floor(Math.random() * 9) + 1; // Number 1-9
                    const id = r * COLS + c;

                    const appleDiv = document.createElement('div');
                    appleDiv.className = 'apple-item';
                    appleDiv.dataset.id = id;
                    appleDiv.dataset.row = r;
                    appleDiv.dataset.col = c;

                    appleDiv.innerHTML = `${APPLE_SVG}<span class="apple-number">${num}</span>`;

                    boardEl.appendChild(appleDiv);

                    boardData.push({
                        id,
                        row: r,
                        col: c,
                        num,
                        element: appleDiv,
                        isCleared: false
                    });
                }
            }
        }

        function startGame() {
            score = 0;
            timeLeft = GAME_DURATION;
            scoreEl.textContent = score;
            highScoreEl.textContent = highScore;
            timerEl.textContent = `${timeLeft}s`;

            initBoard();

            startModal.classList.add('hidden');
            gameoverModal.classList.add('hidden');
            isGaming = true;

            clearInterval(timerInterval);
            timerInterval = setInterval(() => {
                timeLeft--;
                timerEl.textContent = `${timeLeft}s`;

                if (timeLeft <= 0) {
                    endGame();
                }
            }, 1000);
        }

        function endGame() {
            isGaming = false;
            clearInterval(timerInterval);

            if (score > highScore) {
                highScore = score;
                localStorage.setItem('apple_game_high_score', highScore.toString());
                highScoreEl.textContent = highScore;
            }

            finalScoreEl.textContent = score;
            finalHighScoreEl.textContent = highScore;
            gameoverModal.classList.remove('hidden');
        }

        function getPointerPos(e) {
            const rect = containerEl.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        }

        function onPointerDown(e) {
            if (!isGaming) return;
            isDragging = true;
            const pos = getPointerPos(e);
            startX = pos.x;
            startY = pos.y;

            dragBox.style.left = `${startX}px`;
            dragBox.style.top = `${startY}px`;
            dragBox.style.width = '0px';
            dragBox.style.height = '0px';
            dragBox.style.display = 'block';
            dragBox.classList.remove('valid');

            updateSelection(startX, startY, startX, startY);
        }

        function onPointerMove(e) {
            if (!isDragging || !isGaming) return;
            const pos = getPointerPos(e);
            const currentX = pos.x;
            const currentY = pos.y;

            const left = Math.min(startX, currentX);
            const top = Math.min(startY, currentY);
            const width = Math.abs(currentX - startX);
            const height = Math.abs(currentY - startY);

            dragBox.style.left = `${left}px`;
            dragBox.style.top = `${top}px`;
            dragBox.style.width = `${width}px`;
            dragBox.style.height = `${height}px`;

            updateSelection(left, top, left + width, top + height);
        }

        function onPointerUp() {
            if (!isDragging || !isGaming) return;
            isDragging = false;
            dragBox.style.display = 'none';

            // Check total sum of selected apples
            const currentSum = selectedApples.reduce((acc, apple) => acc + apple.num, 0);

            if (currentSum === 10) {
                // Clear selected apples
                selectedApples.forEach(apple => {
                    apple.isCleared = true;
                    apple.element.classList.add('cleared');
                });

                // Increase Score
                const gainedPoints = selectedApples.length;
                score += gainedPoints;
                scoreEl.textContent = score;

                // Show Score Animation
                if (selectedApples.length > 0) {
                    showScorePop(selectedApples[0].element, `+${gainedPoints}`);
                }
            }

            // Reset Selection Highlight
            boardData.forEach(apple => {
                apple.element.classList.remove('selected');
            });
            selectedApples = [];
        }

        function updateSelection(left, top, right, bottom) {
            selectedApples = [];
            let currentSum = 0;

            boardData.forEach(apple => {
                if (apple.isCleared) return;

                const rect = apple.element.getBoundingClientRect();
                const containerRect = containerEl.getBoundingClientRect();

                const appleLeft = rect.left - containerRect.left;
                const appleTop = rect.top - containerRect.top;
                const appleRight = appleLeft + rect.width;
                const appleBottom = appleTop + rect.height;

                // Check intersection with selection box
                const isIntersect = !(
                    appleLeft > right ||
                    appleRight < left ||
                    appleTop > bottom ||
                    appleBottom < top
                );

                if (isIntersect) {
                    apple.element.classList.add('selected');
                    selectedApples.push(apple);
                    currentSum += apple.num;
                } else {
                    apple.element.classList.remove('selected');
                }
            });

            // Turn green if exact 10 sum
            if (currentSum === 10) {
                dragBox.classList.add('valid');
            } else {
                dragBox.classList.remove('valid');
            }
        }

        function showScorePop(element, text) {
            const pop = document.createElement('div');
            pop.className = 'score-pop';
            pop.textContent = text;
            pop.style.left = `${element.offsetLeft + 10}px`;
            pop.style.top = `${element.offsetTop - 10}px`;

            containerEl.appendChild(pop);
            setTimeout(() => pop.remove(), 800);
        }

        // Mouse Events
        containerEl.addEventListener('mousedown', onPointerDown);
        window.addEventListener('mousemove', onPointerMove);
        window.addEventListener('mouseup', onPointerUp);

        // Touch Events
        containerEl.addEventListener('touchstart', onPointerDown, { passive: false });
        window.addEventListener('touchmove', onPointerMove, { passive: false });
        window.addEventListener('touchend', onPointerUp);

        // Buttons
        startBtn.addEventListener('click', startGame);
        restartBtn.addEventListener('click', startGame);
        resetBtn.addEventListener('click', startGame);

        // Init Display HighScore on Load
        highScoreEl.textContent = highScore;
        initBoard();
    </script>
</body>
</html>
