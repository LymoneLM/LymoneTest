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
    cin.get();
    char ch[1010];
    stack<char> st;
    while(T--){
        cin.getline(ch,1010);
        int len=strlen(ch);
        for(int i=0;i<=len;i++){
            if(ch[i]==' '||ch[i]=='\0'){
                while (st.size()){
                    cout<<st.top();
                    st.pop();
                }
                cout<<' ';
            } else st.push(ch[i]);
        }
        cout<<endl;
    }

    return 0;
}