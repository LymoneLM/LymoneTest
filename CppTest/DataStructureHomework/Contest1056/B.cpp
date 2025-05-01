#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;
int vc[1010][1010];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N,M,temp,location;
    cin>>N;
    
    mm(vc);
    for(int i=0;i<N;i++){
        cin>>temp;
        vc[i][++vc[i][0]]=temp;
    }
    cin>>M;
    for(int i=0;i<M;i++){
        cin>>location>>temp;
        vc[location-1][++vc[location-1][0]]=temp;
    }
    for(int i=0;i<N;i++){
        for(int t=vc[i][0];t>=1;t--)
            cout<<vc[i][t]<<" ";
    }
        
    return 0;
}