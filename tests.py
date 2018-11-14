import unittest
import random
from timeit import default_timer as timer

from sorts import selection_sort, insertion_sort, shell_sort, merge_sort


N = 1000
MAX_2_POWER = 4
BUILD_PLOTS = False


def _function_is_empty(func):
    empty_function_code = b'd\x00\x00S'
    return func.__code__.co_code == empty_function_code


def build_test_case(sorter):

    class SortTestCase(unittest.TestCase):

        @staticmethod
        def sort(array):
            sorter(array)
            return array

        def check_complexity(self, scaled):
            pass

        def test_empty(self):
            self._perform_test([])

        def test_one(self):
            self._perform_test([1])

        def test_2_ordered(self):
            self._perform_test([1, 2])

        def test_2_unordered(self):
            self._perform_test([2, 1])

        def test_3_ordered(self):
            self._perform_test([1, 2, 3])

        def test_3_unordered(self):
            self._perform_test([1, 3, 2])

        def test_the_same(self):
            self._perform_test([1, 2, 2, 3, 2, 4, 6])

        def test_arbitrary(self):
            self._perform_test([10, -4, 0, 0.3, -13.3, 5, -4, 10, 22, -4, 5])

        def test_reversed(self):
            self._perform_test(list(range(100, 0, -1)))

        def test_random(self):
            self._perform_test(self._build_random_array())

        def test_complexity(self):
            if _function_is_empty(self.check_complexity) and not BUILD_PLOTS:
                return

            random.seed()
            times_reversed = []
            times_random = []
            for n in (2**p * N for p in range(MAX_2_POWER + 1)):
                array_reversed = list(range(n, 0, -1))
                array_random = self._build_random_array()
                times_reversed.append(self._timeit(array_reversed))
                times_random.append(self._timeit(array_random))

            scaled_reversed = [t / times_reversed[0] for t in times_reversed]
            scaled_random = [t / times_random[0] for t in times_random]

            if BUILD_PLOTS:
                import matplotlib.pyplot as plt
                plt.plot(scaled_reversed, label='reversed')
                plt.plot(scaled_random, label='random')
                plt.legend()
                plt.show()

            self.check_complexity(scaled_reversed)
            self.check_complexity(scaled_random)

        def _perform_test(self, array):
            array_sorted = self.sort(list(array))
            assert array_sorted is not array
            self.assertEqual(sorted(array), array_sorted)

        def _timeit(self, array):
            start = timer()
            self.sort(array)
            end = timer()
            return end - start

        @staticmethod
        def _build_random_array():
            array = list(range(N))
            random.shuffle(array)
            return array

    new_cls_name = '{}TestCase'.format(''.join(p.capitalize() for p in sorter.__name__.split('_')))
    SortTestCase.__qualname__ = SortTestCase.__qualname__.replace(SortTestCase.__name__, new_cls_name)
    SortTestCase.__name__ = new_cls_name
    return SortTestCase


if __name__ == '__main__':
    random.seed()

    sorters = (selection_sort, insertion_sort, shell_sort, merge_sort)

    suites = []
    for sorter in sorters:
        suites.append(unittest.TestLoader().loadTestsFromTestCase(build_test_case(sorter)))

    all_tests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
