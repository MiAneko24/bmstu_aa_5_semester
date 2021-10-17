import matplotlib.pyplot as plt
import numpy as np

from resource import getrusage, RUSAGE_SELF
from random import randint
from copy import deepcopy

from MatrixMultiplication import MatrixMultiplication
from VinogradMultiply import VinogradMultiply
from VinogradOptimise import VinogradOptimise

cnts = 10

def get_matrix(shape):
    return np.random.randint(0, 100, shape)

def generate_data():
    data = []
    for i in range(10, 111, 20):
        mat1 = get_matrix((i, i))
        mat2 = get_matrix((i, i))
        data.append([i, mat1, mat2])
        mat1 = get_matrix((i + 1, i + 1))
        mat2 = get_matrix((i + 1, i + 1))
        data.append([i + 1, mat1, mat2])
    return data

def get_time(alg, mat1, mat2, print_data=True):
    timer = 0.
    for _ in range(cnts):
        # l_time = clock_gettime(CLOCK_PROCESS_CPUTIME_ID)
        l_time = getrusage(RUSAGE_SELF)
        r = alg.multiply(mat1, mat2)
        l_time2 = getrusage(RUSAGE_SELF)
        l_time = (l_time2[0] - l_time[0]) + (l_time2[1] - l_time[1])
        timer += l_time * 10000000
        if r is None:
            print("Невозможно умножить матрицы (", mat1.shape[0], ", ", mat1.shape[1], \
                  ") и (", mat2.shape[0], ", ", mat2.shape[1], ")")
            return
        # l_time = clock_gettime(CLOCK_PROCESS_CPUTIME_ID) - l_time
    timer /= cnts
    if print_data:
        print(alg)
        print("CPU time: ", int(timer), " mks")
        print("Result: \n", alg.multiply(mat1, mat2))
    return round(timer)


def get_random_array(length):
    return np.random.randint(0, length * 10, length)


algorithms = []
algorithms.append(MatrixMultiplication())
algorithms.append(VinogradMultiply())
algorithms.append(VinogradOptimise())
err = False
try:
    print("Введите размеры первой матрицы (два целых числа через пробел): ", end="")
    size1 = [int(i) for i in input().split(" ")]
    print(size1)
    if len(size1) != 2:
        raise ValueError
    mat1 = np.zeros(size1, dtype=float)
    print("Введите первую матрицу: ")
    for i in range(size1[0]):
        line = [float(num) for num in input().split(" ")]
        if len(line) != size1[1]:
            raise ValueError
        for j in range(size1[1]):
            mat1[i][j] = line[j]
    print("Введите размеры второй матрицы (два целых числа через пробел): ", end="")
    size2 = [int(i) for i in input().split(" ")]
    if len(size2) != 2:
        raise ValueError
    mat2 = np.zeros(size2, dtype=float)
    print("Введите вторую матрицу: ")
    for i in range(size2[0]):
        line = [float(num) for num in input().split(" ")]
        if len(line) != size2[1]:
            raise ValueError
        for j in range(size2[1]):
            mat2[i][j] = line[j]

except ValueError:
    err = True
    print("Некорректный ввод")


if not err:
    print("Первая матрица: \n", mat1, "\nВторая матрица:\n", mat2)
    for alg in algorithms:
        get_time(alg, mat1, mat2)

# data = generate_data()
# x = [case[0] for case in data]
# result_y=[[],[],[]]
# for case in data:
#     print(case[0], end="")
#     for i in range(len(algorithms)):
#         result_y[i].append(get_time(algorithms[i], case[1], case[2], False))
#         print(" & ", result_y[i][-1], end='')
#         # print(" & ", get_time(algorithms[i], case[1], case[2], False), end='')
#     print("\\\\ \n \hline")

# plt.plot(x, result_y[0], color='red', label="Классик")
# plt.plot(x, result_y[1], color='green', label='Виноград')
# plt.plot(x, result_y[2], color='blue', label='Оптим')
# plt.xlabel("Размер")
# plt.ylabel("Время")
# plt.legend(loc='upper left')
# plt.show()
