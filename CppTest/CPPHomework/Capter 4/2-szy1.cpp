#include<iostream> 
using namespace std;
int f(int a)
{
	int i,sum=0,b;
	 b=a/2;
	for(i=1;i<b;i++)
	{
		if(a%i==0)
		sum+=i;
	}
	return sum; 
}
int main()
{
    int n,A,B; 
	cin>>n;
	for(A=2;A<=n;A++)
	{
		B=f(A);
		if(A==f(B)&&(A<B))
		   cout<<A<<" "<<B<<endl;
	    else
	       cout<<"No"<<endl;
	}
	return 0;
}
