def resolve(n,x):
    if n == 0:
        return 1
    if n == 1:
        return x
    return ((2 * n - 1) * x * resolve(n - 1, x) - (n - 1) * resolve(n - 2, x))/n
n = int(input())
x = float(input())
print(f"Legendre多项式的值： {resolve(n,x)}")