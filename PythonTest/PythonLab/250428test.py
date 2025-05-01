n = int(input())
for i in range(n + 1):
    spaces = ' ' * (n - i)
    numbers = str(i) * (2 * i + 1)
    print(spaces + numbers)

# n = int(input())
for k in range(n + 1):
    spaces = ' ' * (2 * (n - k))
    digits = str(k) * (2 * k + 1)
    print(spaces + digits)