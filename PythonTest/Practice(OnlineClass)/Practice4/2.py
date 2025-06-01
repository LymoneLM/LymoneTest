N = int(input())
K = 0
sum_squares = 0

while True:
    K += 1
    sum_squares += K * K
    if sum_squares >= N:
        K -= 1
        break

print(f"最大K值是{K}")