from itertools import islice
from operator import itemgetter
from heapq import merge


MERGE_SORT_MIN_BIAS = 7


def selection_sort(array):
    for i in range(len(array) - 1):
        min_index, _ = min(islice(enumerate(array), i, None),
                           key=itemgetter(1),
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


def merge_sort(array):

    def sort(lo, hi):
        if lo >= hi - 1:
            return
        if hi - lo <= MERGE_SORT_MIN_BIAS:
            temp = array[lo:hi]
            insertion_sort(temp)
            array[lo:hi] = temp
            return

        mid = lo + (hi - lo) // 2
        sort(lo, mid)
        sort(mid, hi)
        if array[mid - 1] <= array[mid]:
            return
        array[lo:hi] = merge(islice(iter(array), lo, mid),
                             islice(iter(array), mid, hi))

    sort(0, len(array))
