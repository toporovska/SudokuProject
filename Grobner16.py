from sympy import groebner, symbols,  Eq
#this program solves sudoku by use groebner algorithm
#for matrix 4*4

x = [symbols(f'x{i}') for i in range(16)]

sudoku = [
    1, 3, 0, 0,
    2, 4, 3, 1,
    0, 1, 2, 0,
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


solution = groebner(F)

#This is a reflection of our solution
values = {}
for poly in solution:
    if poly.as_poly().degree() == 1 and poly.as_poly().gens[0] in x:
        var = poly.as_poly().gens[0]
        value = -poly.as_poly().coeffs()[1] / poly.as_poly().coeffs()[0] if poly.as_poly().coeffs()[0] != 0 else 0
        values[var] = int(value)

sorted_keys = sorted(values.keys(), key=lambda k: int(str(k)[1:]))
sorted_values = [values[key] for key in sorted_keys]

n_rows = 4
for i in range(n_rows):
    row_values = sorted_values[i*n_rows:(i+1)*n_rows]
    print(' '.join(map(str, row_values)))
