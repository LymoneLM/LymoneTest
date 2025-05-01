#include<iostream>
#include<cmath>
#include<string>
using namespace std;

class Complex { 
       double real; //复数实部 
       double imag; //复数虚部 
	public: 
       Complex (); //无参构造函数，将复数对象的实部和虚部均置为0 
       Complex (double r, double i):real(r),imag(i){}; //有参构造函数，设置对象的实部和虚部 
       Complex AddCom(Complex c2); //调用者对象与对象c2相加，返回Complex类对象 
       void OutCom () ; //输出调用者对象的有关数据（各分量） 
}; 
Complex Complex::AddCom(Complex c2)
{
	Complex c3(real+c2.real,imag+c2.imag);
	return c3;
}
void Complex::OutCom()
{
	if (imag==0&&real!=0) cout<<real<<endl;
	else if (real==0&&imag!=0) cout<<imag<<'i'<<endl;
	else if (real==0&&imag==0) cout<<0<<endl;
	else cout<<real<<'+'<<imag<<'i'<<endl;
}

int main()
{
	double a,b,c,d;
	cin>>a>>b>>c>>d;
	Complex c1(a,b),c2(c,d);
	c1=c1.AddCom(c2);
	c1.OutCom();
}
