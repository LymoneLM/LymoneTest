import  csv
with open(r"sy8-2.csv", "r") as f:
    x = list(csv.reader(f))
x.insert(0, ["姓名", "班级", "语文", "数学", "英语"])
with open(r"sy8-2.csv", "w", newline="") as f:
    csv.writer(f).writerows(x)