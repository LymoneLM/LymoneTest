#include <cstdio>
#include <cstring>
#include <iostream>
using namespace std;
 
const int maxn = 40;
int pos1[maxn], pos2[maxn];
int a1[maxn], a2[maxn];
int L[maxn], size[maxn], R[maxn];
bool book = false;
 
void dfs(int l, int r) {
    if (l >= r)
        return;
    int root = a1[l];
    int lroot = a1[l + 1];
    int rroot = a2[pos2[root] - 1];
    if (lroot == rroot) {
        R[root] = rroot;
        book = true;
        dfs(l + 1, r);
        return;
    }
    int lsize = pos1[rroot] - pos1[lroot];
    L[root] = lroot;
    R[root] = rroot;
    dfs(l + 1, l + lsize);
    dfs(l + lsize + 1, r);
}
 
void dfs3(int now) {
    if (L[now])
        dfs3(L[now]);
    cout << now << " ";
    if (R[now])
        dfs3(R[now]);
    if (now == a1[1])
        cout << endl;
}
 
int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        size[i] = 1;
        cin >> a1[i];
        pos1[a1[i]] = i;
    }
    for (int i = 1; i <= n; i++) {
        cin >> a2[i];
        pos2[a2[i]] = i;
    }
 
    dfs(1, n);
    if (book)
        cout << "No" << endl;
    else
        cout << "Yes" << endl;
    dfs3(a1[1]);
 
    return 0;
}