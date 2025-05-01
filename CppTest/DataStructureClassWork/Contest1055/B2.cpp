#include <iostream>
#include <vector>
#include <climits>

int findMinVertex(const std::vector<int>& cost, const std::vector<bool>& visited, int n) {
    int minVertex = -1;
    for (int i = 0; i < n; ++i) {
        if (!visited[i] && (minVertex == -1 || cost[i] < cost[minVertex])) {
            minVertex = i;
        }
    }
    return minVertex;
}

int primMST(const std::vector<std::vector<int>>& graph, int n) {
    std::vector<int> parent(n);  // 用于存储最小生成树中每个顶点的父节点
    std::vector<int> cost(n, INT_MAX);  // 用于存储每个顶点与最小生成树的代价
    std::vector<bool> visited(n, false);  // 记录顶点是否被访问

    parent[0] = -1;  // 根节点的父节点设为-1
    cost[0] = 0;  // 根节点的代价为0

    for (int i = 0; i < n - 1; ++i) {
        int minVertex = findMinVertex(cost, visited, n);
        visited[minVertex] = true;

        for (int j = 0; j < n; ++j) {
            if (graph[minVertex][j] && !visited[j] && graph[minVertex][j] < cost[j]) {
                parent[j] = minVertex;
                cost[j] = graph[minVertex][j];
            }
        }
    }

    int minCost = 0;
    for (int i = 1; i < n; ++i) {
        minCost += cost[i];
    }

    return minCost;
}

int main() {
    int n;
    std::cin >> n;

    std::vector<std::vector<int>> graph(n, std::vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            std::cin >> graph[i][j];
        }
    }

    int minCost = primMST(graph, n);
    std::cout << minCost << std::endl;

    return 0;
}
