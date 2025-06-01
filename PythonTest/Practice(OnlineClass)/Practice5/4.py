def coprime(a, b):
    while b:
        a, b = b, a % b
    return a == 1

a, b = map(int, input().split(','))
if coprime(a, b):
    print(f"{a}和{b}互质")
else:
    print(f"{a}和{b}不互质")