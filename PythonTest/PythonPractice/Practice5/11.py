# 递推法
def iterative_f(n):
    total = 0.0
    for i in range(1, n+1):
        total += i / (2*i + 1)
    return total

# 递归法
def recursive_f(n):
    if n == 0:
        return 0.0
    return n / (2*n + 1) + recursive_f(n-1)

n = int(input())
print(f"递推法f({n})={iterative_f(n)}")
print(f"递归法f({n})={recursive_f(n)}")