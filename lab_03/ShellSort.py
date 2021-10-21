from Sort import Sort


class ShellSort(Sort):
    def __init__(self):
        super(ShellSort, self).__init__()
        
    def sort(self, array, n):
        if n == 0:
            print("Ошибка")
            return array
        step = n // 2
        while step > 0:
            for i in range(step, n):
                j = i
                while j >= step and array[j - step] > array[j]:
                    array[j - step], array[j] = array[j], array[j - step]
                    j -= step
            step //= 2
        return array

    def __str__(self):
        return "Сортировка Шелла"
