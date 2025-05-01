#include<bits/stdc++.h>
using namespace std;
int count(char *str)
{
	int i=0;
	int n=0;
	while(str[i++]!='\0')
	{
		if((str[i-1]>='0'&&str[i-1]<='9')&&(str[i]<'0'||str[i]>'9'))
			n++;
	}
	return n;
}
void output(char *str)
{
	int i=0;
	int n=0;
	while(str[i++]!='\0')
	{
		if(str[i-1]>='0'&&str[i-1]<='9')
		{
			cout<<str[i-1];
			if(str[i]<'0'||str[i]>'9')
				cout<<endl;
		}
	}
}
int main()
{
	char str[100];
	cin.getline(str, 99);
	cout<<count(str)<<endl;
	output(str);
	return 0;
}