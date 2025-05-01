using namespace std;
#include <iostream>
int c[100];
class cset
{
	int n;
	int* data;
public:
	cset(int n1, int* d1) :n(n1), data(d1) {}
	cset operator+(cset& c1);
	void show()
	{
		for (int i = 0; i <= n; i++)
			cout << *(data + i) << " ";
	}
};
cset cset:: operator+(cset& c1)
{
	int nn2;
	int num = 0;
	for (int i = 0; i < n; i++)//i 前
	{
		c[i] = *(data + i);//把a中所有复制到c,0~n-1的数 共n个，结尾c[n-1]
	}
	cout << endl;
	nn2 = n-1;
	for (int j = 0; j < c1.n; j++)//j 后
	{
		for (int i = 0; i < n; i++)
		{
			if (*(c1.data + j) == *(data + i))
			{
				break;
			}
			if ((*(c1.data + j) != *(data + i)) && (i == (n - 1)))//当a中数被扫描完并此数为a数个数时
			{
				//集合b中有几个与a不匹配的数
				c[++nn2] = *(c1.data + j);//原先a有的加上b有a没有的，这里不是++i
			}
		}
	}int* p = c;
	cset c3(nn2 , p);
	for (int i = 0; i <= nn2; i++)//<=
		cout << *(c3.data + i) << " ";//这里输出正常
	cout << endl;
	//return c3;
    return cset(nn2,p);
}
int main()
{
	int n, n1, a[100], b[100], * nn, * nn1;
	cin >> n;
	for (int i = 0; i < n; i++)
		cin >> a[i];
	cin >> n1;
	for (int i = 0; i < n1; i++)
		cin >> b[i];
	nn = a;
	nn1 = b;
	cset c0(n, a);
	cset c1(n1, b);
    cset cm = c0 + c1;
	cm.show();
}
