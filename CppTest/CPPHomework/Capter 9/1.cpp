#include <bits/stdc++.h>
using namespace std;
class point
{
    double x, y;
public:
    point(double x0 = 0, double y0 = 0)
    {
        x = x0;
        y = y0;
    }
    void display();
    friend double dis(point&,point&);
};
void point::display()
{
    cout<<"("<<x<<","<<y<<")\n";
    //printf("(%lf,%lf)\n",x,y);
}
double dis(point &A,point &B)
{
    double x1=A.x,y1=A.y;
    double x2=B.x,y2=B.y;
    return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
}
int main()
{
    double x1,y1,x2,y2;
    cin>>x1>>y1>>x2>>y2;
    point A(x1,y1),B(x2,y2);
    A.display();
    B.display();
    cout<<dis(A,B);
    return 0;
}