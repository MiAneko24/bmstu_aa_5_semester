from StringDistanceFinder import StringDistanceFinder
import numpy as np

class LevRecursiveWithMat(StringDistanceFinder):
    def __init__(self):
        super().__init__()

    def find_distance(self, s1, s2):
        mat = self.init_matrix(len(s1), len(s2))
        return self.__find_distance(s1, s2, mat)

    def __find_distance(self, s1, s2, mat): 
        i = len(s1)
        j = len(s2)
        if mat[i][j] != np.inf:
            return mat[i][j]
        if i == 0:
            return j
        if j == 0:
            return i
        D = self.__find_distance(s1[:-1], s2, mat) + 1
        D = min(D, self.__find_distance(s1, s2[:-1], mat) + 1)
        m = 0 if s1[-1] == s2[-1] else 1
        D = min(D, self.__find_distance(s1[:-1], s2[:-1], mat) + m)
        mat[i][j] = D
        return D
    
    def __str__(self) -> str:
        return "Рекурсивный алгоритм Левенштейна с заполнением матрицы"