#include <bits/stdc++.h>
using namespace std;
int main()
{
    char data[120];
    cin>>data;
    int len=strlen(data);
    if(data[0]=='-')
    {
    int st=len%3;
    cout<<"-";
    for(int i=1;i<len;i++)
        cout<<data[i]<<(((i+1)%3==st)&&(i!=len-1)?",":"");
    }
    else
    {
    int st=(len-1)%3;   
    for(int i=0;i<len;i++)
        cout<<data[i]<<(((i)%3==st)&&(i!=len-1)?",":"");
    }
    return 0;
}
/**************************************************************
    Problem: 1106
    User: 04223498
    Language: C++
    Result: 正确
    Time:0 ms
    Memory:2088 kb
****************************************************************/
