"""
快速排序
"""


def quick_sort(start_index, end_index, array):
    # 递归的结束条件
    if start_index >= end_index:
        return
    # 得到基准元素的位置
    pivot_index = partition_v1(start_index, end_index, array)
    # 根据基准元素位置，分成两部分进行排序
    quick_sort(start_index, pivot_index-1, array)
    quick_sort(pivot_index+1, end_index, array)


def partition_v1(start_index, end_index, array):
    # 取第一个元素作为基准元素
    pivot = array[start_index]
    left = start_index
    right = end_index

    while left != right:
        # 控制right指针比较并左移
        while left < right and array[right] > pivot:
            right -= 1
        # 控制left指针比较并右移(注意等号)
        while left < right and array[left] <= pivot:
            left += 1
        # 交换left和right指向的元素
        if left < right:
            array[left], array[right] = array[right], array[left]
    # pivot和指针重合点交换(注意不能直接用pivot的值进行交换，改变pivot的值没有意义)
    array[start_index], array[left] = array[left], array[start_index]
    return left


if __name__ == '__main__':
    my_array = list([3, 4, 14, 1, 5, 6, 7, 8, 1, -1, 0, 9, 11])
    quick_sort(0, len(my_array) - 1, my_array)
    print(my_array)