#include <bits/stdc++.h>
using namespace std;
int main()
{
	double a,b,c,d;
	cin>>a>>b>>c>>d;
	cout<<"A:"<<(a*=2.75)<<"\n";
	cout<<"B:"<<(b*=12.5)<<"\n";
	cout<<"C:"<<(c*=26.8)<<"\n";
	if(d<=3)
		d*=512;
	else if(d<=8)
		d=512.0*d*0.9;
	else
		d=512.0*d*0.85;
	cout<<"D:"<<d<<"\n";
	cout<<"total:"<<a+b+c+d;
	return 0;
}
