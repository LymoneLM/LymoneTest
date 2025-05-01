#include <bits/stdc++.h>
using namespace std;
class Person
{
    char* name;
    int age;
    char sex;
    public:
    Person(char* n,char s,int a):name(n),age(a),sex(s){}
    void show()
    {
        cout<<"name:"<<this->name<<endl;
        cout<<"age:"<<this->age<<endl;
        cout<<"sex:"<<this->sex<<endl;
    }
};
class Employee:public Person
{
    int basicSalary;
    int leaveDays;
    public:
    Employee(char* n,char s,int a,int b,int l):Person(n,s,a),basicSalary(b),leaveDays(l){}
    void show()
    {
        Person::show();
        cout<<"basicSalary:"<<this->basicSalary<<endl;
        cout<<"leavedays:"<<this->leaveDays<<endl;
    }
};
int main()
{
    char name[20],sex;
    int age,ba,le;
    cin>>name>>sex>>age>>ba>>le;
    Employee data(name,sex,age,ba,le);
    data.show();
    return 0;
}