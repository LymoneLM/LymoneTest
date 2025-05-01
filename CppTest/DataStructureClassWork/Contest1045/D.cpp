#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;

int matrix[110][110];
void init(int N){
    int ha=N/2;
    int cnt=1;
    for(int i=0;i<ha;i++){
        int x=i,y=i;
        int step=N-i*2-1;
        for(int j=0;j<step;j++)matrix[x++][y]=cnt++;
        for(int j=0;j<step;j++)matrix[x][y++]=cnt++;
        for(int j=0;j<step;j++)matrix[x--][y]=cnt++;
        for(int j=0;j<step;j++)matrix[x][y--]=cnt++;
    }
    if(N%2==1)
        matrix[N/2][N/2]=N*N;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin>>N;
    mm(matrix);
    init(N);

    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++)
            cout<<matrix[j][i]<<(j==N-1?'\n':' ');

    return 0;
}