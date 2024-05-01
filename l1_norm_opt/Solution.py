import numpy as np
import cvxpy as cp
from l1_norm_opt.func import *
sudoku = np.array([4, 3, 0, 2, 6, 0, 7, 8, 1, 6, 8, 0, 0, 7, 0, 0, 9, 3, 0, 9, 7, 8, 0, 4, 0, 0, 2, 8, 2, 0, 1, 0, 5, 0, 4, 0, 0, 7, 4, 6, 0, 2, 0, 0, 5, 9, 0, 1, 7, 0, 3, 6, 2, 8, 0, 1, 0, 3, 2, 6, 8, 7, 0, 2, 4, 8, 9, 0, 7, 0, 3, 0, 7, 6, 3, 4, 0, 8, 2, 0, 0])
solved_sudoku = np.array([4, 3, 5, 2, 6, 9, 7, 8, 1, 6, 8, 2, 5, 7, 1, 4, 9, 3, 1, 9, 7, 8, 3, 4, 5, 6, 2, 8, 2, 6, 1, 9, 5, 3, 4, 7, 3, 7, 4, 6, 8, 2, 9, 1, 5, 9, 5, 1, 7, 4, 3, 6, 2, 8, 5, 1, 9, 3, 2, 6, 8, 7, 4, 2, 4, 8, 9, 5, 7, 1, 3, 6, 7, 6, 3, 4, 1, 8, 2, 5, 9])
def L1SudokuSolving(orgin_clues, guesses, iterCount, solution):
    sizeOfPuzzle = int(np.sqrt(len(orgin_clues)))
    rawGuesses = guesses
    guesses = arrange_clues(guesses)
    A = makingA(sizeOfPuzzle, rawGuesses)
    b = np.ones((A.shape[0], 1))
    m, n = A.shape
    x = cp.Variable(n)
    objective = cp.Minimize(cp.norm(x, 1))
    constraint = [A @ x == b]
    problem = cp.Problem(objective, constraint)
    problem.solve()
    iterationThresh = 10
    if iterCount >= iterationThresh:
        wrapped = wrapper(x.copy(), sizeOfPuzzle)
        sol = wrapped
    else:
        wrapped = wrapper(x.copy(), sizeOfPuzzle)
        number_wrong = checker(wrapped, solution)
        if number_wrong == 0:
            sol = wrapped
            return
        holder = rawGuesses
        x = np.transpose(x)
        x = x.reshape((9, 81), order = 'F')
        thres = 0.3
        for t in range(x.shape[1]):
            maxi = max(abs(x[:, t]))
            ind = np.argmax(abs(x[:, t]))
            if maxi >= thres and holder[t] < 0.99:
                holder[t] = ind
        fixed_rows = check_rows(holder, sizeOfPuzzle)
        fixed_columns = check_columns(holder, sizeOfPuzzle)
        fixed_boxes = check_boxes(holder, sizeOfPuzzle)
        for u in range(len(fixed_boxes)):
            if fixed_boxes[u] == 0 or fixed_columns[u] == 0 or fixed_rows[u] == 0:
                holder[u] = 0
            if orgin_clues[u] != 0:
                holder[u] = orgin_clues[u]
        number_wrong = checker(holder, solution)
        if number_wrong < 4:
            if number_wrong == 0:
                sol = wrapped
                return sol
            out = brute_solve(holder)
            sol = out
            return sol
        else:
            iter_count += 1
        checked_backwards = check_backwards(sizeOfPuzzle, holder, orgin_clues, solution)
        number_wrong = checker(checked_backwards, solution)
        if number_wrong < 4:
            if number_wrong == 0:
                sol = checked_backwards
                return sol
            out = brute_solve(checked_backwards)
            sol = out
            return sol
        checked_rl = check_right_left(sizeOfPuzzle, checked_backwards, orgin_clues, solution)
    
        number_wrong = checker(checked_rl, solution)
        if number_wrong < 4:
            if number_wrong == 0:
                sol = checked_rl
                return sol
            out = brute_solve(checked_rl)
            sol = out
            return sol

        checked_lr = check_left_right(sizeOfPuzzle, checked_rl, orgin_clues, solution)
        number_wrong = checker(checked_lr, solution)
        if number_wrong < 4:
            if number_wrong == 0:
                sol = checked_lr
                return sol
            out = brute_solve(checked_lr)
            sol = out
            return sol

        sol = L1SudokuSolving(orgin_clues, checked_lr, iter_count, solution)

    return sol


def brute_solve(puzz):
    bank = np.where(puzz == 0)[0]
    holder = puzz.copy()
    if len(bank) == 3:
        for i in range(1, 10):
            holder[bank[0]] = i
            for j in range(1, 10):
                holder[bank[1]] = j
                for k in range(1, 10):
                    holder[bank[2]] = k
                    rows_w0 = np.where(check_rows(holder.copy(), 9) == 0)[0]
                    if len(rows_w0) == 0:
                        boxs_w0 = np.where(check_boxes(holder.copy(), 9) == 0)[0]
                        if len(boxs_w0) == 0:
                            colm_w0 = np.where(check_columns(holder.copy(), 9) == 0)[0]
                            if len(colm_w0) == 0:
                                return holder
        return 0
    if len(bank) == 2:
        for i in range(1, 10):
            holder[bank[0]] = i
            for j in range(1, 10):
                holder[bank[1]] = j
                rows_w0 = np.where(check_rows(holder.copy(), 9) == 0)[0]
                if len(rows_w0) == 0:
                    boxs_w0 = np.where(check_boxes(holder.copy(), 9) == 0)[0]
                    if len(boxs_w0) == 0:
                        colm_w0 = np.where(check_columns(holder.copy(), 9) == 0)[0]
                        if len(colm_w0) == 0:
                            return holder
                        
        return 0
    if len(bank) == 1:
        for i in range(1, 10):
            holder[bank[0]] = i
            colm_w0 = np.where(check_columns(holder.copy(), 9) == 0)[0]
            if len(colm_w0) == 0:
                return holder
        return holder

def check_backwards(sizeOfPuzzle, clues ,oriClues, solution):
    pass
def check_right_left(sizeOfPuzzle, clues ,oriClues, solution):
    pass
def check_left_right(sizeOfPuzzle, clues ,oriClues, solution):
    pass
