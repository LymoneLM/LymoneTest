n = int(input())
S = 0
sign = 1
for i in range(1, 2*n, 2):
    S += sign * i
    sign *= -1
print(S)