#include<iostream>
using namespace std;
int main() 
{
	int A[8][3] = { 0 },sum=0; //数组A为每户人家要乘坐电梯的次数
	                            // 例A[2][1]为2楼1室要乘坐电梯的次数，
                                //规定A[0][0]为要补偿的费用,A[0][1]为题目中的W
	for (int i = 0;i < 8;i++)  //sum为所有户人家要乘坐电梯次数的总和
	{
		for (int j = 1;j < 3;j++)
		{
			cin >>A[i][j];
			sum += (i-1)*A[i][j];
		}
	}
	int b;
	double p;
	for (int i = 1;i < 8;i++)
	{
		for (int j = 1;j < 3;j++)
		{
			b = (i - 1) * A[i][j];
			p = (double)(A[0][1] + A[0][0]) * b / sum;
			cout << "第" << i << "层" << "第" << j << "户要承担的费用为： " << p << endl;
		}
	}
	return 0;
}