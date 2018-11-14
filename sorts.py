from itertools import islice
from operator import itemgetter
from heapq import merge
from math import log2
from random import shuffle


SORT_ELEMENTS_BIAS = 7


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
        if hi - lo <= SORT_ELEMENTS_BIAS:
            temp = array[lo:hi]
            insertion_sort(temp)
            array[lo:hi] = temp
            return

        mid = lo + (hi - lo) // 2
        sort(lo, mid)
        sort(mid, hi)
        if array[mid - 1] <= array[mid]:
            return
        merge_iter = merge(islice(iter(array), lo, mid),
                           islice(iter(array), mid, hi))
        # The following assignment is safe when array is a list:
        # https://stackoverflow.com/questions/53286531/assign-iterators-to-a-python-slice
        array[lo:hi] = merge_iter if isinstance(array, list) else list(merge_iter)

    sort(0, len(array))


def merge_sort_non_recursive(array):
    if not array:
        return
    for sz in (2 ** p for p in
               range(0,
                     int(log2(len(array))) + 1
                     )
               ):
        for lo in range(0, len(array) - sz, 2 * sz):
            mid = lo + sz
            hi = lo + 2 * sz
            merge_iter = merge(islice(iter(array), lo, mid),
                               islice(iter(array), mid, hi))
            # The following assignment is safe when array is a list:
            # https://stackoverflow.com/questions/53286531/assign-iterators-to-a-python-slice
            array[lo:hi] = merge_iter if isinstance(array, list) else list(merge_iter)


def quick_sort(array):
    shuffle(array)

    def partition(lo, hi):
        while True:
            i = lo + 1
            for i in range(i, hi):
                if array[i] > array[lo]:
                    break

            j = hi - 1
            for j in range(j, lo - 1, -1):
                if array[j] <= array[lo]:  # Stop on equal keys
                    break

            if i >= j:
                break
            array[i], array[j] = array[j], array[i]

        array[lo], array[j] = array[j], array[lo]
        return j

    def sort(lo, hi):
        if hi - lo < 2:
            return
        if hi - lo <= SORT_ELEMENTS_BIAS:
            temp = array[lo:hi]
            insertion_sort(temp)
            array[lo:hi] = temp
            return

        j = partition(lo, hi)
        sort(lo, j)
        sort(j + 1, hi)

    sort(0, len(array))


def quick_sort_3_way(array):
    shuffle(array)

    def sort(lo, hi):
        if hi - lo < 2:
            return
        if hi - lo <= SORT_ELEMENTS_BIAS:
            temp = array[lo:hi]
            insertion_sort(temp)
            array[lo:hi] = temp
            return

        lt, i, gt = lo, lo, hi - 1
        v = array[lo]
        while i <= gt:
            if array[i] < v:
                array[lt], array[i] = array[i], array[lt]
                i += 1
                lt += 1
            elif array[i] > v:
                array[gt], array[i] = array[i], array[gt]
                gt -= 1
            else:
                i += 1

        sort(lo, lt)
        sort(gt + 1, hi)

    sort(0, len(array))


def heap_sort(array):

    class PriorityQueue:  # Just for demo, use heapq instead

        def __init__(self, capacity, ascending=True):
            self._heap = [None] * (capacity + 1)
            self._n = 0
            self._ascending = ascending

        def insert(self, value):
            self._n += 1
            self._heap[self._n] = value
            self._swim(self._n)

        def pop(self):
            value = self._heap[1]
            self._exch(1, self._n)
            self._heap[self._n] = None
            self._n -= 1
            self._sink(1)
            return value

        def consume(self):
            while self._n > 0:
                yield self.pop()

        def empty(self):
            return self._n == 0

        def _swim(self, k):
            while k > 1 and self._less(k // 2, k):
                self._exch(k, k // 2)
                k //= 2

        def _sink(self, k):
            while 2 * k <= self._n:
                j = 2 * k
                if j < self._n and self._less(j, j + 1):
                    j += 1
                if not self._less(k, j):
                    break
                self._exch(k, j)
                k = j

        def _less(self, i, j):
            if self._ascending:
                return self._heap[i] >= self._heap[j]
            else:
                return self._heap[i] < self._heap[j]

        def _exch(self, i, j):
            self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    queue = PriorityQueue(len(array))
    for value in array:
        queue.insert(value)
    array[:] = queue.consume()
