#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

struct Node {
    char data;
    Node *l, *r;
};

void postOrderTraversal(Node *p) {
    if (p->l != NULL)
        postOrderTraversal(p->l);
    if (p->r != NULL)
        postOrderTraversal(p->r);
    cout << p->data;
    delete p;
}

Node *creatBTreeIP(char *ins, char *posts, int n) {
    if (n == 0)
        return NULL;
    Node *p = new Node;
    p->data = posts[n - 1];
    int i = 0;
    while (ins[i] != posts[n - 1])
        i++;
    p->l = creatBTreeIP(ins, posts, i);
    p->r = creatBTreeIP(ins + i + 1, posts + i, n - i - 1);
    return p;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    char ins[30], posts[30], ctrl;
    cin >> ins >> posts >> ctrl;
    Node *p = creatBTreeIP(ins,posts,strlen(ins));
    ctrl == 'L' ? postOrderTraversal(p->l):postOrderTraversal(p->r);
    cout<<endl;
    
    return 0;
}