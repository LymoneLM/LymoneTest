#include <bits/stdc++.h>
using namespace std;
int main()
{
    int n,m,n_m;cin>>n>>m;n_m=n-m;
    long long ln=1,ln_m=1;
    for(int i=1;i<=n;i++)
        ln*=i;
    for(int i=1;i<=n_m;i++)
        ln_m*=i;
    cout<<ln/ln_m;
    return 0;
}
/**************************************************************
    Problem: 1138
    User: 04223498
    Language: C++
    Result: 正确
    Time:0 ms
    Memory:2088 kb
****************************************************************/
