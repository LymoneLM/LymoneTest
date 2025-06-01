n = int(input())

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

sum_primes = sum(num for num in range(2, n) if is_prime(num))
print(sum_primes)