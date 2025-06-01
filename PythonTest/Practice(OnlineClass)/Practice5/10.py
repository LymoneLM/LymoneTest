def isSymmetrical(lst):
    for i in range(4):
        for j in range(4):
            if lst[i][j] != lst[j][i]:
                return False
    return True


def matrix_sum(lst):
    total = 0
    for i in range(4):
        total += lst[i][i]
    return total


if __name__ == "__main__":
    matrix = []
    for _ in range(4):
        row = list(map(int, input().split(',')))
        matrix.append(row)

    if isSymmetrical(matrix):
        print("矩阵是对称矩阵")
    else:
        print("矩阵不是对称矩阵")

    print(f"矩阵对角线元素和是: {matrix_sum(matrix)}")