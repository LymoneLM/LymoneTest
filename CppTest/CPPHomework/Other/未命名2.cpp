#include <iostream>
using namespace std;
int main()
{
	int a,n;cin>>a>>n;
	int sum=0;int temp=0;
	for(int i=1;i<=n;i++)
	{
		temp*=10,temp+=a;
		sum+=temp;
	}
	cout<<"sum="<<sum<<endl;
	return 0; 
 } 
