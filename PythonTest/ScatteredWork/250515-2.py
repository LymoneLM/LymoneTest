def is_prime(x):
    for i in range(2,x):
        if x % i == 0:
            return False
    return True

s = []
for i in range(2,101):
    if is_prime(i):
        s.append(str(i))

with open("sy8-3.txt","w") as f:
    f.write(", ".join(s))