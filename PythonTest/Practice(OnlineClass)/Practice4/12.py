M = int(input())
sequence = [1, 2, 3]
n = 3

while sequence[-1] <= M:
    next_value = sequence[-1] + sequence[-2] + sequence[-3]
    sequence.append(next_value)
    n += 1

print(f"数列从第{n}项开始，数值超过{M}。")
print(f"第{n}项的值为{sequence[-1]}。")