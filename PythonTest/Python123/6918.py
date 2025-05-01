for i in range(3):
    a, b = input(), input()
    if a == 'Kate' and b == '666666':
        print("登录成功！")
        break
    if i == 2:
        print("3次用户名或者密码均有误！退出程序。")

