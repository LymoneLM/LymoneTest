#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    string s;
    while(cin>>s){
    int len=s.size();
    cout<<len*(len+1)/2+1<<endl;
    }
    

    return 0;
}