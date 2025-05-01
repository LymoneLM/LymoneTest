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
    bool hasEmptyChild = false; // 标记是否出现过空节点
    bool foundEmptyChild = false; // 标记是否找到第一个空节点

    for (int i = 0; i < n; i++) {
        if (tree[i].left != -1) {
            if (foundEmptyChild) // 如果已经找到了空节点，但当前节点不为空，则不是完全二叉树
                return false;
        } else {
            foundEmptyChild = true; // 标记已经找到第一个空节点
            hasEmptyChild = true; // 标记出现了空节点
        }

        if (tree[i].right != -1) {
            if (foundEmptyChild) // 如果已经找到了空节点，但当前节点不为空，则不是完全二叉树
                return false;
        } else {
            foundEmptyChild = true; // 标记已经找到第一个空节点
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
