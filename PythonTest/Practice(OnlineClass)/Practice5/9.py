def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def is_palindrome(n):
    return str(n) == str(n)[::-1]

x = int(input())
count = 0
num = 2
result = []

while count < x:
    if is_prime(num) and is_palindrome(num):
        result.append(str(num))
        count += 1
    num += 1

for i in range(0, len(result), 10):
    print(','.join(result[i:i+10]) + ',')