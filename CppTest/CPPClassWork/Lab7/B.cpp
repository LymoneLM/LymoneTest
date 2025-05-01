/*
问题 B: 狮子与老虎的朋友（友元函数）
[命题人 : liuhouquan]
时间限制 : 1.000 sec  内存限制 : 128 MB

题目描述
定义狮子 Lion 与老虎 Tiger 两个类，二者都有 weight 私有整型属性，定义二者的一个友元函数 totalWeight(参数表)，计算二者的重量和。设计程序，定义狮子与老虎两个对象之后，调用 totalWeight(参数表)，计算二者的重量和，然后输出。其中狮子与老虎的 Weight 是在各自的类成员函数中读数赋值。 
输入
两个整数。分别为狮子与老虎对象的重量
输出
输出一个整数，是两个对象重量之和。
样例输入 Copy
240 280
样例输出 Copy
520 */
#include <bits/stdc++.h>
using namespace std;
class Lion;
class Tiger{
	int weight;
	public:
		Tiger(int w):weight(w){};
		friend int totalWeight(Lion a,Tiger b);
};
class Lion{
	int weight;
	public:
		Lion(int w):weight(w){};
		friend int totalWeight(Lion a,Tiger b);	
};
int totalWeight(Lion a,Tiger b){
	return a.weight+b.weight;
}
int main()
{
	int w1,w2;cin>>w1>>w2;
	Lion l(w1);Tiger t(w2);
	cout<<totalWeight(l,t);
	return 0;	
}