#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    bool child[110];
    mm(child);
    int n,m;
    cin>>n>>m;
    int cnt=0,bnt=0;
    while(cnt!=n)
        for(int i=0;i<n;i++){
            if(!child[i]) bnt++;
            if(bnt==m){
                cout<<i+1<<" ";
                child[i]=true;
                cnt++,bnt=0;
            }
        }

    return 0;
}