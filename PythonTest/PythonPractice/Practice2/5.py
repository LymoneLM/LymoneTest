input = input()
list = input.split(',')
num = 1
for i in input:
    if i==",":
        num+=1
print(f"{len(list)} {num}")