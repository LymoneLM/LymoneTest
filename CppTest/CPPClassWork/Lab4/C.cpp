#include <bits/stdc++.h>
using namespace std;
bool is_r(int n)
{
    return (0 == n % 4 && n % 100 != 0) || (0 == n % 400)?1:0;
}
class date
{
	const int m_day[13]={0,31,28,31,30,31,30,31,31,30,31,30,31}; 
    public:
    int year,month,day;
    void input()
    {
        cin>>year>>month>>day;
    }
    bool equal(const date &temp)
    {
        bool flag=true;
        if(year!=temp.year)
            flag=false;
        if(month!=temp.month)
            flag=false;
        if(day!=temp.day)
            flag=false;
        return flag;
    }
    void add()
    {
        day++;
        if(month==2&&is_r(year))
        {
            if(day>m_day[2]+1)
            {
                month=3;
                day=1;
            }
        }
        else
        {
            if (day>m_day[month])
            {
                month++;
                day=1;
            }
            if (month>12)
            {
                year++;
                month=1;
            }
        }
    }
};
int main()
{
    date fir,sec;
    fir.input();
    sec.input();
    int n=0;
    while(true)
    {
        if(fir.equal(sec))
            break;
        fir.add();
        ++n;
    }
    cout<<n;
    return 0;
}