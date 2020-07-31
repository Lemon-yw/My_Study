"""
1. 排序
    冒泡、快排
2. 二叉树
    深度、广度遍历
3. 链表
    反转链表
    判断成环、相交
4. 字符串
    最长公共前缀
    求字符串中的子串
    反转字符串
    无重复字符的最长子串
5. 数组
    合并有序数组
    最大子序和
6. 递归
    爬楼梯
7. 栈/字典
    有效括号
"""
from queue import Queue


# 1.1
def bubble_sort(array):
    length = len(array)

    for i in range(length-1):
        is_sorted = True
        for j in range(length-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                is_sorted = False
        if is_sorted:
                break


# array = [4, 5, 2, 9, 2, 5, 1, 3, 7]
# bubble_sort(array)
# print(array)


# 1.2
def quick_sort(array, start_index, end_index):
    if start_index > end_index:
        return

    pivot_index = partition(array, start_index, end_index)

    quick_sort(array, start_index, pivot_index-1)
    quick_sort(array, pivot_index+1, end_index)


def partition(array, start_index, end_index):
    pivot = array[start_index]
    left = start_index
    right = end_index

    while left < right:
        while left < right and array[right] > pivot:
            right -= 1
        while left < right and array[left] <= pivot:
            left += 1
        if left < right:
            array[left], array[right] = array[right], array[left]
    array[start_index], array[left] = array[left], array[start_index]

    return left

# array = [4, 5, 2, 9, 2, 5, 1, 3, 7]
# quick_sort(array, 0, len(array)-1)
# print(array)


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


# 2.1
def pre_order_traveral(node):
    if not node:
        return

    print(node.data, end=' ')
    pre_order_traveral(node.left)
    pre_order_traveral(node.right)


def pre_order_traveral_stack(node):
    stack = []
    while node and len(stack) > 0:
        while node:
            print(node.data, end=' ')
            stack.append(node)
            node = node.left
        if len(stack) > 0:
            node = stack.pop()
            node = node.right


# 2.2
def level_order_traveral(node):
    queue = Queue()
    queue.put(node)

    while not queue.empty():
        node = queue.get()
        print(node.data)
        if node.left:
            queue.put(node.left)
        if node.right:
            queue.get(node.right)


# 5.1
def merge_sort(a, b):
    result = []

    while len(a) > 0 and len(b) > 0:
        if a[0] <= b[0]:
            result.append(a[0])
            a.remove(a[0])
        if b[0] < a[0]:
            result.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        result += b
    if len(b) == 0:
        result += a
    return result


# a = [1, 3, 4, 6, 7, 78, 97, 190]
# b = [2, 5, 6, 8, 10, 12, 14, 16, 18]
# print(merge_sort(a, b))


# 4.2
def count_str(input_str):
    result = []
    length = len(input_str)

    for i in range(length):
        for j in range(length - i):
            result.append(input_str[j:i + j + 1])
    return result


# input_str = 'abc'
# print(count_str(input_str))
