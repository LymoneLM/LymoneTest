#include <iostream>
#include <queue>
#include <vector>
#include <string>

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

    for (int i = 0; i < n; i++) {
        if (tree[i].left != -1) {
            if (hasEmptyChild) // 出现过空节点，当前节点必须是叶子节点
                return false;
            q.push(tree[i].left);
        } else {
            hasEmptyChild = true; // 标记出现了空节点
        }

        if (tree[i].right != -1) {
            if (hasEmptyChild) // 出现过空节点，当前节点必须是叶子节点
                return false;
            q.push(tree[i].right);
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
        string leftStr, rightStr;
        cin >> leftStr >> rightStr;

        tree[i].left = (leftStr == "-") ? -1 : stoi(leftStr);
        tree[i].right = (rightStr == "-") ? -1 : stoi(rightStr);
    }

    if (isCompleteBinaryTree(tree))
        cout << "YES " << N - 1 << endl;
    else
        cout << "NO 0" << endl;

    return 0;
}
