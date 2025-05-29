s = input()
letter = digit = other = 0
for ch in s:
    if ch.isalpha():
        letter += 1
    elif ch.isdigit():
        digit += 1
    else:
        other += 1
print(f"letter = {letter}, digit = {digit}, other = {other}")