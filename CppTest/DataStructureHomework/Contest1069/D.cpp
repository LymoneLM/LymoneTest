#include <bits/stdc++.h>
using namespace std;
int main() {  
    
    int N,x,dat[100];
    cin>>N;x=N;
    while(x--) cin>>dat[x];
    sort(dat,dat+N,greater<int>());
    while(N--) cout<<dat[N]<<" \n"[N==0?1:0];

    return 0;
}