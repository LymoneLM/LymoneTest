#include <bits/stdc++.h>
using namespace std;
int enSum(int n)
{
	int sum=0,max=sqrt(n);
	for(int i=1;i<n;i++)
	    if(n%i==0)
            sum+=i;
	return sum;
}
int main()
{
	int n;cin>>n;
    bool flag=true;
	for(int a=1;a<=n;a++)
	{
        int b=enSum(a);
		if(b<=n&&a<b&&enSum(b)==a)
		{
				cout<<a<<" "<<b<<endl;
                flag=false;
		}
	}
    if(flag)
        cout<<"No";
	return 0;
} 
