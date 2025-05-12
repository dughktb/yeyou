import random

class Minesweeper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]  
        self.game_over = False
        self._place_mines()

    def reset_game(self):
        """重置游戏，重新生成棋盘并放置地雷"""
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flags = [[False] * self.cols for _ in range(self.rows)]
        self.game_over = False
        self._place_mines()  # 重新放置地雷

    def _place_mines(self):
        """随机放置地雷，并更新周围格子的数字"""
        positions = random.sample(range(self.rows * self.cols), self.mines)
        for pos in positions:  
            row = pos // self.cols
            col = pos % self.cols
            self.board[row][col] = -1  # -1 表示地雷
            # 更新周围8格的数字
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.board[nr][nc] != -1:
                            self.board[nr][nc] += 1

    def reveal(self, row, col):
        """揭示格子，若是地雷则游戏失败，若是 0 则递归揭示周围格子"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return []
        if self.revealed[row][col]:
            return []

        self.revealed[row][col] = True
        result = []

        # 如果是地雷，返回当前格子，游戏失败可由前端判断
        if self.board[row][col] == -1:
            self.game_over = True
            return [(row, col, -1)]

        # 如果是 0，则递归揭示周围格子
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.revealed[nr][nc]:
                        result.extend(self.reveal(nr, nc))

        # 返回当前格子的值（0 表示没有相邻雷，其他是 1~8）
        result.append((row, col, self.board[row][col]))
        return result
    
    def toggle_flag(self, row, col):
        """切换格子的旗子状态，只有格子未被揭示时才允许标记旗子"""
        if not self.revealed[row][col]:
            self.flags[row][col] = not self.flags[row][col]

    def get_public_board(self):
        """获取公开的棋盘，返回已揭示的格子内容，未揭示的格子为 None"""
        return [[
            self.board[r][c] if self.revealed[r][c] else None
            for c in range(self.cols)
        ] for r in range(self.rows)]

    def get_flagged_board(self):
        """获取标记旗子的棋盘，已标记的格子为 'F'，其他为 None"""
        return [[
            "F" if self.flags[r][c] else None
            for c in range(self.cols)
        ] for r in range(self.rows)]

    def check_game_status(self):
        """检查游戏状态，返回 'Game Over', 'You Win' 或 'Game in Progress'"""
        if self.game_over:
            return "Game Over"  # 游戏失败
        # 检查是否所有没有地雷的格子都已揭示
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and not self.revealed[r][c]:
                    return "Game in Progress"
        return "You Win"  # 所有非地雷格子都被揭示，玩家获胜
