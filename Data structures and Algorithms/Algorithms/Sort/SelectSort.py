"""
选择排序
"""


def select_sort(array):
    length = len(array)

    for i in range(length-1):
        # 记录最小数的索引
        min_index = i
        for j in range(i+1, length):
            if array[j] < array[min_index]:
                min_index = j
        # i 不是最小数时，将 i 和最小数进行交换
        if i != min_index:
            array[i], array[min_index] = array[min_index], array[i]


if __name__ == '__main__':
    my_array = list([3, 4, 14, 1, 5, 6, 7, 8, 1, -1, 0, 9, 11])
    select_sort(my_array)
    print(my_array)
