n = int(input())
for i in range(n + 1):
    spaces = ' ' * (n - i)
    numbers = str(i) * (2 * i + 1)
    print(spaces + numbers)