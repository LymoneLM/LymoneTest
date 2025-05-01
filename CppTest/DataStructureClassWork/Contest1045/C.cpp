#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T,temp,ans=0;
    cin>>T;
    for(int i=0;i<T;i++)
        for(int j=0;j<T;j++){
            cin>>temp;
            if(i==j)
                ans+=temp;
        }
    cout<<ans;
    return 0;
}