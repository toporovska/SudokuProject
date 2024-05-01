import numpy as np
def arrange_clues(A):
    clues_holder = []
    for i in range(len(A)):
        if A[i] > 0:
            clues_holder.extend([A[i], i + 1])
    clues = np.array(clues_holder)
    return clues

def get_a_clue(N, clues):
    holdM = []
    for i in range(0, len(clues), 2):
        holdV = np.zeros(N**3)
        val = clues[i]
        pos = clues[i + 1]
        holdV[N * pos - N + val - 1] = 1
        holdM.append(holdV)
    clueA = np.array(holdM)
    return clueA
def get_a_cell(N):
    cells = []

    for i in range(1, N**2 + 1):
        start_pos = (i - 1) * N
        cell = np.zeros(N**3)
        cell[start_pos:start_pos + N] = 1
        cells.append(cell)

    cellA = np.array(cells)
    return cellA
def Abox(N):
    I = np.eye(N)
    j = np.concatenate((I, I, I), axis=1)

    boxes = []
    for i in range(N):
        zeros_before = i * 3 * N
        zeros_after = N**3 - ((i + 3) * 3 * N) - 2 * ((N**2) - j.shape[1])
        box = np.hstack([
            np.zeros((N, zeros_before)),
            j,
            np.zeros((N, N**2 - j.shape[1])),
            j,
            np.zeros((N, N**2 - j.shape[1])),
            j,
            np.zeros((N, zeros_after))
        ])
        boxes.append(box)

    res = np.vstack(boxes)
    return res
def Acol(N):
    Inxn = np.eye(N)
    Ocoln = np.zeros((N, N**2 - N))
    col1 = np.hstack([Inxn, Ocoln] * N)
    colsMid = []
    for row in range(2, N):
        colTemp = np.zeros((N, N * (row - 1)))
        for i in range(1, N + 1):
            if i != 4:
                colTemp = np.hstack([colTemp, Inxn, Ocoln])
            else:
                colTemp = np.hstack([colTemp, Inxn])
        colTemp = np.hstack([colTemp, np.zeros((N, (N**2 - N) - N * (row - 1)))])
        colsMid.append(colTemp)
    colsMid = np.vstack(colsMid)
    colN = np.hstack([Ocoln, Inxn] * N)
    res = np.vstack([col1, colsMid, colN])
    return res
def Arow(N):
    Inxn = np.eye(N)
    row1 = np.hstack([Inxn] * N)
    row1 = np.hstack([row1, np.zeros((N, N**2 * (N - 1)))])
    rowsMid = []
    for row in range(2, N):
        rowTemp = np.zeros((N, (row - 1) * N**2))
        for j in range(1, N + 1):
            rowTemp = np.hstack([rowTemp, Inxn])
        rowTemp = np.hstack([rowTemp, np.zeros((N, N**3 - row * (N**2)))])
        rowsMid.append(rowTemp)
    rowsMid = np.vstack(rowsMid)
    rowN = np.hstack([np.zeros((N, N**2 * (N - 1))), np.hstack([Inxn] * N)])
    res = np.vstack([row1, rowsMid, rowN])
    return res
import numpy as np

def makingA(sizeOfPuzzle, clues):
    clues = arrange_clues(clues)
    AClue = get_a_clue(sizeOfPuzzle, clues)
    ACell = get_a_cell(sizeOfPuzzle)
    ABox = Abox(sizeOfPuzzle)
    ARow = Arow(sizeOfPuzzle)
    ACol = Acol(sizeOfPuzzle)

    A = np.vstack([ARow, ACol, ABox, ACell, AClue])
    return A

def wrapper(x, N):
    holder = np.zeros(N**2)
    x = np.transpose(x)
    x = x.reshape((N, 81), order = 'F')
    for i in range(len(holder)):
        idx = np.argmax(x[:, i])
        holder[i] = idx+1
    return holder

def checker(correct, answers):
    count = 0
    for i in range(len(answers)):
        if correct[i] != answers[i]:
            count += 1
    return count

