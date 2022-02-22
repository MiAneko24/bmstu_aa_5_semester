from matplotlib import pyplot as plt


class Search(object):
    def binary(size, key):
        L = 0
        R = size - 1
        found = False
        count = 0

        while (L <= R and not found):
            mid = (L + R) // 2
            res = key - mid
            count += 1
            
            if res < 0:
                R = mid -1
            elif res > 0:
                L = mid + 1
            else:
                found = True
        return count
        
class Plot(object):
    def Bar(x, y, title, xlabel, ylabel, comp = False):
        plt.figure(figsize=(22,7))
        plt.xlim(min(x), max(x))

        if comp:
            plt.bar(x, y, width = 0.01)
        else:
            plt.bar(x, y)

        plt.title(title)
        plt.xlabel(xlabel, fontsize=15)
        plt.ylabel(ylabel, fontsize=15)
        plt.show()
    
    def swap_axis(X, Y):
        til = max(Y)
        data = [[X[i], Y[i]] for i in range(len(X))]
        X = []
        Y = []
        for i in range(1, til + 1):
            temp = []
            for el in data:
                if el[1] == i:
                    temp.append(el[0])
            if len(temp) == 0:
                continue
            temp.sort()
            start = i - 0.95
            step = 0.9 / len(temp)
            for el in temp:
                X.append(start)
                start += step
                Y.append(el)
        return X, Y


def read_data():
    animals_dict = {}
    f = open("/home/mianeko/university_stuff/bmstu_aa_5_semester/lab_07/src/data.txt", "r")
    l = [i.split("\n")[0].split("~") for i in f.readlines()]
    f.close()
    for kv in l:
        if kv[0] not in animals_dict.keys():
            animals_dict[kv[0]] = kv[1]
    # f = open("/home/mianeko/university_stuff/bmstu_aa_5_semester/lab_07/src/data.txt", "w")
    # for t in animals_dict.items():
    #     f.write(f"{t[0]}~{t[1]}\n")
    # f.close()
    return animals_dict


def search_simple(key, animals_dict):
    cnt = 0
    for dict_key in animals_dict.keys():
        cnt += 1
        if key == dict_key:
            return animals_dict[key], cnt
    return None, 0

def bin_search(key, animal_dict):
    keys = list(animal_dict.keys())
    cnt = 0
    i = 0
    j = len(animal_dict) - 1
    m = int(j / 2)

    while keys[m] != key and i < j:
        cnt += 1
        if key > keys[m]:
            i = m + 1
        else:
            j = m - 1
        m = int((i + j) / 2)
    cnt += 1
    if keys[m] != key:
        return None, cnt
    else:
        return animal_dict[keys[m]], cnt

def combined_search(key, seg_dict):
    cur_dict = {}
    a = key[0]
    if a < 'A' or a > 'Z':
        return None, 0
    else:
        cnt = 0
        for i in seg_dict.keys():
            cnt += 1
            if i == key[0]:
                cur_dict = seg_dict[i]
                break
        if len(cur_dict) == 0:
            return None, 0

        r, c = bin_search(key, cur_dict)
        return r, c+cnt

def get_seg_dict(animals_dict):
    seg_dict = {}
    for a in animals_dict.keys():
        if a[0] not in seg_dict.keys():
            seg_dict[a[0]] = {}
    for i in animals_dict.items():
        seg_dict[i[0][0]][i[0]] = i[1]
    return seg_dict

def sort(animals_dict):
	sorted_list = sorted(animals_dict.items())
	sorted_dict = {}
	for i in range(len(sorted_list)):
		sorted_dict[sorted_list[i][0]] = sorted_list[i][1]
	return sorted_dict

def sort_frequent(seg_dict):
    s = sorted([len(seg[1]) for seg in seg_dict.items()], reverse=True)
    new_d = {}
    for i in s:
        for seg in seg_dict.items():
            if len(seg[1]) == i:
                new_d[seg[0]] = seg[1]
    return new_d


size = 4000
segment_sizes = [207, 424, 398, 174, 131, 124, 290, 135, 41, 57, 76, 198,\
        201, 60, 86, 205, 10, 234, 483, 123, 6, 48, 243, 0, 36, 10]
if __name__ == "__main__":
    animal_dict = sort(read_data())
    seg_dict = sort_frequent(get_seg_dict(animal_dict))
    # print(seg_dict.keys())
    # print(seg_dict)
    key = input("Введите ключ: ")
    print("Результат работы алгоритма полного перебора: ")
    t = search_simple(key, animal_dict)
    if (t[0] == None):
        print("Ключ не найден ", t[1])
    else:
        print(t)
        
    print("Результат работы алгоритма бинарного поиска: ")
    t = bin_search(key, animal_dict)
    if (t[0] == None):
        print("Ключ не найден ", t[1])
    else:
        print(t)
        
    print("Результат работы комбинированного алгоритма: ")
    t = combined_search(key,seg_dict)
    if (t[0] == None):
        print("Ключ не найден ", t[1])
    else:
        print(t)

    # X = [x for x in range(len(animal_dict))]
    # Y = [search_simple(i, animal_dict)[1] for i in animal_dict.keys()]
    
    # Plot.Bar(X, Y, "", 'Номер ключа', "Сравнения") #Key out
    # X, Y = Plot.swap_axis(X, Y) #To compares
    # Plot.Bar(X, Y, "", "Сравнения", 'Номер ключа', True)