#include <bits/stdc++.h>
using namespace std;
class node
{
    public:
    int name;
    node *next;
};
class link
{
    node *head,*rear;
    node *tp;
    public:
    int add(int n)
    {
        int m=n-2;
        while(m--)
            tp=tp->next;
        node *p=tp->next;
        tp->next=p->next;
        m=p->name;
        delete p;
        return m;
    }
    void en(int n)
    {
        node *p=new node;
        p->name=n;
        rear->next=p;
        rear=p;
        p->next=head;
    }
    link()
    {
        tp=new node;
        tp->name=1;
        tp->next=tp;
        head=rear=tp;
        for(int i=2;i<=12;i++)
            en(i);
    }
};
int main()
{
    int k,m,n=12;
    cin>>k;
    link data;
    while(n--)
        m=data.add(k);
    cout<<m;
    return 0;
}