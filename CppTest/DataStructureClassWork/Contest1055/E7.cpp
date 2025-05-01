#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct TreeNode {
    int left;
    int right;
};

bool isCompleteBinaryTree(const vector<TreeNode>& tree) {
    int n = tree.size();
    queue<int> q;
    q.push(0); // 根节点的索引入队

    for (int i = 1; i < n; i++) {
        int left = tree[i].left;
        int right = tree[i].right;

        if (left != -1)
            q.push(left);

        if (right != -1)
            q.push(right);
    }

    // 遍历队列，判断是否有非空节点后面还有空节点
    while (!q.empty()) {
        int nodeIndex = q.front();
        q.pop();

        if (tree[nodeIndex].left != -1)
            q.push(tree[nodeIndex].left);

        if (tree[nodeIndex].right != -1)
            q.push(tree[nodeIndex].right);
    }

    // 判断队列中剩余的节点是否全是空节点
    while (!q.empty()) {
        if (tree[q.front()].left != -1 || tree[q.front()].right != -1)
            return false;
        q.pop();
    }

    return true;
}

int main() {
    int N;
    cin >> N;

    vector<TreeNode> tree(N);
    for (int i = 0; i < N; i++) {
        cin >> tree[i].left >> tree[i].right;
    }

    if (isCompleteBinaryTree(tree))
        cout << "YES " << N - 1 << endl;
    else
        cout << "NO 0" << endl;

    return 0;
}
