#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int temp,i=0,data[200];
    while(cin>>temp)
        data[i++]=temp;
    sort(data,data+i,greater<int>());
    while(i--)
        cout<<data[i]<<" ";

    return 0;
}