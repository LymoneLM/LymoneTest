#include <bits/stdc++.h>
using namespace std;
int main()
{
    int t,m;
    cin>>t;
    double temp;
    for(int i=0;i<t;i++)
    {
        cin>>temp>>m;
        cout<<int(temp*pow(10,m))%10<<endl;
    }
    return 0;
}
/**************************************************************
    Problem: 1141
    User: 04223498
    Language: C++
    Result: 正确
    Time:0 ms
    Memory:2340 kb
****************************************************************/
