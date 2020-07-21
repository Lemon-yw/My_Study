"""
冒泡排序
"""


def bubble_sort_v1(array):
    length = len(array)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


def bubble_sort_v2(array):
    """
    v1方法的问题：
        当某轮中不再有元素交换，说明已排好序，接下来未进行的轮数就不再需要继续了。
    优化策略：
        进行有序标记
    优化结果：
        减少了元素比较的轮数
    :param array: 原数组
    """
    length = len(array)
    for i in range(length - 1):
        # 有序标记，每一轮初始是True
        is_sorted = True
        for j in range(length - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                # 有元素交换，所以不是有序，标记变为false
                is_sorted = False
        if is_sorted:
            break


def bubble_sort_v3(array):
    """
    v2方法的问题：
        每轮通过交换得到的有序区的长度与排序的轮数是相等的，
        但实际上数列真正的有序区是可能超过这个长度
    优化策略：
        在每一轮排序后，记录下最后一次元素交换的位置，
        该位置即为无序数列的边界，再往后就是有序区了。
    优化结果：
        减少了每轮元素比较的次数
    :param array: 原数组
    """
    length = len(array)
    # 记录最后一次交换的位置
    last_exchange_index = 0
    # 无序数列的边界，每次比较只需要比到这里为止
    sorted_border = length - 1
    for i in range(length - 1):
        # 有序标记，每一轮初始是True
        is_sorted = True
        for j in range(sorted_border):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                # 有元素交换，所以不是有序，标记变为false
                is_sorted = False
                # 把无序数列的边界更新为最后一次交换元素的位置
                last_exchange_index = j
        sorted_border = last_exchange_index
        if is_sorted:
            break


if __name__ == '__main__':
    my_array = list([3, 4, 14, 1, 5, 6, 7, 8, 1, -1, 0, 9, 11])
    bubble_sort_v3(my_array)
    print(my_array)
