def is_odd(num):
    return num % 2 != 0

n = int(input())
print(f"{n}是{'奇数' if is_odd(n) else '偶数'}")