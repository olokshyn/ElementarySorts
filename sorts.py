import itertools
import operator


def selection_sort(array):
    if len(array) < 2:  # Not required, just for optimization
        return
    for i in range(len(array) - 1):
        min_index, _ = min(itertools.islice(enumerate(array), i, None),
                           key=operator.itemgetter(1),
                           default=(0, 0))
        array[i], array[min_index] = array[min_index], array[i]