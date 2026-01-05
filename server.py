import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dlxsudoku import Sudoku

app = FastAPI()

class SudokuRequest(BaseModel):
    # 81-char string like "530070000..." or list of 9 strings
    puzzle: str

class SudokuResponse(BaseModel):
    solution: str

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/solve", response_model=SudokuResponse)
def solve(req: SudokuRequest):
    puzzle = req.puzzle.strip()
    if len(puzzle) != 81:
        raise HTTPException(status_code=400, detail="Puzzle must be an 81-character string")
    try:
        s = Sudoku(puzzle)
        solved = s.solve()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not solved:
        raise HTTPException(status_code=422, detail="Puzzle is unsolvable")
    return SudokuResponse(solution=str(s))
