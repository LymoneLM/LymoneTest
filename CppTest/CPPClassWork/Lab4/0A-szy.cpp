#include<iostream> 
using namespace std;
int main()
{
	int a[50];
	int b[50]={0};
	int k,n;
	cin>>k;
	for(int i=0;i<k;i++)
	{
		cin>>a[i];
	}
	int sum=0;
	for(int i=0;i<k;i++)
	{
		sum+=a[i];
	}
	double ave=0;
	n=0;
	ave=(double)sum/k;
	for(int i=0;i<k;i++)
	{
		if(a[i]>ave)
		{
			n++;
		}
	}
	cout<<ave<<" "<<n<<endl;
	int m=0;
	for(int i=0;i<k;i++)
	{
	    bool flag=true;
		for(int j=0;j<m;j++)
		{
			if(a[i]==b[j])
			{
				flag=false;
				break;
			}
		}
		if(flag)
		{
			b[m]=a[i];
			m++;
		}
	}
    for(int j=0;j<m;j++)	cout<<b[j]<<" ";
}

