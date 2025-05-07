n = int(input())
original = n
seen = set()
while n != 1 and n not in seen:
    seen.add(n)
    n = sum(int(d)**2 for d in str(n))
if n == 1:
    print("{}是快乐数字".format(original))
else:
    print("{}不是快乐数字".format(original))
