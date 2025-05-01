#include <iostream>
#include<string.h>
#include<iomanip>
using namespace std;
void f(int a[][10],string A[][10])
{
	for(int j=0; j<5; j++)
	{
		cin>>A[j][0];

		for(int i=0; i<4; i++)
		{
			cin>>a[j][i];

		}

		a[j][4]=a[j][0]+a[j][1]+a[j][2]+a[j][3];
		a[j][5]=a[j][4]/4;
	}

}
int main()
{
	int a[10][10],b,c=0;
	string A[10][10],B;
	f(a,A);
	for(int j=0; j<5; j++)
	{
		if(a[j][25]>c)
		{
			c=a[j][5];
			b=j;
		}

	}
	B=A[b][0];
	cout<<"Name TotalScore AverageScore"<<endl;
	for(int j=0; j<5; j++)
	{


		cout<<setiosflags(ios::left)<<setw(10)<<A[j][0]<<setw(9)<<a[j][4]<<a[j][5]<<endl;
	}

	cout<<"Student with the highest AverageScore is "
	    <<B<<","<<"AverageScore is "<<c;
	return 0;
}
