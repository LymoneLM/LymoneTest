#include <ctime>
#include <iostream>
#include <string>
using namespace std;

// 定义学生结构体
struct Student {
    string name; // 学生姓名
    int score;   // 学生分数
};
struct Teacher {
    string name;              // 老师姓名
    struct Student sArray[5]; // 一个老师带五个学生
};
void allocateSpace(Teacher tArray[], int len) {
    string nameSeed = "ABCDE";
    for (int i = 0; i < len; ++i) {
        // tArray[i].name = "Teacher_" + nameSeed[i];

        tArray[i].name = "Teacher_";
        tArray[i].name += nameSeed[i];
        for (int j = 0; j < 5; ++j) {
            int random = rand() % 100; // 生成随机数函数，伪随机，数字一旦生成就不会改变
            tArray[i].sArray[j].name = string("Student_") + nameSeed[j];
            tArray[i].sArray[j].score = random;
        }
    }
}
void printInfo(Teacher tArray[], int len) {
    for (int i = 0; i < len; ++i) {
        cout << "老师姓名： " << tArray[i].name << endl;
        for (int j = 0; j < 5; ++j) {
            cout << "\t学生姓名： " << tArray[i].sArray[j].name << " 考试分数： " << tArray[i].sArray[j].score << endl;
        }
    }
}

int main() {
    // 添加随机数种子，利用当前系统时间生成随机数，防止每次随机数都一样
    srand((unsigned int)time(NULL));
    // 创建数组存放三名老师
    struct Teacher tArray[3];
    // 通过函数给每个老师及其所带学生赋值
    int len = sizeof(tArray) / sizeof(tArray[0]);
    allocateSpace(tArray, len);
    // 打印出老师数据及老师所带学生数据
    printInfo(tArray, len);
    system("pause");
    return 0;
}
