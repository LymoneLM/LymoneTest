import math

r = float(input())
h = float(input())
S = 2 * math.pi * r * (r + h)
V = math.pi * r * r * h
print(f"{S:.2f}")
print(f"{V:.2f}")