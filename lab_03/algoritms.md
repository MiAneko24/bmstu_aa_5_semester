* shaker sort (шейкерная сортировка)
* Shell sort (сортировка Шелла)
* Choice sort (сортировка выбором)

## Shaker sort

```python
def ShakerSort(array):
    left = 0                                                    # 1
    right = len(array) - 1                                      # Пусть len(s) = 2, 1 + 2 + 1 = 4
    
    while left < right:                                         # 1 
        for i in range(left, right):                            # 1 + 1 + 
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
        right -= 1
    
        for i in range(right, left, -1):
            if array[i - 1] > array[i]:
                array[i], array[i - 1] = array[i - 1], array[i]
        left += 1
    return array

```

## Shell sort

```python
def shell_sort(data):
    n = len(data)                                               # 3
    step = n // 2                                               # 3
    while step > 0:                                             # 1 + sqrt(n)*(2 + 1 + 
        for i in range(step, n):                                # 1 + 1 + (n - 1 + n / 2) / 2 * (2 + 1  + 
            j = i                                               # 1
            while j >= step and data[j - step] > data[j]:       # 1 + 2 + 2 + 1 + 1 + x
                data[j-step], data[j] = data[j], data[j-step]
                j -= step
        step //= 2
    return data
```

## Choice sort 

```python
def choice_sort(array):
    n = len(array)
    for i in range(n - 1):
        min_i = i
        for j in range(i + 1, n):
            if array[j] < array[min_i]:
                min_i = j
        array[i], array[min_i] = array[min_i], array[i]
    return array
```