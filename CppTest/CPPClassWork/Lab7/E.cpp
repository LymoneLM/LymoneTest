/*
问题 E: 员工类（继承与派生）
[命题人 : liuhouquan]
时间限制 : 1.000 sec  内存限制 : 128 MB

题目描述
定义一个基类Person，它有3个protected的数据成员：姓名name(char *类型)、性别 sex(char类型)、年龄age(int类型)；一个构造函数用于对数据成员初始化；有一个成员函数show()用于输出数据成员的信息。
创建Person类的公有派生类Employee，增加两个数据成员 基本工资 basicSalary（int类型） 请假天数leaveDays（int型）；为它定义初始化成员信息的构造函数，和显示数据成员信息的成员函数show()。
输入
共5个数据，分别代表姓名、性别、年龄、基本工资、请假天数。
输出
如示例数据所示，共5行，分别代表姓名、年龄、性别、基本工资、请假天数
样例输入 Copy
zhangsan m 30 4000 2
样例输出 Copy
name:zhangsan
age:30
sex:m
basicSalary:4000
leavedays:2*/
#include<iostream>
#include<cmath>
#include<string>
using namespace std;
class Person
{
	protected:
		char* name;
		char sex;
		int age;
	public:
		Person(char *name_,char sex_,int age_):name(name_),sex(sex_),age(age_){}
		void show();
};
void Person::show()
{
	cout<<"name:"<<name<<endl;
	cout<<"age:"<<age<<endl;
	cout<<"sex:"<<sex<<endl;
}

class Employee:public Person
{
	public:
		int basicSalary;
		int leaveDays;
		Employee(char *name_,char sex_,int age_,int bs,int ld):Person(name_,sex_,age_),basicSalary(bs),leaveDays(ld){}
		void show();
};
void Employee::show()
{
	Person::show();
	cout<<"basicSalary:"<<basicSalary<<endl;
	cout<<"leavedays:"<<leaveDays<<endl;
}

int main()
{
	char name_[1000],sex_;
	int age_,bs_,ld_;
	cin>>name_>>sex_>>age_>>bs_>>ld_;
	Employee someone(name_,sex_,age_,bs_,ld_);
	someone.show();
}
