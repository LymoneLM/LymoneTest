#include <iostream>
using namespace std;
bool a(int n)
{
    if (n % 4 == 0 && n % 100 != 0 || n % 400 == 0)
        return true;
    else
        return false;
}
int y(int n)
{
    int r = 0, p = 0, i;
    for (i = 0; i < n; i++)
    {
        if (a(i))
            r++;
        else
            p++;
    }
    return (r * 366 + p * 365);
}
int m(int year, int month, int day)
{
    int num;
    if (a(year))
    {
        switch (month)
        {
        case 1:
            num = day;
            break;
        case 2:
            num = 31 + day;
            break;
        case 3:
            num = 31 + 29 + day;
            break;
        case 4:
            num = 31 + 29 + 31 + day;
            break;
        case 5:
            num = 31 + 29 + 31 + 30 + day;
            break;
        case 6:
            num = 31 + 29 + 31 + 30 + 31 + day;
            break;
        case 7:
            num = 31 + 29 + 31 + 30 + 31 + 30 + day;
            break;
        case 8:
            num = 31 + 29 + 31 + 30 + 31 + 30 + 31 + day;
            break;
        case 9:
            num = 31 + 29 + 31 + 30 + 31 + 30 + 31 + 31 + day;
            break;
        case 10:
            num = 31 + 29 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + day;
            break;
        case 11:
            num = 31 + 29 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + day;
            break;
        case 12:
            num = 31 + 29 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + day;
            break;
        }
    }
    else
    {
        switch (month)
        {
        case 1:
            num = day;
            break;
        case 2:
            num = 31 + day;
            break;
        case 3:
            num = 31 + 28 + day;
            break;
        case 4:
            num = 31 + 28 + 31 + day;
            break;
        case 5:
            num = 31 + 28 + 31 + 30 + day;
            break;
        case 6:
            num = 31 + 28 + 31 + 30 + 31 + day;
            break;
        case 7:
            num = 31 + 28 + 31 + 30 + 31 + 30 + day;
            break;
        case 8:
            num = 31 + 28 + 31 + 30 + 31 + 30 + 31 + day;
            break;
        case 9:
            num = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + day;
            break;
        case 10:
            num = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + day;
            break;
        case 11:
            num = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + day;
            break;
        case 12:
            num = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + day;
            break;
        }
    }
    return num;
}
int main()
{
    int year1, month1, day1,
        year2, month2, day2;
    cin >> year1 >> month1 >> day1 >> year2 >> month2 >> day2;
    cout << y(year2) + m(year2, month2, day2) -
                y(year1) - m(year1, month1, day1);
}
