#include <bits/stdc++.h>
using namespace std;
long symm(long n)
{
	long n_=n;
	long dn=0;
	do
	{
		dn*=10;
		dn+=n%10;
	}
	while((n/=10)>0);
	return n_+dn;
}
int main()
{
	long n;
	cin>>n;
	cout<<symm(n);
	return 0;
}
