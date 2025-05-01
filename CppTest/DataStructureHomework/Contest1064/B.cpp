#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int T;
    cin>>T;
    while(T--){
        int temp;
        cin>>temp;
        for(int i=1;i<=temp;i++)
            for(int j=1;j<=temp;j++)
                cout<<i*j<<" \n"[j==temp?1:0];
    }

    return 0;
}