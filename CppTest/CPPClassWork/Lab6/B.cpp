#include<iostream>
#include<cmath>
#include<string>
using namespace std;
int month[13]={0,31,28,31,30,31,30,31,31,30,31,30,31};

int checkRun(int y)
{
	if (y%400==0||(y%100!=0&&y%4==0)) return 1;
	return 0;
}

class DateType { 
 //自定义的日期类 DateType
    	int y,m,d; //数据成员，表示当前日期的年、月、日
	public:
    	DateType(int y0=1,int m0=1,int d0=1):y(y0),m(m0),d(d0){};
        //构造函数，设定年、月、日；并设置参数默认值
    	void IncrementDay(); //增加 1 天
    	bool Equal(DateType dt2); //判断二日期是否相等
    	void PrintDate(); //屏幕输出日期对象的有关数据（年、月、日）
}; 
void DateType::IncrementDay()
{
	d++;month[2]+=checkRun(y);
	if (d>month[m]){
		d=1;m++;
		if (m>12) {m=1;y++;}
	}
	month[2]-=checkRun(y);
}
bool DateType::Equal(DateType dt2)
{
	if (y==dt2.y&&m==dt2.m&&d==dt2.d) return true;
	return false;
}
void DateType::PrintDate()
{
	cout<<y<<':'<<m<<':'<<d<<endl;
}

int main()
{
	int y1,y2,m1,m2,d1,d2;
	cin>>y1>>m1>>d1>>y2>>m2>>d2;
	DateType dt1(y1,m1,d1),dt2(y2,m2,d2);
	dt1.PrintDate();
	dt2.PrintDate();	
	dt1.IncrementDay();
	dt2.IncrementDay();
	cout<<(dt1.Equal(dt2)?"True":"False")<<endl;
	dt1.PrintDate();
	dt2.PrintDate();	
}
