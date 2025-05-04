n = int(input())

for num in range(1, n + 1):
    sum_factors = 0
    for i in range(1, num):
        if num % i == 0:
            sum_factors += i
    if sum_factors == num:
        print(num)