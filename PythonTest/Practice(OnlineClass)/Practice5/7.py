def huiwen(num):
    return str(num) == str(num)[::-1]

M = int(input())
print(f"{M}{'是' if huiwen(M) else '不是'}回文数")