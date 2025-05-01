#include <bits/stdc++.h>
using namespace std;
int main()
{
    int k;cin>>k;
    int data[13][2];
    for(int i=1;i<=12;i++)
    {
        data[i][0]=i-1;
        data[i][1]=i+1;
    }
    data[1][0]=12;
    data[12][1]=1;
    int p=1,m;
    for(int xi=1;xi<12;xi++)
    {
        for(int yi=1;yi<k;yi++)
        {
            p=data[p][1];
        }
        m=data[p][1];
        data[data[p][0]][1]=data[p][1];
        data[data[p][1]][0]=data[p][0];
        p=m;
    }
    cout<<m;
    return 0;
}