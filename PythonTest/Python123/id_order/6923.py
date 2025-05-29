import turtle
def koch(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        for angle in [0, 60, -120, 60]:
           turtle.left(angle)
           koch(size/3, n-1)

def main(level):
    turtle.setup(600,600)
    turtle.penup()
    turtle.goto(-200, 100)
    turtle.speed(500)
    turtle.pendown()
    turtle.pensize(2)
    koch(400,level)
    turtle.right(120)
    koch(400,level)
    turtle.right(120)
    koch(400,level)
    turtle.hideturtle()

try:
    level = eval(input("请输入科赫曲线的阶: "))
    main(level)
except:
    print("输入错误")