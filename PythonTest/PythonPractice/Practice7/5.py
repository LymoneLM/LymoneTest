# 1
n = int(input())
pri = 1
for i in range(0, n):
    pri += i
    num = pri
    print(num, end=" ")
    for j in range(i + 2, n + 1):
        num += j
        print(num, end=" ")
    print()
# 2
n = int(input())
matrix = [[0]*n for _ in range(n)]
num = 1
for d in range(n):
    i = d
    j = 0
    while i >= 0:
        matrix[i][j] = num
        num += 1
        i -= 1
        j += 1
for row in matrix:
    print(' '.join(map(str, filter(bool, row))),end=" \n")