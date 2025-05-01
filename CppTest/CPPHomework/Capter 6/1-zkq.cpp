#include<iostream>
#include<string>
using namespace std;
int main()
{
	int a[5] = { 0 };//存储每个字符串的长度的数组
	string str[5];//即将输入的字符串
	for (int i = 0; i < 5; i++)
	{
		cin >> str[i];
	}
	for (int i = 0; i < 5; i++)
	{
		a[i] = str[i].length();//计算并存储长度
	}
	int temp1 = 0;//作为媒介辅助数据交换
	string temp2;//同上
	for (int i = 0; i < 5; i++)//冒泡排序
		for (int j = 0; j < 5 - i; j++)
		{
			if (a[j] > a[j + 1])
			{
				temp1=a[j];
				a[j] = a[j + 1];
				a[j + 1] = temp1;
				temp2 = str[j];
				str[j] = str[j + 1];
				str[j + 1] = temp2;
			}
		}
	for (int i = 0; i < 5; i++)//输出排序后的字符串
		cout << str[i] << ' ';
	cout << endl;
	cout << "concatenate string:";
	for (int i = 0; i < 5; i++)
	{
		if (a[i] >= 3)
			cout << str[i][2];
		else
			cout << ' ';
	}
	getchar();
	getchar();
	return 0;
}
