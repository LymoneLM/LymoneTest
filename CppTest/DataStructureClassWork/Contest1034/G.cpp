#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin>>N;
    int a[20000],b[200000];
    for(register int i=0;i<N;i++) cin>>a[i];
    for(register int i=0;i<N;i++) cin>>b[i];
    int pa=0,pb=0;
    while(pa<N&&pb<N){
        if(a[pa]<b[pb])
            cout<<a[pa++]<<" ";
        else
            cout<<b[pb++]<<" ";
    }
    if(pa+pb!=2*N){
        if(pa==N){
            for(int i=pb;i<N;i++)
                cout<<b[i]<<" ";
        } else {
            for(int i=pa;i<N;i++)
                cout<<a[i]<<" ";
        }
    }

    return 0;
}