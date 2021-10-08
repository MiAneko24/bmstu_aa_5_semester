from StringDistanceFinder import StringDistanceFinder

class LevRecursive(StringDistanceFinder):
    def __init__(self):
        super().__init__()

    def find_distance(self, s1, s2):
        return self.__find_distance(s1, s2)
    
    def __find_distance(self, s1, s2): # max stack = (len(s1) + len(s2)) * (sizeof(int) * 3 + 2 * sizeof(string)) ?? 
        if len(s1) == 0:
            return len(s2)
        elif len(s2) == 0:
            return len(s1)
        D = self.__find_distance(s1[:-1], s2) + 1
        D = min(D, self.__find_distance(s1, s2[:-1]) + 1)
        m = 0 if s1[-1] == s2[-1] else 1
        
        D = min(D, self.__find_distance(s1[:-1], s2[:-1]) + m)
        
        return D

    def __str__(self) -> str:
        return "Рекурсивный алгоритм Левенштейна"