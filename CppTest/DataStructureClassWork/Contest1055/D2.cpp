#include <iostream>
#include <string>
#include <unordered_map>

struct TreeNode {
    char val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(char v) : val(v), left(nullptr), right(nullptr) {}
};

int getHeight(TreeNode* root) {
    if (root == nullptr) {
        return 0;
    }

    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);

    return std::max(leftHeight, rightHeight) + 1;
}

TreeNode* buildTree(const std::string& preorder, const std::string& inorder, int preStart, int preEnd, int inStart, int inEnd, std::unordered_map<char, int>& inorderIndex) {
    if (preStart > preEnd || inStart > inEnd) {
        return nullptr;
    }

    char rootValue = preorder[preStart];
    TreeNode* root = new TreeNode(rootValue);

    int rootIndex = inorderIndex[rootValue];

    int leftSize = rootIndex - inStart;

    root->left = buildTree(preorder, inorder, preStart + 1, preStart + leftSize, inStart, rootIndex - 1, inorderIndex);
    root->right = buildTree(preorder, inorder, preStart + leftSize + 1, preEnd, rootIndex + 1, inEnd, inorderIndex);

    return root;
}

int main() {
    int n;

    while (std::cin >> n) {
        std::string preorder, inorder;
        std::cin >> preorder >> inorder;

        std::unordered_map<char, int> inorderIndex;
        for (int i = 0; i < n; ++i) {
            inorderIndex[inorder[i]] = i;
        }

        TreeNode* root = buildTree(preorder, inorder, 0, n - 1, 0, n - 1, inorderIndex);
        int height = getHeight(root);

        std::cout << height << std::endl;
    }

    return 0;
}
