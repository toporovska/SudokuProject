from sympy import groebner, symbols, Eq

#this program solves sudoku by use groebner algorithm
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
    F.append(Eq(sum(x[i*9+j] for j in range(9)), 45))  # Sum of each row equals 45
    F.append(Eq(sum(x[i+j*9] for j in range(9)), 45))  # Sum of each column equals 45

for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        F.append(Eq(sum(x[i*9+j+k+9*l] for k in range(3) for l in range(3)), 45))  # Sum of each 3x3 subgrid equals 45

for index, value in enumerate(sudoku):
    if value != 0:
        F.append(Eq(x[index], value))

solution = groebner(F)

# Extract and print the solution
values = {}
for poly in solution:
    if poly.is_linear and poly.gens[0] in x:
        var = poly.gens[0]
        value = -poly.coeffs()[0] / poly.coeffs()[1] if poly.coeffs()[1] != 0 else 0
        values[var] = int(value)

sorted_keys = sorted(values.keys(), key=lambda k: (int(str(k)[1:]), int(str(k)[2:])))
sorted_values = [values[key] for key in sorted_keys]

n_rows = 9
for i in range(n_rows):
    row_values = sorted_values[i*n_rows:(i+1)*n_rows]
    print(' '.join(map(str, row_values)))
