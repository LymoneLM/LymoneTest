#include <bits/stdc++.h>
using namespace std;
map<int,bool>mp;
int enSum(int n)
{
	int sum=0;
	int max=sqrt(n);
	for(int i=1;i<n;i++)
	{
		if(n%i==0)
		{
			sum+=i;
		}
	}
	return sum;
}

int main()
{
	int n;
	cin>>n;
	if(n<284)
	{
		cout<<"No";
		return 0;
	}
	cout<<"220 284"<<endl;
	for(int i=400;i<=n;i++)
	{
		if(enSum(i)<=n&&enSum(i)!=i&&enSum(enSum(i))==i)
		{
			if(mp.count(min(enSum(i),i))==0)
			{
				cout<<min(enSum(i),i)<<" "
				<<max(enSum(i),i)<<endl;
				mp[min(enSum(i),i)]=true;
			}
		}
	}
	return 0;
} 
