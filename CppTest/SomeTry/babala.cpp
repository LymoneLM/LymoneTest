#include <bits/stdc++.h>
using namespace std;
int main() {
    int T;cin>>T;
    for(int x=1;x<=T;x++){
        cout<<"Case #"<<x<<": ";
        string I,P;
        cin>>I>>P;
        int p=0;
        for(auto i:P){
            if(i==P[p])
                p++;
            if(p==P.size())
                break;
        }
        if(p==P.size())
            cout<<P.size()-I.size();
        else
            cout<<"IMPOSSIBLE";
        cout<<endl;
    }
    return 0;
}