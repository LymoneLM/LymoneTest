#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;
int euler(int n){
    int ans = n;
    for (int i = 2; i*i <= n; i++)
        if (n % i == 0) {
            ans = ans / i * (i - 1);
            while (n % i == 0) n /= i;
        }
    if (n > 1) ans = ans / n * (n - 1);
    return ans;
}
inline void soluteA(){
    int T;
    cin>>T;
    while(T--){
        int N;
        cin>>N; 
        cout<<euler(N)<<endl;
    }
}
inline void soluteB(){
    int T;
    cin>>T;
    while(T!=0){
        cout<<euler(T)<<endl;
        cin>>T;
    }
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    //soluteA();
    soluteB();
    
    return 0;
}