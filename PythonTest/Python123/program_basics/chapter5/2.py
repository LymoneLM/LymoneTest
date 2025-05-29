def odds(s):
    new_s = []
    for i in range(len(s)):
        if i % 2 == 1:
            new_s.append(s[i])
    return new_s


a = [1, 2, 3, 4, 5]
b = [7, 8, 9, 10, 12, 13]
print(odds(a))
print(odds(b))