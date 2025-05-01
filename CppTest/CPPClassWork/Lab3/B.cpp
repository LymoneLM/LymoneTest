#include <bits/stdc++.h>
using namespace std;
void find(int i,int n)
{
	int t=0;
	while(t<n)
	{
		int m=sqrt(i);
		bool flag=true;
		for(int x=2;x<=m;x++)
		{
			if(i%x==0)
				flag=false;
		}
		if(flag)
		{
			cout<<i<<" ";
			t++;
		}
		i++;
	}
	return;
}
int main()
{
	int i,n;
	cin>>i>>n;
	find(i,n);
	return 0;
}
