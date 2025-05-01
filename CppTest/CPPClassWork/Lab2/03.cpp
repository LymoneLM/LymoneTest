#include <bits/stdc++.h>
using namespace std;
int main()
{
	int N;
	cin>>N;
	bool flag=false;
	for(int i=15; i<=N; i++)
	{
		if(i%3==1&&i%10==6)
		{
			if(flag)
				cout<<' ';
			cout<<i;
			flag=true;
		}

	}
	return 0;
}

