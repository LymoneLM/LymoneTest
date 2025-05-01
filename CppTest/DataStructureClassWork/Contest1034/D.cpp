#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;
const char num[37] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
stack<int> st;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, r;
    cin >> n >> r;
    while (n > 0) {
        st.push(n % r);
        n /= r;
    }
    while (st.size() != 0) {
        cout << num[st.top()];
        st.pop();
    }
    
    return 0;
}