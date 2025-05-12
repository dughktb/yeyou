from flask import Flask, render_template, request, jsonify
from game import Minesweeper

app = Flask(__name__)

# 初始化游戏实例
game = Minesweeper(rows=10, cols=10, mines=20)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reveal', methods=['POST'])
def reveal():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    row = int(data['row'])
    col = int(data['col'])
    
    # 执行揭示格子操作
    result = game.reveal(row, col)
    
    # 获取当前的公共棋盘和旗子状态
    public_board = game.get_public_board()
    flagged_board = game.get_flagged_board()
    
    # 返回更新后的棋盘状态以及游戏状态
    status = game.check_game_status()
    return jsonify({
        'public_board': public_board,
        'flagged_board': flagged_board,
        'status': status,
        'result': result  # 包含揭示格子的结果
    })

@app.route('/flag', methods=['POST'])
def flag():
    data = request.get_json()  # 获取 JSON 数据
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    row = int(data['row'])
    col = int(data['col'])
    
    game.toggle_flag(row, col)
    
    # 获取当前的棋盘状态
    flagged_board = game.get_flagged_board()
    
    return jsonify({'flagged_board': flagged_board})

@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    return jsonify({'status': 'Game Reset'})

if __name__ == '__main__':
    app.run(debug=True)
