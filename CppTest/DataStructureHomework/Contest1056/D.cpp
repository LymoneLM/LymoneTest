#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int max,temp,cnt=1;
    cin>>max;
    while(cin>>temp)
        if(temp<max)
            continue;
        else if(++cnt&&temp>max)
            max=temp,cnt=1;
    cout<<cnt;

    return 0;
}