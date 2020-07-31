"""
归并算法
"""


def merge_sort(array):
    length = len(array)
    if length < 2:
        return array

    middle = length // 2
    left, right = array[0: middle], array[middle:]
    return merge(merge_sort(left), merge_sort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))

    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


if __name__ == '__main__':
    my_array = list([3, 4, 14, 1, 5, 6, 7, 8, 1, -1, 0, 9, 11])
    print(merge_sort(my_array))
