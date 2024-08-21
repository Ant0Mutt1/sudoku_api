from fastapi import FastAPI
from sudoku_greed import SudokuGreed

app = FastAPI()

@app.get("/sudoku")
def index():
    sudoku_greed = SudokuGreed()
    greed_solucion = sudoku_greed.greed_solucion
    greed_sudoku = sudoku_greed.greed_sin_resolver
    return {
        "greed_sudoku":greed_sudoku,
        "greed_solucion": greed_solucion
    }