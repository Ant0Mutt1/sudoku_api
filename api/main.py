from fastapi import FastAPI
from .sudoku_grid import SudokuValid

app = FastAPI()

@app.get("/")
def index():
    sudoku= SudokuValid()
    sudoku_grid = sudoku.sudoku()
    grid_solucion = sudoku_grid[0]
    grid_sudoku = sudoku_grid[1]
    return {
        "valores":grid_sudoku,
        "solucion": grid_solucion
    }