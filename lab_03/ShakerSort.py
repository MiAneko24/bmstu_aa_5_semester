from Sort import Sort


class ShakerSort(Sort):
    def __init__(self):
        super(ShakerSort, self).__init__()

    def sort(self, array, n):
        if n == 0:
            print("Ошибка")
            return array
        left = 0
        right = n - 1

        while left < right:
            for i in range(left, right):
                if array[i] > array[i + 1]:
                    array[i], array[i + 1] = array[i + 1], array[i]
            right -= 1

            for i in range(right, left, -1):
                if array[i - 1] > array[i]:
                    array[i], array[i - 1] = array[i - 1], array[i]
            left += 1
        return array

    def __str__(self):
        return "Шейкерная сортировка"
