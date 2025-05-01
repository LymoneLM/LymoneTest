/*
Warning!
There is the shit HELL.
*/
#include <bits/stdc++.h>
using namespace std;

class Date
{
    const int m_day[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int year, month, day;

public:
    Date() {}
    void setDate()
    {
        cin >> year >> month >> day;
    }
    bool isLeapYear(int n)
    {
        return (0 == n % 4 && n % 100 != 0) || (0 == n % 400) ? 1 : 0;
    }
    void outputLeapYear()
    {
        cout << year << " is"
             << (isLeapYear(year) ? " " : " not ")
             << "leap year." << endl;
    }
    bool equal(const Date &temp)
    {
        bool flag = true;
        if (year != temp.year)
            flag = false;
        if (month != temp.month)
            flag = false;
        if (day != temp.day)
            flag = false;
        return flag;
    }
    void add()
    {
        day++;
        if (month == 2 && isLeapYear(year))
        {
            if (day > m_day[2] + 1)
            {
                month = 3;
                day = 1;
            }
        }
        else
        {
            if (day > m_day[month])
            {
                month++;
                day = 1;
            }
            if (month > 12)
            {
                year++;
                month = 1;
            }
        }
    }
    int EXgetSkip(Date o)
    {
        int n = 0;
        while (true)
        {
            if (equal(o))
                break;
            add();
            ++n;
        }
        return n;
    }
    int SZYgetSkip(Date o)
    {
        int m_day[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        int y1, m1, d1;
        y1 = this->year, m1 = this->month, d1 = this->day;
        int y2, m2, d2;
        y2 = o.year, m2 = o.month, d2 = o.day;
        int sumy = 0;
        for (int i = y1; i < y2; i++)
            if (isLeapYear(i))
                sumy += 366;
            else
                sumy += 365;
        int summ1 = 0;
        if (isLeapYear(y1))
        {
            m_day[1] = 29;
            for (int i = 0; i < m1 - 1; i++)
            {
                summ1 += m_day[i];
            }
            m_day[1] = 28;
        }
        else
        {
            for (int i = 0; i < m1 - 1; i++)
            {
                summ1 += m_day[i];
            }
        }
        int sum1;
        sum1 = summ1 + d1;
        int summ2 = 0;
        if (isLeapYear(y2))
        {
            m_day[1] = 29;
            for (int i = 0; i < m2 - 1; i++)
            {
                summ2 += m_day[i];
            }
            m_day[1] = 28;
        }
        else
        {
            for (int i = 0; i < m2 - 1; i++)
            {
                summ2 += m_day[i];
            }
        }
        int sum2;
        sum2 = summ2 + d2;
        int m;
        m = sumy + sum2 - sum1;
        return m;
    }
    int zeroCount()
    {
        int sum=0;
        for(int i=1;i<year;i++)
        {
            sum+=365;
            if(isLeapYear(i))
               sum++;
        }
        for(int i=1;i<month;i++)
        {
            sum+=m_day[i];
            if(i==2&&isLeapYear(year))
                sum++;
        }
        sum+=day;
        return sum;
    }
    int getSkip(Date o)
    {
        return abs(o.zeroCount()-zeroCount());
    }
};
int main()
{
    Date fir, sec;
    fir.setDate();
    sec.setDate();
    fir.outputLeapYear();
    sec.outputLeapYear();
    cout << "The skip of two date is "
         << fir.getSkip(sec) << ".";
    return 0;
}