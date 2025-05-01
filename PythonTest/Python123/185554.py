def mean(numtuple):
    s = 0.0
    for num in numtuple:
        s = s + num
    return s/ len(numtuple)
#请输入一个列表：
ls = eval(input())
print("average: "+"{:.1f}".format(mean(ls)))