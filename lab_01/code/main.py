from time import clock_gettime, clock_gettime_ns, CLOCK_PROCESS_CPUTIME_ID
from LevRecursive import LevRecursive
from LevIterative import LevIterative
from LevRecursiveWithMat import LevRecursiveWithMat
from DamerauLev import DamerauLev
from random import choice
from string import ascii_lowercase
from resource import getrusage, RUSAGE_CHILDREN, RUSAGE_SELF

cnts = 100

def get_time(algorithm, s1, s2, print_data=True):
    timer = 0.
    for _ in range(cnts):
        # l_time = clock_gettime(CLOCK_PROCESS_CPUTIME_ID)
        l_time = getrusage(RUSAGE_SELF)
        algorithm.find_distance(s1, s2)
        l_time2 = getrusage(RUSAGE_SELF)
        l_time = (l_time2[0] - l_time[0]) + (l_time2[1] - l_time[1])
        # l_time = clock_gettime(CLOCK_PROCESS_CPUTIME_ID) - l_time
        timer += l_time * 10000000
    timer /= cnts
    if print_data:
        print(algorithm)
        print("CPU time: ", int(timer), " mks")
        print("Result: ", algorithm.find_distance(s1, s2))
    return round(timer)

def get_random_str(length):
    return ''.join(choice(ascii_lowercase) for _ in range(length))


recAlgorithm = LevRecursive()
iterAlgorithm = LevIterative()
recCacheAlgorithm = LevRecursiveWithMat()
damerauAlgorithm = DamerauLev()

print("Введите первую строку: ", end="")
s1 = input()
print("Введите вторую строку: ", end="")
s2 = input()

print("Строка 1: ", s1)
print("Строка 2: ", s2)
get_time(recAlgorithm, s1, s2)
get_time(iterAlgorithm, s1, s2)
get_time(recCacheAlgorithm, s1, s2)
get_time(damerauAlgorithm, s1, s2)

# for i in [5, 7, 10, 20, 50, 100]:
#     s1 = get_random_str(i)
#     s2 = get_random_str(i)
#     it_time = get_time(iterAlgorithm, s1, s2, False)
#     r_c_time = get_time(recCacheAlgorithm, s1, s2, False)
#     d_time = get_time(damerauAlgorithm, s1, s2, False)
#     if i < 10:
#         rec_time = get_time(recAlgorithm, s1, s2, False)
#         print(i, " & ", rec_time, " & ", it_time, " & ", r_c_time, " & ", d_time, "\\\\")
#     else:
#         print(i, " & - & ", it_time, " & ", r_c_time, " & ", d_time, "\\\\")
#     print("\hline")

