#include <bits/stdc++.h>
using namespace std;
long func(long n)
{
	return n==0?1:(func(n-1)+1)*2;
}
int main()
{
	long n;
	cin>>n;
	cout<<func(10-n);
	return 0;
}
