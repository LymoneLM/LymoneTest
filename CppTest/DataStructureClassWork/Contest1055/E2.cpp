#include <iostream>
#include <string>
#include <queue>
#include <sstream>

struct TreeNode {
    int index;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int i) : index(i), left(nullptr), right(nullptr) {}
};

bool isCompleteBinaryTree(TreeNode* root, int nodeCount) {
    if (root == nullptr) {
        return true;
    }

    std::queue<TreeNode*> q;
    q.push(root);

    int currentIndex = 0;

    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();

        if (node->index != currentIndex) {
            return false;
        }

        currentIndex++;

        if (node->left != nullptr) {
            q.push(node->left);
        } else if (currentIndex < nodeCount) {
            return false;
        }

        currentIndex++;

        if (node->right != nullptr) {
            q.push(node->right);
        } else if (currentIndex < nodeCount) {
            return false;
        }

        currentIndex++;
    }

    return true;
}

TreeNode* buildTree(const std::vector<std::string>& treeData) {
    std::vector<TreeNode*> nodes(treeData.size());

    for (int i = 0; i < treeData.size(); ++i) {
        if (treeData[i] != "-") {
            nodes[i] = new TreeNode(i);
        }
    }

    for (int i = 0; i < treeData.size(); ++i) {
        if (treeData[i] != "-") {
            TreeNode* node = nodes[i];
            int leftIndex, rightIndex;
            std::istringstream iss(treeData[i]);
            iss >> leftIndex >> rightIndex;

            if (leftIndex != -1) {
                node->left = nodes[leftIndex];
            }

            if (rightIndex != -1) {
                node->right = nodes[rightIndex];
            }
        }
    }

    return nodes[0];
}

int main() {
    int n;

    while (std::cin >> n) {
        std::vector<std::string> treeData(n);

        for (int i = 0; i < n; ++i) {
            std::cin >> treeData[i];
        }

        TreeNode* root = buildTree(treeData);
        bool isComplete = isCompleteBinaryTree(root, n);

        if (isComplete) {
            std::cout << "YES " << n - 1 << std::endl;
        } else {
            std::cout << "NO 0" << std::endl;
        }
    }

    return 0;
}
