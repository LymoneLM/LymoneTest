n = int(input())

for num in range(1, n + 1):
    square = num * num
    if str(num) == str(square)[-len(str(num)):] or str(num) == str(square):
        print(num)
