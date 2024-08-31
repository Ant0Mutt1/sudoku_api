from fastapi import FastAPI, Query, HTTPException
from sudoku_grid import SudokuValid
import uvicorn

app = FastAPI()

@app.get("/")
def index():
    try:
        sudoku = SudokuValid()  
        sudoku_grid = sudoku.sudoku()  
        
        if not sudoku_grid or len(sudoku_grid) != 2:
            raise ValueError("The output of the sudoku() method is not valid.")

        grid_solucion = sudoku_grid[0]
        grid_sudoku = sudoku_grid[1]
        
        return {
            "value": grid_sudoku,
            "solution": grid_solucion
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

data = {
    "es": {
        "name": "Sudoku",
        "description": "El sudoku es un rompecabezas de lógica que se juega en una cuadrícula de 9x9 celdas, dividida en nueve cuadrículas más pequeñas de 3x3. El objetivo es llenar la cuadrícula con números del 1 al 9 de manera que:",
        "rules": [
            "Cada fila contenga todos los números del 1 al 9 sin repetir ninguno.",
            "Cada columna contenga todos los números del 1 al 9 sin repetir ninguno.",
            "Cada cuadrícula de 3x3 contenga todos los números del 1 al 9 sin repetir ninguno."
        ],
        "starting_conditions": "El juego comienza con algunos números ya colocados, y debes usar la lógica para llenar las celdas vacías sin romper las reglas.",
    },
    'en': {
        "name": "Sudoku",
        "description": "Sudoku is a logic puzzle played on a 9x9 grid, which is divided into nine smaller 3x3 grids. The objective is to fill the grid with numbers from 1 to 9 so that:",
        "rules": [
            "Each row contains all the numbers from 1 to 9 without repeating any.",
            "Each column contains all the numbers from 1 to 9 without repeating any.",
            "Each 3x3 grid contains all the numbers from 1 to 9 without repeating any."
        ],
        "starting_conditions": "The game starts with some numbers already placed, and you need to use logic to fill in the empty cells without breaking the rules.",
    }
}
@app.get('/rules')
def info(lang :str = Query("es", alias="lang")):
    try:
        if lang not in data:
            raise HTTPException(status_code=404, detail="Language not supported")
        return data[lang]       
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__=='__main__':
    uvicorn.run(app, host='localhost', port=8000)
