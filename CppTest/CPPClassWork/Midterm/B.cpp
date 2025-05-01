
#include <bits/stdc++.h>
using namespace std;
int main()
{
    int n;cin>>n;
    int data[100];
    for(int i=0;i<n;i++)
        cin>>data[i];
     
    int max=0,temp;
    for(int xi=0;xi<n;xi++)
    {
        for(int yi=xi;yi<n;yi++)
        {
            temp=data[yi]-data[xi];
            max=(max>temp)?max:temp;
        }
    }
    cout<<max;
    return 0;
}
/**************************************************************
    Problem: 1112
    User: 04223498
    Language: C++
    Result: 正确
    Time:0 ms
    Memory:2088 kb
****************************************************************/
