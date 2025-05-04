def passed(score):
    if score < 0 or score > 100:
        return "输入的成绩错误！"
    elif score >= 60:
        return "该同学成绩合格啦！"
    else:
        return "该同学成绩不合格，需继续努力！"

score = int(input())
print(passed(score))