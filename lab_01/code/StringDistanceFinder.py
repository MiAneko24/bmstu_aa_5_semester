import numpy as np

class StringDistanceFinder:
    def __init__(self) -> None:
        pass

    def find_distance(self, s1, s2):
        pass

    def init_matrix(self, n, m):
        mat = np.full((n + 1, m + 1), np.inf)
        for i in range(n + 1):
            mat[i][0] = i
        for j in range(m + 1):
            mat[0][j] = j
        return mat
        
