# scores = []
# for i in range(10):
#     scores.append(float(input()))
scores = [8.5, 9, 9, 10, 7, 8, 8, 9, 8, 10]
scores.sort()
scores = scores[1:-1]
average = sum(scores) / len(scores)
print(f"{average:.2f}")