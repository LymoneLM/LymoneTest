#include <bits/stdc++.h>
using namespace std;
void split(double x,int* iPart,double* fPart)
{
    *iPart=x;
    *fPart=x-*iPart;
}
int main()
{
    int* iPart=new int;
    double* fPart=new double;
    double x;
    cin>>x;
    split( x, iPart, fPart);
    cout<<(*iPart)<<" "<<(*fPart);
    return 0;
}