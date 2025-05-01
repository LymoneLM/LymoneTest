/*
zhangsan 87 76 91 79
lisi 90 89 78 69
wangwu 80 88 91 85
zhaoqian 77 79 78 75
sunli 89 87 88 87
*/
#include <bits/stdc++.h>
using namespace std;
class Student
{
	public:
		char name[20];
		int TotalScore,AverageScore;
	Student()
	{
		TotalScore=0;
		AverageScore=0;
	}
};
int main()
{
	Student data[5];
	int temp;
	for(int i=0;i<5;i++)
	{
		cin>>data[i].name;
		
		for(int t=0;t<4;t++)
		{
			cin>>temp;
			data[i].TotalScore+=temp;
		}
		data[i].AverageScore=data[i].TotalScore/4;
	}
	int maxi=0,maxn=data[0].AverageScore;
	for(int i=1;i<5;i++)
	{
		if(data[i].AverageScore>maxn)
		{
			maxi=i;
			maxn=data[i].AverageScore;
		}
	}
	cout<<"Name TotalScore AverageScore"<<endl;
	for(int i=0;i<5;i++)
	{
		cout<<setiosflags(ios::left)<<setw(10)
		<<data[i].name<<setw(9)<<data[i].TotalScore
		<<data[i].AverageScore<<endl;
	}
	cout<<"Student with the highest AverageScore is ";
	cout<<data[maxi].name<<",AverageScore is "<<data[maxi].AverageScore;
	return 0;
} 
