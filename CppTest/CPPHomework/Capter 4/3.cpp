#include <bits/stdc++.h>
using namespace std;
int digit(long n,int k)
{
	return (n/=(pow(10,(k-1))))?n%10:-1;
}
int main()
{
	long n;int k;
	cin>>n>>k;
	cout<<digit(n,k);
	return 0;
}
