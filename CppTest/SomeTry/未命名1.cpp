#include<iostream>
using namespace std;
int main()
{
    int x1,y1,z1,x2,y2,z2;
    cin>>x1>>y1>>z1>>x2>>y2>>z2;
    cout << (x2-x1)*3600+(y2-y1)*60+z2-z1<< endl;
    return 0;
} 
