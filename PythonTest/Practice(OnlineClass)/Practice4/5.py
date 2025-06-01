n = int(input())
result = []

for num in range(100, n + 1):
    a = num // 100
    b = (num // 10) % 10
    c = num % 10
    if num == a**3 + b**3 + c**3:
        result.append(str(num))

print(' '.join(result))