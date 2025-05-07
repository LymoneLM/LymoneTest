n = int(input())
m = list(map(int, input().split()))
x = list(map(int, input().split()))
current = {0}
for i in range(n):
    mi = m[i]
    xi = x[i]
    current = {w + k * mi for w in current for k in range(xi + 1)}
print(len(current))
