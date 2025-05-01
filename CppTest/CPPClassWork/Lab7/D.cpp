/*问题 D: 矩形类（继承与派生）
[命题人 : liuhouquan]
时间限制 : 1.000 sec  内存限制 : 128 MB

题目描述
要求定义一个基类Point，它有两个私有的float型数据成员X,Y;一个构造函数用于对数据成员初始化；有一个成员函数void Move(float xOff, float yOff)实现分别对X,Y值的改变，其中参数xOff和yOff分别代表偏移量。另外两个成员函数GetX() 、GetY()分别返回X和Y的值。
Rectangle类是基类Point的公有派生类。它增加了两个float型的私有数据成员W,H; 增加了两个成员函数float GetH() 、float GetW()分别返回W和H的值；并定义了自己的构造函数，实现对各个数据成员的初始化。
编写主函数main()根据以下的输入输出提示，完成整个程序。
输入
6个float型的数据，分别代表矩形的横坐标X、纵坐标Y、宽度W，高度H、横向偏移量的值、纵向偏移量的值；每个数据之间用一个空格间隔
输出
输出数据共有4个，每个数据之间用一个空格间隔。分别代表偏移以后的矩形的横坐标X、纵坐标Y、宽度W，高度H的值
样例输入 Copy
5 6 2 3 1 2
样例输出 Copy
6 8 2 3*/
#include<iostream>
#include<cmath>
#include<string>
using namespace std;
class Point
{
	private:
		float X;
		float Y;
	public:
		Point(float x,float y):X(x),Y(y){}
		void Move(float xOff, float yOff)
		{
			X+=xOff;
			Y+=yOff;
		}
		float GetX(){return X;}
		float GetY(){return Y;}
};

class Rectangle:public Point
{
	private:
		float W;
		float H;
	public:
		Rectangle(float x,float y,float w,float h):Point(x,y),W(w),H(h){}
		float GetW(){return W;}
		float GetH(){return H;}
};

int main()
{
	float a,b,c,d,e,f;
	cin>>a>>b>>c>>d>>e>>f;
	Rectangle r(a,b,c,d);
	r.Move(e,f);
	cout<<r.GetX()<<" "<<r.GetY()<<" "<<r.GetW()<<" "<<r.GetH()<<endl;
}