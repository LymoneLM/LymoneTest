#include<iostream>
using namespace std;
void reverse(int a[],int size);
int main()
{
	int size;
	int i;
	cin>>size;
	int a[100001]= {};
	for(int i=0; i<=(size-1); i++)
	{
		cin>>a[i];
	}

	reverse(a,size);
	return 0;
}
void reverse(int a[],int size)
{
	int i,j;
	if(size%2==0)
	{
		while(i<=size/2)
		{
			a[i]=j;
			j=a[size-1-i];
			a[size-1]=j;
			i++;
		}
	}
	else
	{
		while(i<=(size-1)/2)
		{
			a[i]=j;
			j=a[size-1-i];
			a[size-1-i]=j;
			i++;
		}

	}
	for(i=0; i<=(size-1); i++)
	{
		cout<<a[i]<<" ";
	}
}
