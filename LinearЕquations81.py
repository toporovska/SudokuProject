from sympy import symbols, solve, Eq

#this program solves sudoku by creating linear equations and solving them
#for matrix 9*9

x = [symbols(f'x{i}') for i in range(81)]

sudoku = [
    5, 3, 0, 0, 7, 0, 0, 0, 0,
    6, 0, 0, 1, 9, 5, 0, 0, 0,
    0, 9, 8, 0, 0, 0, 0, 6, 0,
    8, 0, 0, 0, 6, 0, 0, 0, 3,
    4, 0, 0, 8, 0, 3, 0, 0, 1,
    7, 0, 0, 0, 2, 0, 0, 0, 6,
    0, 6, 0, 0, 0, 0, 2, 8, 0,
    0, 0, 0, 4, 1, 9, 0, 0, 5,
    0, 0, 0, 0, 8, 0, 0, 7, 9
]

F = []

for xi in x:
    F.append(xi*(xi-1)*(xi-2)*(xi-3)*(xi-4)*(xi-5)*(xi-6)*(xi-7)*(xi-8)*(xi-9))


for i in range(9):
    F.append(Eq(sum(x[i*9+j] for j in range(9)), 45)) 
    F.append(Eq(sum(x[j*9+i] for j in range(9)), 45)) 

    for j in range(0, 9, 3):
        for k in range(0, 9, 3):
            F.append(Eq(sum(x[i*9+j+k] for i in range(3) for j in range(3)), 45))  


for index, value in enumerate(sudoku):
    if value != 0:
        F.append(Eq(x[index], value))


solution = solve(F, dict=True)

solution_dict = solution[0]
sorted_keys = sorted(solution_dict.keys(), key=lambda x: (int(x.name[1:]) // 9, int(x.name[1:]) % 9))
sorted_values = [solution_dict[key] for key in sorted_keys]

n_rows = 9
for i in range(n_rows):
    row = sorted_values[i*n_rows:(i+1)*n_rows]
    print(' '.join(map(str, row)))
