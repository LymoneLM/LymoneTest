#include <bits/stdc++.h>
using namespace std;
char*findLast(char*sourceStr,char*subStr)
{
    char* p=sourceStr-1;
    int i=0;
    while (sourceStr[i]!='\0')
    {
        if(sourceStr[i]==subStr[0])
        {
            int add=0;
            while (++add)
            {
                if(subStr[add]=='\0')
                {
                    p=sourceStr+i;
                    break;
                }
                if(subStr[add]!=sourceStr[i+add])
                    break;
            }         
        }
        i++;
    }
    return p;
}
int main()
{
    char sourceStr[10001],subStr[10001];
    cin.getline(sourceStr, 10000);
    cin.getline(subStr, 10000);
    cout<<findLast(sourceStr,subStr)-sourceStr;
    return 0;
}