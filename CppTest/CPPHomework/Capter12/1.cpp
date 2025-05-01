#include <bits/stdc++.h>
using namespace std;
class Fruit
{
    protected:
    double W,P;
    public:
    Fruit(double w,double p):W(w),P(p){}
    virtual double operator +(double all)=0;
};
class Apple:public Fruit
{
    public:
    Apple(double w,double p):Fruit(w,p){}
    double operator+(double all)
    {
        all+=W*P;
        return all;
    }
};
class Banana:public Fruit
{
    public:
    Banana(double w,double p):Fruit(w,p){}
    double operator+(double all)
    {
        all+=W/2*P;
        return all;
    }
};
class Orange:public Fruit
{
    public:
    Orange(double w,double p):Fruit(w,p){}
    double operator+(double all)
    {
        all+=(W>10?W*P/2:(W>5?W*P*0.8:W*P));
        return all;
    }
};
int main()
{
    double all=0,w,p;
    char temp;
    Fruit* fp;
    cin>>temp;
    while(temp!='q')
    {
        cin>>w>>p;
        switch (temp)
        {
            case 'a':
            fp=new Apple(w,p);
            break;
            case 'b':
            fp=new Banana(w,p);
            break;
            case 'o':
            fp=new Orange(w,p);
            break;
        }
        all=*fp+all;
        delete fp;
        cin>>temp;
    }
    printf("%.2lf",all);
}