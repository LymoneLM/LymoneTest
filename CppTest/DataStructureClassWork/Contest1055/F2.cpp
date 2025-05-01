#include <iostream>
#include <vector>
#include <unordered_map>
#include <sstream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

TreeNode* buildTree(const std::vector<int>& inorder, const std::vector<int>& postorder,
                    int inStart, int inEnd, int postStart, int postEnd,
                    std::unordered_map<int, int>& indexMap) {
    if (inStart > inEnd || postStart > postEnd) {
        return nullptr;
    }

    int rootVal = postorder[postEnd];
    TreeNode* root = new TreeNode(rootVal);

    int rootIndex = indexMap[rootVal];

    int leftTreeSize = rootIndex - inStart;
    int rightTreeSize = inEnd - rootIndex;

    root->left = buildTree(inorder, postorder, inStart, rootIndex - 1, postStart, postStart + leftTreeSize - 1, indexMap);
    root->right = buildTree(inorder, postorder, rootIndex + 1, inEnd, postEnd - rightTreeSize, postEnd - 1, indexMap);

    return root;
}

void inorderTraversal(TreeNode* root, std::vector<int>& inorderSequence) {
    if (root == nullptr) {
        return;
    }

    inorderTraversal(root->left, inorderSequence);
    inorderSequence.push_back(root->val);
    inorderTraversal(root->right, inorderSequence);
}

int main() {
    int N;
    std::cin >> N;

    std::vector<int> preorder(N);
    std::vector<int> postorder(N);

    for (int i = 0; i < N; ++i) {
        std::cin >> preorder[i];
    }

    for (int i = 0; i < N; ++i) {
        std::cin >> postorder[i];
    }

    std::unordered_map<int, int> indexMap;

    for (int i = 0; i < N; ++i) {
        indexMap[preorder[i]] = i;
    }

    TreeNode* root = buildTree(preorder, postorder, 0, N - 1, 0, N - 1, indexMap);

    std::vector<int> inorderSequence;
    inorderTraversal(root, inorderSequence);

    std::cout << "Yes" << std::endl;
    for (int i = 0; i < inorderSequence.size(); ++i) {
        std::cout << inorderSequence[i];
        if (i != inorderSequence.size() - 1) {
            std::cout << " ";
        }
    }
    std::cout << std::endl;

    return 0;
}
