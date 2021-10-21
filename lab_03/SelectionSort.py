from Sort import Sort


class SelectionSort(Sort):
    def __init__(self):
        super(SelectionSort, self).__init__()

    def sort(self, array, n):
        if n == 0:
            print("Ошибка")
            return array
        for i in range(n - 1):
            min_i = i
            for j in range(i + 1, n):
                if array[j] < array[min_i]:
                    min_i = j
            array[i], array[min_i] = array[min_i], array[i]
        return array

    def __str__(self):
        return "Сортировка выбором"
