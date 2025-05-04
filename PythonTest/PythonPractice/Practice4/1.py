num = int(input())
original = num
reverse = 0

while num > 0:
    digit = num % 10
    reverse = reverse * 10 + digit
    num = num // 10

print(f"{original}的反序数是:{reverse}")