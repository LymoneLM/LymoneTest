#include<iostream>
#include<string>
using namespace std;
int main()
{
	string name[5], Name;
	int number[4];
	int i = 0;
	int totalscoar = 0, TotalScore, AverageScore = 0, averagescore;
	while (i < 5)
	{
		cin >> name[i];
		int x = 0;
		//cout << "i=" << i<<' ';
		while (x < 4)
		{
			//cout << "x=" << x<<' ';
			cin >> number[x];
			totalscoar = totalscoar + number[x];
			x++;
		}
		averagescore = totalscoar / 4;
		if (averagescore > AverageScore)
		{
			AverageScore = averagescore;
			Name = name[i];
			TotalScore = totalscoar;
		}
		if (averagescore == AverageScore)
		{
			cout << Name << ' ' << TotalScore << ' ' << AverageScore << endl;
		}
		cout << name[i] << ' ' << totalscoar << ' ' << averagescore << endl;
		i++;
	}
	cout << "Student with the highest AverageScore is " << Name << ",AverageScore is " << AverageScore;

	getchar();
	getchar();
	return 0;
}

