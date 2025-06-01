with open(r".\sy8-1a.txt", "r") as f:
    x = f.read().split(',')
    x = [eval(i) for i in x]
with open(r".\sy8-1b.txt", "w") as f:
    f.write(f"{max(x)}, {min(x)}, {sum(x)/len(x)}")