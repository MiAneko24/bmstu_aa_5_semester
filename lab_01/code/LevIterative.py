from StringDistanceFinder import StringDistanceFinder

class LevIterative(StringDistanceFinder):
    def __init__(self):
        super().__init__()

    def find_distance(self, s1, s2):
        return self.__find_distance(s1, s2)

    def __find_distance(self, s1, s2): # sizeof(float) * (len(s1) + 1)(len(s2) + 1) + 7 * sizeof(int) ??
        n = len(s1)
        m = len(s2)
        mat = self.init_matrix(n, m)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                step1 = mat[i][j - 1] + 1
                step2 = mat[i - 1][j] + 1
                elem = 0 if s1[i-1] == s2[j-1] else 1
                step3 = mat[i - 1][j - 1] + elem
                mat[i][j] = min(step1, step2, step3)
        return mat[-1][-1]

    def __str__(self) -> str:
        return "Матричный алгоритм Левенштейна"