def check_columns(rawClues, sizeOfPuzzle):
    rawClues = np.transpose(rawClues)
    puzz = rawClues.reshape(sizeOfPuzzle, sizeOfPuzzle, order = "f")
    for j in range(sizeOfPuzzle):
        _, ind = np.unique(puzz[:, j], axis=0, return_index=True)
        duplicate_ind = np.setdiff1d(np.arange(puzz.shape[0]), ind)
        duplicate_value = puzz[duplicate_ind, j]

        if len(duplicate_value) < sizeOfPuzzle - 2:
            for p in range(sizeOfPuzzle):
                for b in range(len(duplicate_value)):
                    if puzz[p, j] == duplicate_value[b]:
                        puzz[p, j] = 0

    fixedColms = np.reshape(puzz, (1, sizeOfPuzzle**2), order = "f")
    return fixedColms

def check_rows(raw_clues, size_of_puzzle):
    raw_clues = np.transpose(raw_clues)
    puzz = raw_clues.reshape(size_of_puzzle, size_of_puzzle, order = "f").T
    fixed_rows = np.copy(puzz)

    for j in range(size_of_puzzle):
        _, ind = np.unique(puzz[:, j], return_index=True)
        duplicate_ind = np.setdiff1d(np.arange(puzz.shape[0]), ind)
        duplicate_values = puzz[duplicate_ind, j]
        if len(duplicate_values) < size_of_puzzle - 2:
            for p in range(size_of_puzzle):
                for b in range(len(duplicate_values)):
                    if puzz[p, j] == duplicate_values[b]:
                        fixed_rows[p, j] = 0

    fixed_rows = np.reshape(fixed_rows.T, size_of_puzzle**2, order = "f")
    return fixed_rows

def check_boxes(raw_clues, size_of_puzzle):
    puzz = np.reshape(raw_clues, (size_of_puzzle, size_of_puzzle)).T
    puzz = shape_box(puzz)
    
    # Moving through each column
    for j in range(size_of_puzzle):
        # Checking each row for duplicates
        _, ind = np.unique(puzz[:, j], axis=0, return_index=True)
        duplicate_ind = np.setdiff1d(np.arange(puzz.shape[0]), ind)
        duplicate_value = puzz[duplicate_ind, j]
        if len(duplicate_value) == 1:
            for p in range(size_of_puzzle):
                for b in range(len(duplicate_value)):
                    if puzz[p, j] == duplicate_value[b]:
                        puzz[p, j] = 0
        
    boxes = unshape_box(puzz)
    fixed_boxes = np.reshape(boxes.T, size_of_puzzle ** 2)
    return fixed_boxes

def shape_box(puzz):
    temp = puzz.copy()

    puzz[0:3, 0] = temp[0, 0:3]
    puzz[3:6, 0] = temp[1, 0:3]
    puzz[6:9, 0] = temp[2, 0:3]
    
    puzz[0:3, 1] = temp[0, 3:6]
    puzz[3:6, 1] = temp[1, 3:6]
    puzz[6:9, 1] = temp[2, 3:6]
    
    puzz[0:3, 2] = temp[0, 6:9]
    puzz[3:6, 2] = temp[1, 6:9]
    puzz[6:9, 2] = temp[2, 6:9]
    
    puzz[0:3, 3] = temp[3, 0:3]
    puzz[3:6, 3] = temp[4, 0:3]
    puzz[6:9, 3] = temp[5, 0:3]
    
    puzz[0:3, 4] = temp[3, 3:6]
    puzz[3:6, 4] = temp[4, 3:6]
    puzz[6:9, 4] = temp[5, 3:6]
    
    puzz[0:3, 5] = temp[3, 6:9]
    puzz[3:6, 5] = temp[4, 6:9]
    puzz[6:9, 5] = temp[5, 6:9]
    
    puzz[0:3, 6] = temp[6, 0:3]
    puzz[3:6, 6] = temp[7, 0:3]
    puzz[6:9, 6] = temp[8, 0:3]
    
    puzz[0:3, 7] = temp[6, 3:6]
    puzz[3:6, 7] = temp[7, 3:6]
    puzz[6:9, 7] = temp[8, 3:6]
    
    puzz[0:3, 8] = temp[6, 6:9]
    puzz[3:6, 8] = temp[7, 6:9]
    puzz[6:9, 8] = temp[8, 6:9]
    
    return puzz

def unshape_box(puzz):
    temp = puzz.copy()
    
    reshaped = np.zeros((9, 9))
    for i in range(9):
        row_block = i // 3
        col_block = i % 3
        reshaped[3 * row_block:3 * (row_block + 1), 3 * col_block:3 * (col_block + 1)] = temp[:, i].reshape(3, 3)
    
    return reshaped



