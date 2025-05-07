def FacSum(n):
    if n == 1:
        return 0
    sum_factors = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            if i == n // i:
                sum_factors += i
            else:
                sum_factors += i + n // i
    return sum_factors

x = int(input())
pairs = set()

for a in range(2, x):
    b = FacSum(a)
    if b > a and FacSum(b) == a:
        pairs.add((a, b))

for pair in sorted(pairs):
    print(f"亲密数对: A={pair[0]:4}, B={pair[1]:4}")