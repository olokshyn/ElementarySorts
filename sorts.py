import itertools
import operator


def selection_sort(array):
    for i in range(len(array) - 1):
        min_index, _ = min(itertools.islice(enumerate(array), i, None),
                           key=operator.itemgetter(1),
                           default=(0, 0))
        array[i], array[min_index] = array[min_index], array[i]


def insertion_sort(array, h=1):
    for i in range(h, len(array)):
        for j in range(i - h, -1, -h):
            if array[j] <= array[j + h]:
                break
            array[j], array[j + h] = array[j + h], array[j]


def shell_sort(array):
    h = 1
    while h < len(array) // 3:
        h = 3 * h + 1

    while h >= 1:
        insertion_sort(array, h)
        h //= 3
