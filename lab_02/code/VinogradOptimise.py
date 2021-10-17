import numpy as np

from MatrixMultiplication import MatrixMultiplication

class VinogradOptimise(MatrixMultiplication):
    def __init__(self):
        super(VinogradOptimise, self).__init__()

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
                buff = mulH[i] - mulV[j]
                for k in range(0, m - 1, 2):
                    # print("k = ", k)
                    buff += (mat1[i][k] + mat2[k + 1][j]) * \
                                 (mat1[i][k + 1] + mat2[k][j])
                if m % 2 == 1:
                    buff += mat1[i][m - 1] * mat2[m - 1][j]
                mat3[i][j] = buff

        return mat3

    def get_mulH(self, mat1):
        mulH = np.zeros(mat1.shape[0], dtype=float)
        for i in range(mat1.shape[0]):
            for k in range(0, mat1.shape[1] - 1, 2):
                mulH[i] -= mat1[i][k] * mat1[i][k + 1]
        return mulH

    def get_mulV(self, mat2):
        mulV = np.zeros(mat2.shape[1], dtype=float)
        for i in range(mat2.shape[1]):
            for k in range(0, mat2.shape[0] - 1, 2):
                mulV[i] += mat2[k][i] * mat2[k + 1][i]
        return mulV

    def __str__(self):
        return "Оптимизированный алгоритм Винограда умножения матриц"