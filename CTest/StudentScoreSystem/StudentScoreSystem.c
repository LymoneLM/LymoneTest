#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

//=====用于存储成绩数据的结构体和枚举=====

struct Score
{
    double math, marx, c;
};
struct Student
{
    char stuNo[20];
    char name[30];
    Score usually, finally, total;
};
enum Subject
{
    math = 1,
    marx,
    c
}; // 枚举

//=====开辟存储数据的全局变量空间=====

Student data[10];  // 存储原始数据
Student data_[10]; // 用于存储排序后的数据
Score average;     // 存储数据data的平均成绩

//=====键盘录入数据有关函数=====

// 输入数据合法性检查(检查成绩部分)
bool scoreIsInLaw(int num)
{
    return num >= 0 && num <= 100;
}
// 输入数据合法性检查(检查学号部分)
// 参数1为已输入数据，参数2为待审查数据，参数3为当前已经输入的数据规模
bool stuNoIsInLaw(Student *p, char *stuNo, int max)
{
    while (max--)
        if (strcmp(p[max].stuNo, stuNo) == 0)
            return false;
    return true;
}
// 基本输入处理,同时简单的处理数据，获取该组数据的平均值等
void basicInput(Student *data, int max, Score *average)
{
    average->math = 0;
    average->marx = 0;
    average->c = 0;
    for (int i = 0; i < max; i++)
    {
        average->math += data[i].total.math = data[i].usually.math * 0.3 + data[i].finally.math * 0.7;
        average->marx += data[i].total.marx = data[i].usually.marx * 0.5 + data[i].finally.marx * 0.5;
        average->c += data[i].total.c = data[i].usually.c * 0.4 + data[i].finally.c * 0.6;
    }
    average->math /= 10;
    average->marx /= 10;
    average->c /= 10;
}
// 一次只输入一个数据
void oboInput(Student *data, int max)
{
    Student temp[10];
    for (int i = 0; i < max; i++)
    {
    q1:
        printf("请输入第%d位学生学号：", i + 1);
        scanf("%s", temp[i].stuNo);
        if (!stuNoIsInLaw(temp, temp[i].stuNo, i))
        {
            printf("第%d位学生学号重复，请检查后再次输入该数据\n", i + 1);
            scanf("%s", temp[i].stuNo);
            goto q1;
        }
        printf("请输入第%d位学生姓名：", i + 1);
        scanf("%s", temp[i].name);
    q2:
        printf("请输入第%d位学生高数平时成绩：", i + 1);
        scanf("%lf", &temp[i].usually.math);
        if (!scoreIsInLaw(temp[i].usually.math))
        {
            printf("第%d位学生高数平时成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].usually.math);
            goto q2;
        }
    q3:
        printf("请输入第%d位学生高数考试成绩：", i + 1);
        scanf("%lf", &temp[i].finally.math);
        if (!scoreIsInLaw(temp[i].finally.math))
        {
            printf("第%d位学生高数考试成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].finally.math);
            goto q3;
        }
    q4:
        printf("请输入第%d位学生马克思平时成绩：", i + 1);
        scanf("%lf", &temp[i].usually.marx);
        if (!scoreIsInLaw(temp[i].usually.marx))
        {
            printf("第%d位学生马克思平时成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].usually.marx);
            goto q4;
        }
    q5:
        printf("请输入第%d位学生马克思考试成绩：", i + 1);
        scanf("%lf", &temp[i].finally.marx);
        if (!scoreIsInLaw(temp[i].finally.marx))
        {
            printf("第%d位学生马克思考试成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].finally.marx);
            goto q5;
        }
    q6:
        printf("请输入第%d位学生C语言平时成绩：", i + 1);
        scanf("%lf", &temp[i].usually.c);
        if (!scoreIsInLaw(temp[i].usually.c))
        {
            printf("第%d位学生C语言平时成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].usually.c);
            goto q6;
        }
    q7:
        printf("请输入第%d位学生C语言考试成绩：", i + 1);
        scanf("%lf", &temp[i].finally.c);
        if (!scoreIsInLaw(temp[i].finally.c))
        {
            printf("第%d位学生C语言考试成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].finally.c);
            goto q7;
        }
    }
    for (int i = 0; i < max; i++)
    {
        data[i] = temp[i];
    }
}
// 一次输入一行
void oilInput(Student *data, int max)
{
    char stuNo[20];
    char name[30];
    double math, math_, marx, marx_, c, c_;
    for (int i = 0; i < max; i++)
    {
        printf("请按照\n学号 姓名 高数平时成绩 高数考试成绩 马克思平时成绩 马克思考试成绩 C语言平时成绩 C语言考试成绩\n的顺序录入第%d名学生的成绩:\n", i + 1);
    loop:
        scanf("%s%s%lf%lf%lf%lf%lf%lf", stuNo, name, &math, &math_, &marx, &marx_, &c, &c_);
        if (stuNoIsInLaw(data, stuNo, i))
            strcpy(data[i].stuNo, stuNo);
        else
        {
            printf("学号重复，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
        strcpy(data[i].name, name);
        if (scoreIsInLaw(math))
            data[i].usually.math = math;
        else
        {
            printf("高数平时成绩错误，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
        if (scoreIsInLaw(math_))
            data[i].finally.math = math_;
        else
        {
            printf("高数考试成绩错误，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
        if (scoreIsInLaw(marx))
            data[i].usually.marx = marx;
        else
        {
            printf("马克思平时成绩错误，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
        if (scoreIsInLaw(marx_))
            data[i].finally.marx = marx_;
        else
        {
            printf("马克思考试成绩错误，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
        if (scoreIsInLaw(c))
            data[i].usually.c = c;
        else
        {
            printf("C语言平时成绩错误，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
        if (scoreIsInLaw(c_))
            data[i].finally.c = c_;
        else
        {
            printf("C语言考试成绩错误，请检查后再次输入该学生全部数据\n");
            goto loop;
        }
    }
}
// 一次输入全部数据
void aaoInput(Student *data, int max)
{
    Student temp[10];
    char stuNo[20];
    char name[30];
    double math, math_, marx, marx_, c, c_;
    for (int i = 0; i < max; i++)
    {
        scanf("%s%s%lf%lf%lf%lf%lf%lf", stuNo, name, &math, &math_, &marx, &marx_, &c, &c_);
        strcpy(temp[i].stuNo, stuNo);
        strcpy(temp[i].name, name);
        temp[i].usually.math = math;
        temp[i].finally.math = math_;
        temp[i].usually.marx = marx;
        temp[i].finally.marx = marx_;
        temp[i].usually.c = c;
        temp[i].finally.c = c_;
    }
    for (int i = 0; i < max; i++)
    {
    q1:
        if (!stuNoIsInLaw(temp, temp[i].stuNo, i))
        {
            printf("第%d位学生学号重复，请检查后再次输入该数据\n", i + 1);
            scanf("%s", temp[i].stuNo);
            goto q1;
        }
    q2:
        if (!scoreIsInLaw(temp[i].usually.math))
        {
            printf("第%d位学生高数平时成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].usually.math);
            goto q2;
        }
    q3:
        if (!scoreIsInLaw(temp[i].finally.math))
        {
            printf("第%d位学生高数考试成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].finally.math);
            goto q3;
        }
    q4:
        if (!scoreIsInLaw(temp[i].usually.marx))
        {
            printf("第%d位学生马克思平时成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].usually.marx);
            goto q4;
        }
    q5:
        if (!scoreIsInLaw(temp[i].finally.marx))
        {
            printf("第%d位学生马克思考试成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].finally.marx);
            goto q5;
        }
    q6:
        if (!scoreIsInLaw(temp[i].usually.c))
        {
            printf("第%d位学生C语言平时成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].usually.c);
            goto q6;
        }
    q7:
        if (!scoreIsInLaw(temp[i].finally.c))
        {
            printf("第%d位学生C语言考试成绩错误，请检查后再次输入该数据\n", i + 1);
            scanf("%lf", &temp[i].finally.c);
            goto q7;
        }
    }
    for (int i = 0; i < max; i++)
    {
        data[i] = temp[i];
    }
}

//=====排序有关功能的函数=====

// 比较函数
bool cmp(Student *A, Student *B, Subject kind)
{
    switch (kind)
    {
    case math:
        return A->total.math < B->total.math;
    case marx:
        return A->total.marx < B->total.marx;
    case c:
    default:
        break;
    }
    return A->total.c < B->total.c; // 默认匹配方案
}
// 快排递归函数
void quick_sort(Student *s, int l, int r, Subject kind)
{
    if (l < r)
    {
        int i = l, j = r;
        Student x = s[l]; // 记录第一个数为“基准”
        while (i < j)
        {
            while (i < j && cmp(&s[j], &x, kind)) // 从下向上找第一个大于等于“基准”的数
                j--;
            if (i < j)
                s[i++] = s[j];
            while (i < j && !cmp(&s[i], &x, kind)) // 从上向下找第一个小于“基准”的数
                i++;
            if (i < j)
                s[j--] = s[i];
        } // 结果一定是i==j
        s[i] = x;
        quick_sort(s, l, i - 1, kind); // 递归调用前半部分
        quick_sort(s, i + 1, r, kind); // 递归调用后半部分
    }
}
// 核心排序函数
// 参数1为待排序数据，参数2用于存放排序结果，参数3数据规模，参数4为排序类型
// 该函数排序算法思想为快速排序（Quicksort）时间复杂度期望O(nlogn)
void sort(Student *source, Student *dest, int max, Subject kind)
{
    for (int i = 0; i < max; i++)
        dest[i] = source[i];
    quick_sort(dest, 0, 9, kind);
}

//=====文件读写有关功能的函数=====

// 从文件读入
// 参数依次为文件名、待写入数据、数据规模
bool readFile(char *filename, Student *p, int max)
{
    Student temp[10];
    char stuNo[20];
    char name[30];
    double math, math_, marx, marx_, c, c_;
    int reCode;
    strcat(filename, ".studentdb");
    FILE *rFile = fopen(filename, "r");
    if (rFile == NULL)
        return false;
    for (int i = 0; i < max; i++)
    {
        reCode = fscanf(rFile, "%s%s%lf%lf%lf%lf%lf%lf", stuNo, name, &math, &math_, &marx, &marx_, &c, &c_);
        if (reCode == EOF)
        {
            fclose(rFile);
            return false;
        }
        strcpy(temp[i].stuNo, stuNo);
        strcpy(temp[i].name, name);
        temp[i].usually.math = math;
        temp[i].finally.math = math_;
        temp[i].usually.marx = marx;
        temp[i].finally.marx = marx_;
        temp[i].usually.c = c;
        temp[i].finally.c = c_;
    }
    bool flag = true;
    for (int i = 0; i < max; i++)
    {
        if (!stuNoIsInLaw(temp, temp[i].stuNo, i))
            flag = false;
        if (!scoreIsInLaw(temp[i].usually.math))
            flag = false;
        if (!scoreIsInLaw(temp[i].finally.math))
            flag = false;
        if (!scoreIsInLaw(temp[i].usually.marx))
            flag = false;
        if (!scoreIsInLaw(temp[i].finally.marx))
            flag = false;
        if (!scoreIsInLaw(temp[i].usually.c))
            flag = false;
        if (!scoreIsInLaw(temp[i].finally.c))
            flag = false;
    }
    if (!flag)
    {
        fclose(rFile);
        return false;
    }
    for (int i = 0; i < max; i++)
    {
        p[i] = temp[i];
    }
    fclose(rFile);
    return true;
}
// 写入到文件
// 参数依次为文件名、待写入数据、数据规模
bool writeFile(char *filename, Student *p, int max)
{
    int reCode;
    strcat(filename, ".studentdb");
    FILE *rFile = fopen(filename, "r+");
    if (rFile == NULL)
        rFile = fopen(filename, "w+");
    for (int i = 0; i < max; i++)
    {
        reCode = fprintf(rFile, "%s %s %.3lf %.3lf %.3lf %.3lf %.3lf %.3lf\n", p[i].stuNo, p[i].name, p[i].usually.math, p[i].finally.math, p[i].usually.marx, p[i].finally.marx, p[i].usually.c, p[i].finally.c);
        if (reCode < 0)
        {
            fclose(rFile);
            return false;
        }
    }
    fclose(rFile);
    return true;
}

//=====打印输出有关函数=====

// 打印学生成绩
// 参数1为打印的学生数据数组头指针，参数2为数据规模
void dataPrint(Student *p, int max)
{
    printf("学号\t\t姓名\t\t高数\t马克思\tC语言\n");
    for (int i = 0; i < max; i++)
        printf("%s\t\t%s\t\t%.2lf\t%.2lf\t%.2lf\n", p[i].stuNo, p[i].name, p[i].total.math, p[i].total.marx, p[i].total.c);
}
// 输出3门课程低于平均分的学生个数
// 参数1为待统计学生数据，参数2为数据规模，参数3为平均数据
void underlineNumPrint(Student *p, int max, Score *avg)
{
    int math = 0, marx = 0, c = 0;
    for (int i = 0; i < max; i++)
    {
        if (p[i].total.math < avg->math)
            math++;
        if (p[i].total.marx < avg->marx)
            marx++;
        if (p[i].total.c < avg->c)
            c++;
    }
    printf("\t\t高数\t马克思\tC语言\n");
    printf("平均分\t\t%.2lf\t%.2lf\t%.2lf\n", avg->math, avg->marx, avg->c);
    printf("低于平均分人数\t%d\t%d\t%d\n", math, marx, c);
}

//=====命令行伪图形界面/菜单绘制函数=====
// 因为有互相调用的问题，所以这部分函数在前部提前进行声明

// 输出程序初始化界面
void Awake();
// 菜单输出函数，仅用于输出，提高代码可读性、重用率
// 参数1为菜单条数，参数2为菜单内容
inline void Menu(int num, char content[][50])
{
    for (int i = 0; i < num; i++)
        printf("%s\n", content[i]);
}
// 输出主要功能菜单
void MainMenu();
// 输出键盘输入方式菜单
void InputMenu();
// 数据处理有关功能菜单
void CalcuMenu();
// 排序方案选择菜单
void SortKindMenu();
// 暂停
inline void PauseLine()
{
    getchar();
    printf("按任意键以继续……");
    getchar();
}

void Awake()
{
    int line = 5;
    char title[][50] = {
        "    ====================",
        "    |    欢迎使用      |",
        "    | 学生成绩录入系统 |",
        "    |        Ver1.0.0  |",
        "    ===================="};
    Menu(line, title);
    Sleep(300);
}
void MainMenu()
{
    int numFunction = 3; // 功能的数量
    char nameFunction[][50] = {
        "1、直接从键盘录入学生成绩数据",
        "2、从文件读取学生成绩数据",
        "3、读取最后一次录入的成绩"};
    {
        char bar[] = "-\\|/";
        printf("     正在载入功能菜单 ");
        for (int i = 0; i < 15; i++)
        {
            Sleep(100);
            printf("\b%c", bar[i % 4]);
        }
    } // 模拟进度条的语句块，用于提高程序连贯性
    printf("\n\n请输入对应功能的编号以使用功能\n");
    Menu(numFunction, nameFunction);
    int temp;
loop:
    scanf("%d", &temp);
    switch (temp)
    {
    case 1:
        system("cls");
        InputMenu();
        break;
    case 2:
    {
        char filename[50];
        printf("请键入文件名（无需包含扩展名）：\n");
        scanf("%s", filename);
        if (!readFile(filename, data, 10))
        {
            printf("读取失败：输入的文件名错误或文件数据损坏\n");
            PauseLine();
            system("cls");
            MainMenu();
        }
        else
        {
            printf("从文件%s读取数据成功\n", filename);
            basicInput(data, 10, &average);
            PauseLine();
            system("cls");
            CalcuMenu();
        }
    }
    break;
    case 3:
    {
        char filename[50] = "history";
        if (!readFile(filename, data, 10))
        {
            printf("读取失败：历史录入数据不存在或已损坏\n");
            PauseLine();
            system("cls");
            MainMenu();
        }
        else
        {
            printf("读取历史录入数据成功\n");
            basicInput(data, 10, &average);
            PauseLine();
            system("cls");
            CalcuMenu();
        }
    }
    break;
    default:
        printf("无效的选项，请重试\n");
        goto loop;
    }
}
void InputMenu()
{
    int numFunction = 3; // 功能的数量
    char nameFunction[][50] = {
        "1、按条目依次录入学生成绩",
        "2、每次录入一个学生所有成绩",
        "3、一次性录入所有学生成绩"};
    printf("[默认只录入10位学生的成绩]\n");
    printf("请选择录入方式：\n");
    Menu(numFunction, nameFunction);
    int temp;
loop:
    scanf("%d", &temp);
    switch (temp)
    {
    case 1:
        oboInput(data, 10);
        break;
    case 2:
        oilInput(data, 10);
        break;
    case 3:
        aaoInput(data, 10);
        break;
    default:
        printf("无效的选项，请重试\n");
        goto loop;
    }
    basicInput(data, 10, &average);
    PauseLine();
    system("cls");
    CalcuMenu();
}
void CalcuMenu()
{
    char _filename[50] = "history";
    writeFile(_filename, data, 10);
    int numFunction = 6; // 功能的数量
    char nameFunction[][50] = {
        "1、按录入顺序输出学生总成绩",
        "2、按照学科成绩顺序输出学生总成绩",
        "3、输出3门课程低于平均分学生个数",
        "4、重新录入学生成绩(覆盖现有记录)",
        "5、将录入的成绩保存为文件并退出",
        "6、直接退出学生成绩录入系统"};
    printf("已完成学生成绩录入\n");
    printf("请继续选择数据处理方式：\n");
    Menu(numFunction, nameFunction);
    int temp;
loop:
    scanf("%d", &temp);
    switch (temp)
    {
    case 1:
        system("cls");
        dataPrint(data, 10);
        PauseLine();
        system("cls");
        CalcuMenu();
        break;
    case 2:
        system("cls");
        SortKindMenu();
        dataPrint(data_, 10);
        PauseLine();
        system("cls");
        CalcuMenu();
        break;
    case 3:
        system("cls");
        underlineNumPrint(data, 10, &average);
        PauseLine();
        system("cls");
        CalcuMenu();
        break;
    case 4:
        system("cls");
        MainMenu();
        break;
    case 5:
    {
        char filename[50];
        printf("请键入文件名（如果重名会覆盖前一文件）：\n");
        scanf("%s", filename);
        writeFile(filename, data, 10);
    }
    break;
    case 6:
        break;
    default:
        printf("无效的选项，请重试\n");
        goto loop;
    }
}
void SortKindMenu()
{
    int numFunction = 3; // 功能的数量
    char nameFunction[][50] = {
        "1、按高数成绩排序",
        "2、按马克思成绩排序",
        "3、按C语言成绩排序",
    };
    printf("请选择排序方案(默认从高到低的排序):\n");
    Menu(numFunction, nameFunction);
    int temp;
loop:
    scanf("%d", &temp);
    switch (temp)
    {
    case math:
        printf("按照高数成绩排序如下：\n");
    case marx:
        printf("按照马克思成绩排序如下：\n");
    case c:
        printf("按照C语言成绩排序如下：\n");
        sort(data, data_, 10, Subject(temp));
        break;
    default:
        printf("无效的选项，请重试\n");
        goto loop;
    }
}

//=====主函数部分=====
int main()
{
    Awake();
    MainMenu();
    return 0;
}