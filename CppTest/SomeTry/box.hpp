#include<bits/stdc++.h>
using namespace std;
class Box {
private:
    int height, length;
    char ch;
    bool isSolid;
    string text;
public:
    Box(int h, int l, char q = '.') : height(h), length(l), ch(q),isSolid(false){}
    Box operator+(){
        Box ans(height,length,ch);
        ans.isSolid=true;
        return ans;
    }
    Box operator*(const int right){
        Box ans=*this;
        ans.height=height*right;
        ans.length=length*right;
        return ans;
    }
    Box operator=(const Box sourc){
        this->height=sourc.height;
        this->length=sourc.length;
        this->ch=sourc.ch;
        this->isSolid=sourc.isSolid;
        return sourc;
    }
    friend ostream &operator<<(ostream &output, const Box object){ 
        for(int i=0;i<object.length-1;i++)
            output<<object.ch<<' ';
        output<<object.ch<<'\n';
        if(object.isSolid==true){
            for(int t=0;t<object.height-2;t++){
                for(int i=0;i<object.length-1;i++)
                    output<<object.ch<<' ';
                output<<object.ch<<'\n';
            }
        }else{
            int at=0;
            int len=object.text.length();
            int tlen=2*object.length-3;
            for(int t=0;t<object.height-2;t++){
                output<<object.ch;
                for(int i=0;i<tlen;i++)
                    output<<(at<len?object.text[at++]:' ');
                output<<object.ch<<'\n';
            }
        } 
        for(int i=0;i<object.length-1;i++)
            output<<object.ch<<' ';
        output<<object.ch<<'\n';
        int max=(2*object.length-3)*(object.height-2);
        int len=object.text.length();
        if(len>max)
            for(int i=max;i<len;i++)
                output<<object.text[i];
        return output;            
    }
    void contain(const string X){
        text=X;
    }
};