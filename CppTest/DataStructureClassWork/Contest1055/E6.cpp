#include <iostream>
#include <vector>
#include <queue>
#include <sstream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

bool isCompleteBinaryTree(TreeNode* root) {
    if (root == nullptr) {
        return false;
    }

    std::queue<TreeNode*> q;
    q.push(root);

    bool hasNullChild = false;

    while (!q.empty()) {
        TreeNode* curr = q.front();
        q.pop();

        if (curr->left) {
            if (hasNullChild) {
                return false;
            }
            q.push(curr->left);
        } else {
            hasNullChild = true;
        }

        if (curr->right) {
            if (hasNullChild) {
                return false;
            }
            q.push(curr->right);
        } else {
            hasNullChild = true;
        }
    }

    return true;
}

int main() {
    int N;
    std::cin >> N;

    std::vector<TreeNode*> nodes(N);
    for (int i = 0; i < N; ++i) {
        nodes[i] = new TreeNode(i);
    }

    for (int i = 0; i < N; ++i) {
        int left, right;
        std::cin >> left >> right;
        if (left != -1) {
            nodes[i]->left = nodes[left];
        }
        if (right != -1) {
            nodes[i]->right = nodes[right];
        }
    }

    TreeNode* root = nodes[0];

    if (isCompleteBinaryTree(root)) {
        std::cout << "YES " << N - 1 << std::endl;
    } else {
        std::cout << "NO 0" << std::endl;
    }

    return 0;
}
