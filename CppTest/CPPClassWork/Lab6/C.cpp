#include<iostream>
#include<cmath>
#include<cstring> 
using namespace std;
class CStudent { //学生类 CStudent
        unsigned long reg_num; //数据成员：注册号
    	char name[30]; //数据成员：姓名
    	float math, eng, comp; //数据成员：数学、英语、计算机成绩
	public: //公有成员函数
    	float Sum(); //求三门课总成绩的函数 Sum
        float Average(); //求三门课平均成绩的函数 Average
        void Display(); //显示学生数据信息的函数 Display
        void SetData (unsigned long r,char* n,float m,float e,float c);
        //设置学生数据信息的函数 SetData
 };
 void CStudent::SetData(unsigned long r,char* n,float m,float e,float c)
{
	reg_num=r;
	strcpy(name,n);
	math=m;
	eng=e;
	comp=c;
}
float CStudent::Sum()
{
	return math+eng+comp;
} 
float CStudent::Average()
{
	return (math+eng+comp)/3.0;
}
void CStudent::Display()
{
	cout<<reg_num<<" "<<name<<" "<<math<<" "<<eng<<" "<<comp<<endl;
}


int main()
{
	char c,name_[30];
	unsigned long reg_num_;
    float math_,eng_,comp_,sum_max,sum_n;
	string s; 
	int n,x,res,res_num;
	CStudent stu[160];
	cin>>n;
	cout<<"TOTAL="<<n<<endl;
	for (int i=1;i<=n;i++)
	{
		cin>>res_num>>name_>>math_>>eng_>>comp_;
		stu[i].SetData(res_num,name_,math_,eng_,comp_);
		cout<<"CStudent "<<i<<" : ";
		stu[i].Display();
	}
	for (int i=1;i<=n;i++)
	{
		sum_n=stu[i].Sum();
		if (sum_n>sum_max) {
			sum_max=sum_n;
			res=i;
		}
		cout<<"CStudent"<<i<<".Sum="<<sum_n<<",CStudent"<<i<<".average="<<stu[i].Average()<<endl;
	}
	cout<<"class_Sum_max="<<sum_max<<endl<<"The infomation of the CStudent with class_Sum_max : ";
	stu[res].Display(); 
}
