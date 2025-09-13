from flask import Flask, request, jsonify, render_template
from sudoku import generate_puzzle
from database import init_db, save_game, load_game
import ast

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/puzzle")
def puzzle():
    difficulty = request.args.get("difficulty", "medium")
    puzzle, solution = generate_puzzle(difficulty)
    save_game(puzzle, solution, puzzle)
    return jsonify({"puzzle": puzzle, "solution": solution})

@app.route("/load")
def load():
    data = load_game()
    if not data:
        return jsonify({"puzzle": None})
    puzzle, solution, current = map(ast.literal_eval, data)
    return jsonify({"puzzle": puzzle, "solution": solution, "current": current})

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    board = data.get("board")
    game = load_game()
    if not game:
        return jsonify({"errors": []})
    _, solution, _ = map(ast.literal_eval, game)
    errors = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0 and board[i][j] != solution[i][j]:
                errors.append({"row": i, "col": j})
    save_game(board, solution, board)
    return jsonify({"errors": errors})

@app.route("/solve")
def solve():
    game = load_game()
    if not game:
        return jsonify({"solution": None})
    _, solution, _ = map(ast.literal_eval, game)
    return jsonify({"solution": solution})

if __name__ == "__main__":
    app.run(debug=True)