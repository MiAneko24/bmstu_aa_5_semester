import numpy as np

from MatrixMultiplication import MatrixMultiplication

class VinogradMultiply(MatrixMultiplication):
    def __init__(self):
        super(VinogradMultiply, self).__init__()

    def multiply(self, mat1, mat2):
        if len(mat1) == 0 or len(mat2) == 0 or mat1.shape[1] != mat2.shape[0]:
            return None
        n = mat1.shape[0]
        m = mat1.shape[1]
        q = mat2.shape[1]
        mat3 = np.zeros((n, q), dtype=float)
        mulH = self.get_mulH(mat1)
        mulV = self.get_mulV(mat2)

        for i in range(n):
            for j in range(q):
                mat3[i][j] = - mulH[i] - mulV[j]
                for k in range(m // 2):
                    mat3[i][j] = mat3[i][j] + (mat1[i][2 * k] + mat2[2 * k + 1][j]) * \
                    (mat1[i][2 * k + 1] + mat2[2 * k][j])

        if m % 2 == 1:
            for i in range(n):
                for j in range(q):
                    mat3[i][j] = mat3[i][j] + mat1[i][m - 1] * mat2[m - 1][j]
        return mat3

    def get_mulH(self, mat1):
        mulH = np.zeros(mat1.shape[0], dtype=float)
        for i in range(mat1.shape[0]):
            for k in range(mat1.shape[1] // 2):
                mulH[i] = mulH[i] + mat1[i][2 * k] * mat1[i][2 * k + 1]
        return mulH

    def get_mulV(self, mat2):
        mulV = np.zeros(mat2.shape[1], dtype=float)
        for i in range(mat2.shape[1]):
            for k in range(mat2.shape[0] // 2):
                mulV[i] = mulV[i] + mat2[2 * k][i] * mat2[2 * k + 1][i]
        return mulV

    def __str__(self):
        return "Алгоритм Винограда умножения матриц"