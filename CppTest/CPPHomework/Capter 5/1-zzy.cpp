#include<iostream>
#include<string>
#include<iomanip>
using namespace std;
int main()
{
	string Name[5];
	string find_Name;
	int stud[5][4],TotalScore[5]= {0},AverageScore[5];
	int i,j;
	for(i=0; i<5; i++)
	{
		cin>>Name[i];
		for(j=0; j<4; j++)
		{
			cin>>stud[i][j];
			TotalScore[i]+=stud[i][j];
			AverageScore[i]=TotalScore[i]/4;
		}
	}
	cout<<"Name TotalScore AverageScore"<<endl;
	for(i=0; i<5; i++)
		cout<<setiosflags(ios::left)<<setw(10)<<Name[i]<<setw(9)<<TotalScore[i]<<AverageScore[i]<<endl;
	int max[1]= {0};
	string name[1];
	for(i=0; i<5; i++)
	{
		if(AverageScore[i]>max[0])
		{
			max[0]=AverageScore[i];
			name[0]=Name[i];
		}
	}
	cout<<"Student with the highest AverageScore is"<<" "<<name[0]<<"AverageScore is"<<" "<<max[0]<<endl;
	return 0;

}

