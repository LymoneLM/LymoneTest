#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    char x[200];
    cin>>x;
    cout<<x;
    int a,b,i=0;
    while(x[i]!='+')i++;
    x[strlen(x)-1]=x[i]=' ';
    sscanf(x,"%d%d",&a,&b);
    cout<<a+b;

    return 0;
}