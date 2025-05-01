#include <iostream>
#include <queue>
#include <string>

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
        TreeNode* node = q.front();
        q.pop();

        if (node == nullptr) {
            hasNullChild = true;
        } else {
            if (hasNullChild) {
                return false;
            }

            q.push(node->left);
            q.push(node->right);
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
        std::string leftIndex, rightIndex;
        std::cin >> leftIndex >> rightIndex;

        if (leftIndex != "-") {
            nodes[i]->left = nodes[std::stoi(leftIndex)];
        }

        if (rightIndex != "-") {
            nodes[i]->right = nodes[std::stoi(rightIndex)];
        }
    }

    bool isComplete = isCompleteBinaryTree(nodes[0]);

    if (isComplete) {
        std::cout << "YES " << (N - 1) << std::endl;
    } else {
        std::cout << "NO 0" << std::endl;
    }

    return 0;
}
