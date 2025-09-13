import random
import copy

def valid(board, num, pos):
    row, col = pos
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    box_x, box_y = col // 3, row // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_board(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if valid(board, num, (row, col)):
            board[row][col] = num
            if solve_board(board):
                return True
            board[row][col] = 0
    return False

def generate_full_board():
    board = [[0]*9 for _ in range(9)]
    solve_board(board)
    return board

def remove_cells(board, difficulty):
    difficulty_map = {"easy": 35, "medium": 45, "hard": 55}
    cells_to_remove = difficulty_map.get(difficulty, 45)
    puzzle = copy.deepcopy(board)
    for _ in range(cells_to_remove):
        i, j = random.randint(0, 8), random.randint(0, 8)
        while puzzle[i][j] == 0:
            i, j = random.randint(0, 8), random.randint(0, 8)
        puzzle[i][j] = 0
    return puzzle

def generate_puzzle(difficulty="medium"):
    board = generate_full_board()
    puzzle = remove_cells(board, difficulty)
    return puzzle, board