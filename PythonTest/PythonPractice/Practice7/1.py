s = input().strip()
c, f = 0, True
for i in s:
    if i == '(': c += 1
    elif i == ')':
        c -= 1
        if c < 0: f = False; break
print('配对成功' if f and c == 0 else '配对不成功')