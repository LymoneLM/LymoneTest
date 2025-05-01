#include <iostream>
#include <queue>
#include <vector>
#include <string>

using namespace std;

struct TreeNode {
    int left;
    int right;
};

bool isCompleteBinaryTree(vector<TreeNode>& tree) {
    int n = tree.size();
    queue<int> q;
    q.push(0); // 根节点的索引入队

    bool hasEmptyChild = false; // 标记是否出现过空节点

    for (int i = 1; i < n; i++) {
        string leftStr, rightStr;
        cin >> leftStr >> rightStr;

        int left = (leftStr == "-") ? -1 : stoi(leftStr);
        int right = (rightStr == "-") ? -1 : stoi(rightStr);

        tree[i].left = left;
        tree[i].right = right;

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
