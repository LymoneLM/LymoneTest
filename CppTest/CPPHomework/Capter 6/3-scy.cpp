#include<iostream>
using namespace std;
bool f(char b)
{
	if(b>='0'&&b<='9') return true;
	else return false;
}
int main()
{
	char a[50];
	int c=0;
	cin.getline(a,49);
	for(int i=0;a[i]!='\0';i++)
	{
		if(f(a[i])&&(!f(a[i+1]))) c++;   //利用一段数字的最后一个判断整数个数； 
	}
	cout<<c<<endl;
	if(a[0]==0)               //当开头是0时舍去； 
	{
		for(int i=1;a[i]!='\0';i++)
		{
			if(f(a[i])) cout<<a[i];     //输出每个整数；
		    if(f(a[i])&&(!f(a[i+1]))) cout<<endl;     
    	}
	}
	else
	{
		for(int i=0;a[i]!='\0';i++)
		{
			if(f(a[i])) cout<<a[i];
			if(f(a[i])&&!f(a[i+1])) cout<<endl;
		}
	}
	return 0;
}
