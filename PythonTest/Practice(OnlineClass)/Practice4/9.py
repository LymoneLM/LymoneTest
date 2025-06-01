import math

n = int(input())
pairs = []

for a in range(1, n + 1):
    for b in range(a + 1, n + 1):
        sum_ab = a + b
        diff_ab = b - a
        if math.sqrt(sum_ab) == int(math.sqrt(sum_ab)) and math.sqrt(diff_ab) == int(math.sqrt(diff_ab)):
            pairs.append((a, b))

print(f"{n}以内的自然数对有：")
for pair in pairs:
    print(pair[0], pair[1])

print(f"自然数对共有{len(pairs)}对。")