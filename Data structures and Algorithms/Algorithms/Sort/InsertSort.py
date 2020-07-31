"""
插入排序
"""


def insert_sort(array):
    for i in range(1, len(array)):
        pre_index = i-1
        current = array[i]
        while pre_index >= 0 and array[pre_index] > current:
            array[pre_index+1] = array[pre_index]
            pre_index -= 1
        array[pre_index+1] = current


if __name__ == '__main__':
    my_array = list([3, 4, 14, 1, 5, 6, 7, 8, 1, -1, 0, 9, 11])
    insert_sort(my_array)
    print(my_array)