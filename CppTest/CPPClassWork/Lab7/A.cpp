/*
问题 A: 零件类(静态成员)
[命题人 : ]
时间限制 : 1.000 sec  内存限制 : 128 MB

题目描述
定义一个 Lingjian 类，拥有整型的数据成员 Weight 和静态数据成员 AllWeights（初始化为 0），每定义一个对象时， 在AllWeights 中增加该零件的重量 Weight；在析构函数中减去 Weight；静态成员函数 GetAllWeights（）获取AllWeights。设计程序，定义两个对象之后， 输出类的 AllWeights。其中 Weight 是通过成员函数输入对单个零件重量赋值。
输入
两个整数。 分别为两个对象的重量
输出
输出一行，是AllWeights的值
样例输入 Copy
12 24 
样例输出 Copy
36 */
#include <bits/stdc++.h>
using namespace std;
class Lingjian
{
	int Weight;
	static int Allweights;
	public:
	Lingjian(int w):Weight(w)
	{
		Allweights+=w;
	}
	~Lingjian()
	{
		Allweights-=Weight;
	}
	static int GetAllWeights()
	{
		return Allweights;
	}
};
int Lingjian::Allweights=0;
int main()
{
	int a,b;cin>>a>>b;
	Lingjian l1(a),l2(b);
	cout<<Lingjian::GetAllWeights();
	return 0;
}