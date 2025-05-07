m, n, k = int(input()), int(input()), int(input())
people = list(range(1, m + 1))
index = 0
for _ in range(n):
    index = (index + k - 1) % len(people)
    print(f"{people.pop(index)}号下船了")