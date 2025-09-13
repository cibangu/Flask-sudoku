import sqlite3

DB_NAME = "sudoku.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puzzle TEXT,
            solution TEXT,
            current TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_game(puzzle, solution, current):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM game")  # une seule partie à la fois
    c.execute("INSERT INTO game (puzzle, solution, current) VALUES (?, ?, ?)",
              (str(puzzle), str(solution), str(current)))
    conn.commit()
    conn.close()

def load_game():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT puzzle, solution, current FROM game LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row if row else None