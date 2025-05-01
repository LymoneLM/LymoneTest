#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;
int step=0;
void move(int n,char A,char B,char C){
	if(n==1){
        cout<<++step<<' '<<1<<' '<<A<<"->"<<C<<endl;
    }else{
        move(n-1,A,C,B);
        cout<<++step<<' '<<n<<' '<<A<<"->"<<C<<endl;
        move(n-1,B,A,C);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin>>N;
    move(N,'A','B','C');

    return 0;
}