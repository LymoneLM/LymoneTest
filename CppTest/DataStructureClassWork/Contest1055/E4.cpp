#include <iostream>
#include <vector>
#include <queue>
#include <string>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

bool isCompleteBinaryTree(const std::vector<std::pair<int, int>>& tree) {
    std::queue<TreeNode*> q;
    q.push(new TreeNode(0));  // 根节点的索引为0

    int i = 1;
    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();

        if (i < tree.size()) {
            if (tree[i].first != -1) {
                node->left = new TreeNode(tree[i].first);
                q.push(node->left);
            }
            i++;

            if (i < tree.size()) {
                if (tree[i].first != -1) {
                    node->right = new TreeNode(tree[i].first);
                    q.push(node->right);
                }
                i++;
            }
        }
    }

    return i == tree.size();
}

void levelOrderTraversal(TreeNode* root, int& lastNodeIndex) {
    std::queue<TreeNode*> q;
    q.push(root);

    while (!q.empty()) {
        TreeNode* node = q.front();
        q.pop();

        lastNodeIndex = node->val;  // 更新最后一个节点的索引

        if (node->left) {
            q.push(node->left);
        }

        if (node->right) {
            q.push(node->right);
        }
    }
}

int main() {
    int N;
    while (std::cin >> N) {
        std::vector<std::pair<int, int>> tree(N);
        for (int i = 0; i < N; ++i) {
            int left, right;
            std::cin >> left >> right;
            tree[i] = std::make_pair(left, right);
        }

        if (isCompleteBinaryTree(tree)) {
            int lastNodeIndex = -1;
            levelOrderTraversal(new TreeNode(0), lastNodeIndex);
            std::cout << "YES " << lastNodeIndex << std::endl;
        } else {
            std::cout << "NO 0" << std::endl;
        }
    }

    return 0;
}
