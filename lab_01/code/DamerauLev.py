from StringDistanceFinder import StringDistanceFinder
import numpy as np

class DamerauLev(StringDistanceFinder):
    def __init__(self):
        super().__init__()

    def find_distance(self, s1, s2):
        return self.__find_distance(s1, s2)

    def __find_distance(self, s1, s2):
        n = len(s1)
        m = len(s2)
        mat = self.init_matrix(n, m)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                step1 = mat[i][j - 1] + 1
                step2 = mat[i - 1][j] + 1
                elem = 0 if s1[i - 1] == s2[j - 1] else 1
                step3 = mat[i - 1][j - 1] + elem
                step4 = np.inf
                if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s2[j - 1] == s1[i - 2]:
                    step4 = mat[i - 2][j - 2] + 1
                mat[i][j] = min(step1, step2, step3, step4)
        return mat[-1][-1]

    def __str__(self) -> str:
        return "Алгоритм Дамерау-Левенштейна"