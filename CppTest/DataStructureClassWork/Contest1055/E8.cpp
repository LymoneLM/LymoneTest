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

    bool hasEmptyChild = false; // 标记是否出现过空节点

    for (int i = 1; i < n; i++) {
        int left = tree[i].left;
        int right = tree[i].right;

        if (left != -1) {
            q.push(left);
            if (hasEmptyChild) // 出现过空节点，当前节点必须是叶子节点
                return false;
        } else {
            hasEmptyChild = true; // 标记出现了空节点
        }

        if (right != -1) {
            q.push(right);
            if (hasEmptyChild) // 出现过空节点，当前节点必须是叶子节点
                return false;
        } else {
            hasEmptyChild = true; // 标记出现了空节点
        }
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
