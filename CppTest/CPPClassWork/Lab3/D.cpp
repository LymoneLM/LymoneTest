#include <bits/stdc++.h>
using namespace std;
bool symm(long n)
{
	long n_=n;
	long dn=0;
	do
	{
		dn*=10;
		dn+=n%10;
	}
	while((n/=10)>0);
	if(dn==n_)
		return true;
	return false;
}
int main()
{
	long n;
	cin>>n;
	for(int m=1; m<=n; m++)
	{
		if(symm(m)&&symm(7*m)&&symm(3*m*m))
		{
			cout<<m<<" ";
		}
	}
	return 0;
}
