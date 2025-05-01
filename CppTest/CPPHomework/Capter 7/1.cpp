#include <bits/stdc++.h>
using namespace std;
const int m_day[]={0,31,28,31,30,31,30,31,31,30,31,30,31};
struct Date
{
    int year,month,day;
};
int is_r(int n)
{
    return (0 == n % 4 && n % 100 != 0) || (0 == n % 400)?1:0;
}
int days(Date &date)
{
    int day_c=0;
    for(int i=1;i<date.month;i++)
    {
        day_c+=m_day[i];
        if(i==2)
            day_c+=is_r(date.year);
    }
    return day_c+date.day;
}
int main()
{
    Date date;
    cin>>date.year>>date.month>>date.day;
    cout<<days(date);
    return 0;     
}