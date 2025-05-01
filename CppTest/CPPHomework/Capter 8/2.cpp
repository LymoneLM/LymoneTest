#include <bits/stdc++.h>
using namespace std;
class Beeline
{
    int X1, Y1, X2, Y2;

public:
    Beeline(int x1 = 0, int y1 = 0, int x2 = 0, int y2 = 0) : X1(x1), Y1(y1), X2(x2), Y2(y2){}
    float Length() const
    {
        return sqrt((Y2-Y1)*(Y2-Y1)+(X2-X1)*(X2-X1));
    }
    void show() const
    {
        printf("(%d,%d),(%d,%d)\n",X1,Y1,X2,Y2);
    }
}; 
class Triangle
{
    Beeline line1,line2,line3;
    public:
    Triangle(int x1,int y1,int x2,int y2,int x3,int y3):line1(x1,y1,x2,y2),line2(x2,y2,x3,y3),line3(x3,y3,x1,y1){}
    float Area() const
    {
        float a=line1.Length(),b=line2.Length(),c=line3.Length();
        float p=(a+b+c)/2;
        return sqrt(p*(p-a)*(p-b)*(p-c));
    }
    void Print() const
    {
        cout<<"Three edges' points are listed as follows:\n";
        line1.show();
        line2.show();
        line3.show();
        printf("The area of this triangle is:%.2f",Area());
    }
};
int main()
{
    int x1,x2,x3,y1,y2,y3;
    cin>>x1>>y1>>x2>>y2>>x3>>y3;
    Triangle tri(x1,y1,x2,y2,x3,y3);
    tri.Print();
    return 0;
}