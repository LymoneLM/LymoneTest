Node = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.5],
    [2.0, 0.0, 0.0],
    [0.0, 1.0, 0.3],
    [1.0, 1.0, 1.0],
    [2.0, 1.0, 0.7],
    [0.0, 2.0, 0.0],
    [1.0, 2.0, 0.2],
    [2.0, 2.0, 0.0]
]
Cover = [
    [0, 1, 4],
    [0, 4, 3],
    [1, 2, 4],
    [2, 5, 4],
    [3, 4, 6],
    [4, 7, 6],
    [4, 5, 8],
    [4, 8, 7],
]


def get_area(A, B, C):
    AB = (B[0] - A[0], B[1] - A[1], B[2] - A[2])
    AC = (C[0] - A[0], C[1] - A[1], C[2] - A[2])

    cross_x = AB[1] * AC[2] - AB[2] * AC[1]
    cross_y = AB[2] * AC[0] - AB[0] * AC[2]
    cross_z = AB[0] * AC[1] - AB[1] * AC[0]

    area = 0.5 * (cross_x ** 2 + cross_y ** 2 + cross_z ** 2) ** 0.5
    return area


def get_constant_load(A, B, C, p):
    return get_area(A, B, C) * p


def get_live_load(A, B, C, p):
    def to_contour(node):
        return [node[0], node[1], 0]

    A, B, C = to_contour(A), to_contour(B), to_contour(C)
    return get_area(A, B, C) * p


if __name__ == "__main__":
    for f in range(len(Cover)):
        A, B, C = Node[Cover[f][0]], Node[Cover[f][1]], Node[Cover[f][2]]
        print(f"{f}号屋面板： " +
              f"恒载荷：{get_constant_load(A, B, C, 1.0)}kN " +
              f"活载荷：{get_live_load(A, B, C, 0.5)}kN ")
