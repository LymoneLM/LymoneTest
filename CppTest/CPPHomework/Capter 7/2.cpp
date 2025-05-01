#include <bits/stdc++.h>
using namespace std;
struct person
{
    char name[20];
    int count;
} leader[3] = {"Li", 0, "Zhang", 0, "Fun", 0};
int main()
{
    char name[10];
    int n;
    cin>>n;
    for(int i = 0;i<n;i++ )
    {
        cin>>name;
        for(int i=0;i<3;i++)
        {
            if(0==strcmp(name,leader[i].name))
                leader[i].count++;
        }
    }
    for(int i=0;i<3;i++)
    {
        cout<<leader[i].name
        <<":"<<leader[i].count<<endl;
    }
    return 0;
}