def fib(n):
    fib_list = []
    a, b = 1, 1
    for _ in range(n):
        fib_list.append(a)
        a, b = b, a + b
    return fib_list

n = int(input())
print(fib(n))