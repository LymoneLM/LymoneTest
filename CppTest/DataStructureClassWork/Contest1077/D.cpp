#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int N, temp;
        cin >> N;
        set<int> st;
        for(int i=0;i<N;i++){
            cin>>temp;
            st.insert(temp);
        }
        st.erase(st.begin());
        if(st.empty())
            cout<<"NO"<<endl;
        else
            cout<<*st.begin()<<endl;     
    }

    return 0;
}