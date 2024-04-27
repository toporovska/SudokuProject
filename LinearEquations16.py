from sympy import symbols, solve, Eq
#this program solves sudoku by creating linear equations and solving them
#for matrix 4*4

x = [symbols(f'x{i}') for i in range(16)]

sudoku = [
    1, 4, 0, 0,
    2, 0, 3, 1,
    0, 1, 0, 0,
    4, 0, 1, 0
]

F = []

for xi in x:
    F.append(xi*(xi-1)*(xi-2)*(xi-3)*(xi-4))


for i in range(4):
    F.append(Eq(sum(x[i*4+j] for j in range(4)), 10))
    F.append(Eq(sum(x[i+j*4] for j in range(4)), 10))


for index, value in enumerate(sudoku):
    if value != 0:
        F.append(Eq(x[index], value))


solution = solve(F, dict=True)
# print(solution)

#This is print of our solution
solution_dict = solution[0]
sorted_keys = sorted(solution_dict.keys(), key=lambda x: int(x.name[1:]))
sorted_values = [solution_dict[key] for key in sorted_keys]
n_rows = 4
for i in range(n_rows):
    row = sorted_values[i*n_rows:(i+1)*n_rows]
    print(' '.join(map(str, row)))