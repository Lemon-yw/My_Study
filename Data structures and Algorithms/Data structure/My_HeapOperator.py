"""
最小堆代码示例：
    二叉堆的节点上浮、下沉操作
    二叉堆的构建

二叉堆的所有节点存储在数组中
    父节点下标：parent
    左孩子下标：parent*2+1，右孩子下标：parent*2+2
"""


def up_adjust(array):
    """
    二叉树的尾节点上浮操作
    :param array:原数组
    """
    # 尾节点的索引值(左/右孩子下标)
    child_index = len(array) - 1
    parent_index = (child_index - 1) // 2
    # temp保存插入的叶子节点值，用于最后的赋值
    temp = array[child_index]
    # 如果有尾节点，并且尾节点的值小于其父节点值，则进行循环的上浮操作
    while child_index > 0 and temp < array[parent_index]:
        # 无需真正的交换，单向赋值即可
        array[child_index] = array[parent_index]
        child_index = parent_index
        parent_index = (child_index - 1) // 2
    array[child_index] = temp


def down_adjust(parent_index, array):
    """
    二叉堆的节点下沉操作
    :param parent_index: 待下沉的节点下标
    :param array: 原数组
    """
    length = len(array)
    # 待下沉节点(父节点)的左孩子节点
    child_index = parent_index * 2 + 1
    # temp保存待下沉节点的值，用于最后的赋值
    temp = array[parent_index]
    # 如果待下沉节点有左孩子节点，并且待下沉节点值大于其左孩子节点的值，则进行循环的下沉操作
    while child_index < length and temp > array[child_index]:
        # 如果有右孩子，且右孩子小于左孩子值，则定位到右孩子
        if child_index + 1 < length and array[child_index + 1] < array[child_index]:
            child_index += 1
        # 无需真正的交换，单向赋值即可
        array[parent_index] = array[child_index]
        parent_index = child_index
        child_index = parent_index * 2 + 1
    array[parent_index] = temp


def build_heap(array):
    """
    二叉堆的构建操作
    :param array: 原数组
    """
    # 从最后一个非叶子节点开始，依次下沉调整
    for i in range((len(array) - 2) // 2, -1, -1):
        down_adjust(i, array)


if __name__ == '__main__':
    my_array = list([1, 3, 2, 6, 5, 7, 8, 9, 10, 0])
    up_adjust(my_array)
    print("up_adjust:\n", my_array)

    my_array2 = list([7, 1, 3, 10, 5, 2, 8, 9, 6])
    build_heap(my_array2)
    print("build_heap:\n", my_array2)
