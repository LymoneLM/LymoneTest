/*
问题 C: 集合（运算符重载）
[命题人 : ]
时间限制 : 1.000 sec  内存限制 : 128 MB

题目描述
集合是由一个或多个确定的元素所构成的整体。集合的运算有并、交、相对补等。

集合A和集合B的交集：由属于A且属于B的相同元素组成的集合。

集合A和集合B的并集：由所有属于集合A或属于集合B的元素所组成的集合。

集合B关于集合A的相对补集，记做A-B：由属于A而不属于B的元素组成的集合。

假设集合A={10，20，30}，集合B={1，10，50，8}。则A与B的并是{10，20，30,1,50,8}，A与B的交是{10}，B关于A的相对补集是{20,30}。

定义整数集合类CSet，属性包括：集合中的元素个数n，整型指针data存储集合中的元素。
主函数输入集合A、B的数据，计算集合的并、交、相对补。
可根据题目，为CSet类添加需要的成员函数。


方法有：重载输出，按样例格式输出集合中的元素。
重载+运算符，求集合A和集合B的并集，并返回结果集合。 重载-运算符，求集合B关于集合A的相对补集，并返回结果集合。 重载*运算符，求集合A和集合B的交集，并返回结果集合。
输入
测试次数
每组测试数据两行，格式如下：
第一行：集合A的元素个数和元素
第二行：集合B的元素个数和元素
输出
每组测试数据输出如下：
第一行：集合A
第二行：集合B
第三行：A和B的并
第四行：A和B的交
第五行：B关于A的相对补集 与 A关于B的相对补集的并，即(A-B)+(B-A)
每组测试数据间以空行分隔。
样例输入 Copy
2
3 10 20 30
4 10 1 2 3
5 100 2 3 4 -10
6 -34 12 2 4 90 100
样例输出 Copy
A:10 20 30
B:10 1 2 3
A+B:10 20 30 1 2 3
A*B:10
(A-B)+(B-A):20 30 1 2 3

A:100 2 3 4 -10
B:-34 12 2 4 90 100
A+B:100 2 3 4 -10 -34 12 90
A*B:100 2 4
(A-B)+(B-A):3 -10 -34 12 90*/
#include<iostream>
#include<cmath>
#include<string>
using namespace std;
class CSet
{
	public:
		int *data;
		int n;
		CSet(int n_=0,int *a=0):n(n_){
			data = new int[n];
			data = a; 
		}
		CSet operator + (CSet );
		CSet operator - (CSet );
		CSet operator * (CSet );
};
CSet CSet::operator + (CSet c)
{
	int a[1000],t=0,j;
	for (int i=1;i<=n;i++) a[++t]=*(data+i);
	for (int i=1;i<=c.n;i++)
	{
		j=1;
		while (*(c.data+i)!=a[j]&&j<=t) j++;
		if (j>t) a[++t]=*(c.data+i);
	}
	CSet res(t,a);
	return res;
}
CSet CSet::operator * (CSet c)
{
	int a[1000],t=0,j;
	for (int i=1;i<=n;i++)
	{
		j=1;
		while (j<=c.n){
			if (*(data+i)==*(c.data+j)) a[++t]=*(data+i);
			j++;
		}
	}
	CSet res(t,a);
	return res;
}
CSet CSet::operator - (CSet c)
{
	int *a,t=0,j;
	a = new int[n+c.n];
	for (int i=1;i<=n;i++)
	{
		j=1;
		while (*(data+i)!=*(c.data+j)&&j<=c.n) j++;
		if (j>c.n) {*(a+(++t))=*(data+i);}
	}
	CSet res(t,a);
	return res;
}
void display(CSet c)
{
	for (int j=1;j<=c.n;j++) {
		if (j!=1) cout<<" ";
		cout<<*(c.data+j);
	}
	cout<<endl;
}
void getin(int *a,int m)
{
	for (int j=1;j<=m;j++){
		cin>>*(a+j);
		if (j!=1) cout<<" ";
		cout<<*(a+j);
	}
	cout<<endl;
}
int main()
{
	int n,a[1000],b[1000],m1,m2;
	cin>>n;
	for (int i=1;i<=n;i++)
	{
		cin>>m1;
		cout<<"A:";	getin(a,m1);
		cin>>m2;
		cout<<"B:";	getin(b,m2);
		CSet c1(m1,a),c2(m2,b),c3,c4,c;
		c=c1+c2;
		cout<<"A+B:"; display(c);
		c=c1*c2;
		cout<<"A*B:"; display(c);
		c3=c1-c2;c4=c2-c1;
		c=c3+c4;
		cout<<"(A-B)+(B-A):"; display(c);
		cout<<endl;
	}
}