eps = float(input())
pi = 0
sign = 1
denominator = 1
term = 1

while abs(term) >= eps:
    pi += term
    sign *= -1
    denominator += 2
    term = sign / denominator

pi *= 4
print(f"近似值为:{pi}")