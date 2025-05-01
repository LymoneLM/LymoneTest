#include <bits/stdc++.h>
#pragma GCC optimize(2)
#define endl "\n"
#define ll long long
#define INF 0x3f3f3f3f
#define mm(a) memset(a, 0, sizeof(a))
using namespace std;

class Node {
public:
    int weight;
    Node *left, *right;
    Node(int _weight) : weight(_weight) {
        left = right = NULL;
    }
    Node(const Node &n) {
        weight = n.weight;
        left = n.left;
        right = n.right;
    }
    friend bool operator<(Node l, Node r) {
        return l.weight < r.weight;
    }
    ll Travel(int deep){
        if(left=NULL)
            return deep*weight;
        return left->Travel(deep+1)+right->Travel(deep+1);
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, temp;
    set<Node> forest;
    while (cin >> n) {
        ll weight = 0;
        for (int i = 0; i < n; i++) {
            cin >> temp;
            forest.insert(Node(temp));
        }
        Node *A, *B;
        for (int i = 1; i < n; i++) {
            A = new Node(*forest.begin());
            forest.erase(forest.begin());
            B = new Node(*forest.begin());
            forest.erase(forest.begin());
            Node C(A->weight + B->weight);
            C.left=A;
            C.right=B;
            forest.insert(C);
        }
        A = new Node(*forest.begin());
        cout<<A->Travel(0)<<endl;
    }

    return 0;
}