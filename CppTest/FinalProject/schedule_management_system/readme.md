# 日程管理系统

## 需求分析

使用C++语言，单文件，命令行程序，尽可能仅使用标准库

### 原始要求

设计一个有用户交互的程序，要求:

- 程序有引导用户使用的菜单，例如:
“请选择:1.插入 2.删除 3.查询 4.修改 5.展示 0.退出”;
- 用户可以多次输入，直到满足指定条件才退出程序;
- 必须体现使用多态、运算符重载等技术;

### 设计要求

完成一个日程管理系统

1. 可以从json拉取日程记录，也可以将日程存入json文件
2. 可以添加日程、修改日程、查询日程（指定日期或时间范围内），展示日程可以用重载<进行sort排序，也可以按顺序显示所有日程
日程输出可以重载<<进行插入输出
3. 日程含有日程类型（会议、提醒、任务等）和详细信息（时间、内容和类型特有信息（可以体现多态）