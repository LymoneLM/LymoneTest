int logarithm(int x)
{
    int ans = 0;
    for(int t=x;t<=x+300;t++){
        int sum=0,sum2=0;
        for(int i=1; i<=sqrt(t); i++)
            if(t%i == 0)
                sum+=i;
        for(int i=1; i<=sqrt(sum); i++)
            if(sum%i == 0)
                sum2+=i; 
        if(sum2==t){
            ans = t;
            break;
        }
    }
    return ans;
}