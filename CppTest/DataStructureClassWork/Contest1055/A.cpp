#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a,0,sizeof(a))
using namespace std;
char str[110];
int len,cnt=-1;
struct Node{
    char data;
    Node *left,*right;
}*Tree;
Node* CreatTree(){
    if(len==cnt||str[++cnt]==' ')
        return NULL;
    Node *p = new Node;
    p->data=str[cnt];
    p->left=CreatTree();
    p->right=CreatTree();
    return p;
}
void PreOrderTraversel(Node* p){
    cout<<p->data<<" ";
    if(p->left!=NULL) PreOrderTraversel(p->left);
    if(p->right!=NULL) PreOrderTraversel(p->right);
}
void InOrderTraversel(Node* p){
    if(p->left!=NULL) InOrderTraversel(p->left);
    cout<<p->data<<" ";
    if(p->right!=NULL) InOrderTraversel(p->right);
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin.getline(str,110);
    len=strlen(str);

    Tree = CreatTree();
    PreOrderTraversel(Tree);
    cout<<endl;
    InOrderTraversel(Tree);
    cout<<endl;
    InOrderTraversel(Tree);
    cout<<endl;
    return 0;
}