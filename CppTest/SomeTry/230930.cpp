#include <iostream>
#include <cmath> //建议使用CPP提供的头文件cmath替代math.h
using namespace std;
int main(){
    float a,b,c; //CPP中使用变量需要提前声明变量，变量作用范围取决于声明的位置
    cout<<"请输入A,B,C:";
    cin>>a>>b>>c;//cin中使用流提取运算符
    if(sqrt(b*b-4*a*c)>0){ //其实无需使用sqrt，可以改为b*b-4*a*c>0
        float x1=(-b+sqrt(b*b-4*a*c))/(2*a);//注意赋值符号，行末分号，变量名大小写敏感
        float x2=(-b-sqrt(b*b-4*a*c))/(2*a);
        cout<<"\n方程的解为："<<x1<<" "<<x2<<endl;
        //之前有输出，最好提前换行，换行建议使用CPP提供的endl
        //两个变量之前也要使用流插入运算符，最好输出一个空格方便查看输出
        //if后多行语句注意使用花括号扩起来成为语句块
    } else if (sqrt(b*b-4*a*c)==0){ 
        float x = -b/2*a;//赋值运算符
        //这里可以优化，其实可以和上一个if合并
        cout<<"\n方程的解为："<<x<<endl;
    } else { //else关键词没有判定语句，注意；并且此处并不需要判定
        cout<<"\n该方程无解";
    }
    getchar();//getchat可以阻止程序结束，但是请放在程序内return前
    return 0;//main函数在这里终止，等效于程序已经终止，之后的语句不会运行
}
//程序外的语句不会运行