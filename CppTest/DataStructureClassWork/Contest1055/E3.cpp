#include <bits/stdc++.h>

using namespace std;

const int N = 30;
int n;
int l[N], r[N];
bool hf[N];
int maxCur = -1, nodeId;

void dfs(int u, int cur)
{
    if(cur > maxCur)
    {
        maxCur = cur;
        nodeId = u;
    }
    if(l[u] != -1) dfs(l[u], 2 * cur);
    if(r[u] != -1) dfs(r[u], 2 * cur + 1);
}

int main()
{
    cin >> n;
    for(int i = 0; i < n; i++)
    {
        string a, b;
        cin >> a >> b;
        if(a != "-")
        {
            l[i] = stoi(a);
            hf[stoi(a)] = true;
        }
        else l[i] = -1;
        if(b != "-")
        {
            r[i] = stoi(b);
            hf[stoi(b)] = true;
        }
        else r[i] = -1;
    }
    int root = 0;
    while(hf[root]) root ++;

    dfs(root, 1);
    
    if(maxCur == n)
        cout << "YES" << ' ' << nodeId << endl;
    else
        cout << "NO" << ' ' << root << endl;
}