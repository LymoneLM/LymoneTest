def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


a = eval(input())
b = eval(input())
s = []
calcu = 0
for i in range(a, b + 1):
    if is_prime(i):
        s.append(f"{i}*{i}")
        calcu += i * i
print("+".join(s), end="=")
print(calcu)
