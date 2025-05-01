#include <bits/stdc++.h>
using namespace std;
long long func(long long n)
{
	int i=1;
	do
	{
		if(i*i>=n)
			break;
	}
	while(i++);
	return i*i;
}
int main()
{
	long long n;
	cin>>n;
	cout<<func(n);
	return 0;
}
