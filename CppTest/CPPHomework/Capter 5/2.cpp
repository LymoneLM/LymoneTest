#include <bits/stdc++.h>
using namespace std;
int main()
{
	int sum=0;
	int num[10]={};
	char c,str[2000];
	cin>>str;
	int i=0;
	while((c=str[i++])!='\0')
	{
		if(c>='0'&&c<='9')
		{
			sum++;
			num[c-'0']++;
		}
	}
	cout<<"Number's amount is:"<<sum<<endl;
	cout<<"'0...9' amount is:";
	for(int i=0;i<=8;i++)
		cout<<num[i]<<" ";
	cout<<num[9];
	return 0;
}
