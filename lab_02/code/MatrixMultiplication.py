import numpy as np


class MatrixMultiplication:
    def __init__(self):
        pass

    def multiply(self, mat1, mat2):
        if len(mat1) == 0 or len(mat2) == 0 or mat1.shape[1] != mat2.shape[0]:
            return None
        n = mat1.shape[0]
        m = mat1.shape[1]
        q = mat2.shape[1]
        mat3 = np.zeros((n, q), dtype=float)
        for i in range(n):
            for j in range(q):
                for k in range(m):
                    mat3[i][j] += mat1[i][k] * mat2[k][j]

        return mat3

    def __str__(self):
        return "Классический алгоритм умножения матриц"
