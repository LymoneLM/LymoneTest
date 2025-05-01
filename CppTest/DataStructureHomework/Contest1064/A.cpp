#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;
char str[5000];
int len;
int find(int p) {
    int lp = p, rp = p + (str[p] == str[p + 1]);
    for (; lp >= 0 && rp < len; lp--, rp++)
        if (str[lp] != str[rp])
            break;
    lp++, rp--;
    return (rp - lp) ? (rp - lp + 1) / 2 : 1;
}
int find2(int p){
    
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (cin >> str) {
        len = strlen(str);
        int ans = 0;
        for (int i = 0; i < len; i++) {
            ans += find(i);
        }
        cout << ans << endl;
    }

    return 0;
}