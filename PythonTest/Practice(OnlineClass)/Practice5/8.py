def prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

a, b = map(int, input().split(','))
for num in range(a, b+1):
    if num % 2 == 0:
        for i in range(2, num//2 + 1):
            if prime(i) and prime(num - i):
                print(f"{num}={i}+{num-i}")
                break