// 获取DOM元素
const boardElement = document.getElementById('board');
const resetButton = document.getElementById('resetButton');
const statusElement = document.getElementById('status');

// 初始化棋盘
function generateBoard() {
    fetch('/reveal', {
        method: 'POST',
        body: JSON.stringify({ row: 0, col: 0 }),
    }).then(response => response.json())
    .then(data => {
        const publicBoard = data.public_board;
        const flaggedBoard = data.flagged_board;

        // 清空棋盘
        boardElement.innerHTML = '';

        // 动态生成棋盘
        for (let r = 0; r < publicBoard.length; r++) {
            const row = document.createElement('tr');
            for (let c = 0; c < publicBoard[r].length; c++) {
                const cell = document.createElement('td');
                const cellValue = publicBoard[r][c] !== null ? publicBoard[r][c] : '';

                // 设置格子的内容
                cell.textContent = cellValue;
                cell.className = flaggedBoard[r][c] ? 'flagged' : '';
                cell.addEventListener('click', () => revealCell(r, c));
                cell.addEventListener('contextmenu', (event) => {
                    event.preventDefault();
                    toggleFlag(r, c);
                });

                row.appendChild(cell);
            }
            boardElement.appendChild(row);
        }

        // 更新游戏状态
        updateStatus(data.status);
    });
}

// 揭示格子
function revealCell(row, col) {
    fetch('/reveal', {
        method: 'POST',
        body: JSON.stringify({ row: row, col: col }),
    }).then(response => response.json())
    .then(data => {
        generateBoard(); // 更新棋盘
        updateStatus(data.status); // 更新游戏状态
    });
}

// 标记旗子
function toggleFlag(row, col) {
    fetch('/flag', {
        method: 'POST',
        body: JSON.stringify({ row: row, col: col }),
    }).then(response => response.json())
    .then(data => {
        generateBoard(); // 更新棋盘
    });
}

// 更新游戏状态
function updateStatus(status) {
    statusElement.textContent = status;
}

// 重置游戏
resetButton.addEventListener('click', () => {
    fetch('/reset', {
        method: 'POST'
    }).then(() => {
        generateBoard(); // 更新棋盘
    });
});

// 初始化棋盘
generateBoard();
