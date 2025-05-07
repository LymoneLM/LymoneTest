import math

x = eval(input())
sin_x = 0
n = 1
term = x

while abs(term) >= 1e-6:
    sin_x += term
    n += 1
    term = (-1)**(n+1) * x**(2*n - 1) / math.factorial(2*n - 1)

print(f"sin({x})的近似值为:{sin_x}")