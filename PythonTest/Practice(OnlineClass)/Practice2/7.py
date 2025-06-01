s = input().strip()
sorted_s = sorted(filter(lambda x: x!=" ", s))
print(' '.join(sorted_s))