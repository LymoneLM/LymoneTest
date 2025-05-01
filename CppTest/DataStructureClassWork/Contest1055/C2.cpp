#include <iostream>
#include <queue>
#include <vector>

struct Node {
    int weight;
    Node* left;
    Node* right;

    Node(int w) : weight(w), left(nullptr), right(nullptr) {}
};

struct CompareNodes {
    bool operator()(Node* a, Node* b) {
        return a->weight > b->weight;
    }
};

Node* buildHuffmanTree(const std::vector<int>& leafWeights) {
    std::priority_queue<Node*, std::vector<Node*>, CompareNodes> pq;

    for (int weight : leafWeights) {
        Node* node = new Node(weight);
        pq.push(node);
    }

    while (pq.size() > 1) {
        Node* left = pq.top();
        pq.pop();
        Node* right = pq.top();
        pq.pop();

        Node* parent = new Node(left->weight + right->weight);
        parent->left = left;
        parent->right = right;

        pq.push(parent);
    }

    return pq.top();
}

int calculatePathLength(Node* root, int depth) {
    if (root == nullptr) {
        return 0;
    }

    if (root->left == nullptr && root->right == nullptr) {
        return root->weight * depth;
    }

    int leftPathLength = calculatePathLength(root->left, depth + 1);
    int rightPathLength = calculatePathLength(root->right, depth + 1);

    return leftPathLength + rightPathLength;
}

int main() {
    int n;

    while (std::cin >> n) {
        std::vector<int> leafWeights(n);

        for (int i = 0; i < n; ++i) {
            std::cin >> leafWeights[i];
        }

        Node* root = buildHuffmanTree(leafWeights);
        int pathLengthSum = calculatePathLength(root, 0);

        std::cout << pathLengthSum << std::endl;
    }

    return 0;
}
