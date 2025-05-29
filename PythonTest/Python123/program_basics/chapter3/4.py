a, b = 1, 1
result = [a, b]
for _ in range(18):
    a, b = b, a + b
    result.append(b)
for i in result:
    print(i,end="，")