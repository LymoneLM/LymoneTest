#include <bits/stdc++.h>
using namespace std;
int f(int n, int m)
{
    return n == 1 ? n : (f(n - 1, m) + m - 1) % n + 1;
}
int main()
{
    int k;cin>>k;
    cout<<f(12,k);
    return 0;
}