#include <bits/stdc++.h>
using namespace std;
bool f(long n)
{
	do
	{
		if((n%10)%2!=0)
			return false;
	}
	while((n/=10)>0);
	return true;
}
int main()
{
	long n;
	cin>>n;
	if(f(n))
		cout<<"true";
	else
		cout<<"false";
	return 0;
}
