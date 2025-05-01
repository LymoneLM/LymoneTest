#include <bits/stdc++.h>
using namespace std;
int f(unsigned long x, int n,int & Lxn)
{
    char str[10001];
    sprintf(str,"%ld",x);
    Lxn=str[n-1]-'0';
    int len=strlen(str);
    if(len<n)
    {
        Lxn=0;
        return 0;
    }
    return x/((int)pow(10,n-1)) % 10;
}
int main()
{
    unsigned long x;
    int n;
    int Lxn;
    cin>>x>>n;
    cout<<f(x,n,Lxn)<<" "<<Lxn;
    return 0;
}