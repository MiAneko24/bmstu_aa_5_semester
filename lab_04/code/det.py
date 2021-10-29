import time
from multiprocessing import Process, Manager, freeze_support
import random
import numpy as np
import matplotlib.pyplot as plt


class Matrix:
    mult = 0
    size = 0
    matrix = []

    def __init__(self, size, mult=1, matrix=None):
        self.mult = mult
        self.size = size
        if matrix is not None:
            self.matrix = matrix
        else:
            self.matrix = np.zeros((size, size))

    def __str__(self):
        return f'size = {self.size}, mul = {self.mult}, matrix = {self.matrix}'

    def randomize(self):
        self.matrix = []
        self.mult = 1
        for i in range(self.size):
            self.matrix.append([])
            for j in range(self.size):
                self.matrix[-1].append(random.randint(-1000, 1000))
        print(f'Generated matrix  {self.matrix}')
        return self


def calculateDet(m: Matrix):
    s = 0                                                   # 1
    if m.size == 1:                                         # 2
        s = m.matrix[0][0] * m.mult                         # 3
    else:                                                   
        for i in range(m.size):                             # 4
            mul = m.matrix[0][i] * m.mult                   # 5
            if i % 2 == 1:                                  # 6
                mul *= -1                                   # 7
            size = m.size - 1                               # 8
            new_mat = Matrix(size, mul)                     # 9
            for j in range(1, m.size):                      # 10
                cnt = 0                                     # 11
                for k in range(m.size):                     # 12
                    if k != i:                              # 13
                        new_mat.matrix[j - 1][cnt] = m.matrix[j][k] # 14
                        cnt += 1                                    # 15
            s += calculateDet(new_mat)                              # 16
    return s                                                        


def calculateDetThreading(matrixes, returnList: list):
    s = 0
    for m in matrixes:
        s += calculateDet(m)
    returnList.append(s)


class Dispatcher:
    def __init__(self, size: int = 0, matrix: Matrix = None):
        self.m = matrix
        if size == 0: size = 9
        if self.m is None:
            self.m = Matrix(size).randomize()
        self.threadCount = 1
        self.threadManager = Manager()
        self.returnList = self.threadManager.list()

    def dispatch(self):
        activeThreads = []
        matrixPerThread = self.m.size / self.threadCount
        allMatrixes = []
        for i in range(self.m.size):
            mul = self.m.matrix[0][i] * self.m.mult
            if i % 2 == 1:
                mul *= -1
            size = self.m.size - 1
            matrix = []
            for j in range(1, self.m.size):
                matrix.append([])
                for k in range(self.m.size):
                    if k != i:
                        matrix[-1].append(self.m.matrix[j][k])
            allMatrixes.append(Matrix(size, mul, matrix))
        startIndex = 0
        threadTasksCount = []
        for i in range(self.threadCount):
            endIndex = round(matrixPerThread * (i + 1))
            if i == self.threadCount - 1:  # последний thread
                threadMatrixes = allMatrixes[startIndex:]
            else:
                threadMatrixes = allMatrixes[startIndex:endIndex]
            startIndex = endIndex
            activeThreads.append(
                Process(target=calculateDetThreading, args=(threadMatrixes, self.returnList,)))
            threadTasksCount.append(len(threadMatrixes))
        for thread in activeThreads:
            thread.start()
        for thread in activeThreads:
            thread.join()
        result = sum(self.returnList)
        self.returnList = self.threadManager.list()
        return result


def inputMatrix():
    try:
        print("Введите размеры квадратной матрицы (целое число): ", end="")
        size1 = int(input())
        mat1 = np.zeros((size1, size1), dtype=float)
        print("Введите матрицу: ")
        for i in range(size1):
            line = [float(num) for num in input().split(" ")]
            if len(line) != size1:
                raise ValueError
            for j in range(size1):
                mat1[i][j] = line[j]
    except ValueError:
        raise Exception("Неверный ввод")
    return Matrix(matrix=mat1.tolist(), size=size1)


def ui():
    print(f'Введите любой символ для генерации матрицы заданного размера, нажмите Enter для ввода матрицы: ')
    a = input()
    if a != '':
        print(f'Введите размер матрицы для автоматической генерации: ', end='')
        size = int(input())
        a = Dispatcher(size=size)
    else:
        a = Dispatcher(matrix=inputMatrix())
    t = time.time()
    print('Рекурсивно вычисленный определитель', calculateDet(a.m))
    t = time.time() - t
    print(f'Без потоков, время выполнения = {t}')
    threadCount = 1
    while threadCount <= 32:
        a.threadCount = threadCount
        t = time.time()
        res = a.dispatch()
        print(f'Количество потоков: {threadCount}, время выполнения = {time.time() - t}, результат = {res}')
        threadCount *= 2


def tests():
    threadCount = 1
    sizes = []
    minMatrixSize = 4
    maxMatrixSize = 9
    maxThreadsCount = 24
    repeatCount = 10
    results = []
    for i in range(minMatrixSize, maxMatrixSize + 1):
        sizes.append(i)
    results.append(sizes)
    while threadCount <= maxThreadsCount:
        print('threads', threadCount)
        timeResults = []
        a = Dispatcher()
        a.threadCount = threadCount
        for i in range(minMatrixSize, maxMatrixSize + 1):
            t = 0
            for j in range(repeatCount):
                a.m = Matrix(size=i).randomize()
                t_start = time.time()
                a.dispatch()
                t += (time.time() - t_start) * 1000
            t /= repeatCount
            timeResults.append(t)
        results.append(timeResults)
        plt.plot(sizes, timeResults, label=f'{threadCount} поток(ов)')
        if (threadCount == 16):
            threadCount = 6 * 4
        else:
            threadCount *= 2
    for j in range(len(results[0])):
        for i in range(len(results)):
            if (i != len(results) - 1):
                print("{:4.0f} & ".format(results[i][j]), end='')
            else:
                print("{:4.0f}".format(results[i][j]))
        print("\\\\ \n \hline")
    plt.legend(loc='upper left')
    plt.xlabel('Размерность')
    plt.ylabel('Время работы (мс)')
    # plt.title('Зависимость времени работы от размерности матрицы и количества потоков')
    plt.show()


if __name__ == '__main__':
    freeze_support()
    # ui()
    tests()