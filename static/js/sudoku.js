let solution = null;

function newPuzzle(difficulty) {
    fetch(`/puzzle?difficulty=${difficulty}`)
        .then(res => res.json())
        .then(data => {
            solution = data.solution;
            renderBoard(data.puzzle);
        });
}

function loadGame() {
    fetch("/load")
        .then(res => res.json())
        .then(data => {
            if (data.puzzle) {
                solution = data.solution;
                renderBoard(data.current);
            } else {
                document.getElementById("message").innerText = "Aucune partie sauvegardée.";
            }
        });
}

function renderBoard(board) {
    const container = document.getElementById("sudoku-board");
    container.innerHTML = "";
    board.forEach((row, i) => {
        row.forEach((val, j) => {
            const input = document.createElement("input");
            input.type = "number";
            input.inputMode = "numeric";
            input.min = 1;
            input.max = 9;
            input.dataset.row = i;
            input.dataset.col = j;
            if (val !== 0) {
                input.value = val;
                input.readOnly = true;
                input.classList.add("bg-light");
            }
            container.appendChild(input);
        });
    });
}

function getBoard() {
    const inputs = document.querySelectorAll("#sudoku-board input");
    const board = Array.from({ length: 9 }, () => Array(9).fill(0));
    inputs.forEach(input => {
        const row = parseInt(input.dataset.row);
        const col = parseInt(input.dataset.col);
        const val = parseInt(input.value) || 0;
        board[row][col] = val;
    });
    return board;
}

function checkPuzzle() {
    fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board: getBoard() })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("message").innerText =
            data.errors.length === 0 ? "✅ Correct !" : "❌ Erreurs trouvées";
    });
}

function solvePuzzle() {
    fetch("/solve")
        .then(res => res.json())
        .then(data => renderBoard(data.solution));
}