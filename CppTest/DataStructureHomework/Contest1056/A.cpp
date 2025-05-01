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
    ll studentScore[1010][2];
    for(int i=0;i<N;i++)
        cin>>studentScore[i][0]>>studentScore[i][1];
    ll temp;
    cin>>temp;
    for(int i=0;i<N;i++)
        if(studentScore[i][0]==temp){
            cout<<studentScore[i][1];
            return 0;
        }

    return 0;
}