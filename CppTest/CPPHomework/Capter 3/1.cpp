#include <bits/stdc++.h>
using namespace std;
int main()
{
	char num[101];
	cin>>num;
	int len=strlen(num);
	int sum=0;
	for (int i=len-1;i>=0;i--)
	{
		cout<<num[i];
		sum+=num[i]-'0';
	}
	cout<<endl<<sum<<endl<<len;
	return 0;
}
