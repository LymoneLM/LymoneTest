import random
import csv
s = [[random.randint(0, 100) for _ in range(5)] for _ in range(5)]
with open(r".\sy8-4.csv","w",newline="") as f:
    csv.writer(f).writerows(s)