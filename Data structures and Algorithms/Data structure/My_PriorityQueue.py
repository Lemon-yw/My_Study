"""
最大优先队列(最大堆实现)
    入队：二叉堆的节点上浮
    出队：二叉堆的节点下沉
"""


class PriorityQueue:
    def __init__(self):
        self.array = []

    def enqueue(self, element):
        self.array.append(element)
        self.up_adjust(self.array)

    def dequeue(self):
        length = len(self.array)
        if length < 0:
            raise Exception("队列为空 !")
        head = self.array[0]
        self.array[0] = self.array[length-1]
        self.array.pop()
        self.down_adjust(0, self.array)
        return head

    def up_adjust(self, array):
        """
        二叉树的尾节点上浮操作
        :param array:原数组
        """
        # 尾节点的索引值(左/右孩子下标)
        child_index = len(array) - 1
        parent_index = (child_index - 1) // 2
        # temp保存插入的叶子节点值，用于最后的赋值
        temp = array[child_index]
        # 如果有尾节点，并且尾节点的值大于其父节点值，则进行循环的上浮操作
        while child_index > 0 and temp > array[parent_index]:
            # 无需真正的交换，单向赋值即可
            array[child_index] = array[parent_index]
            child_index = parent_index
            parent_index = (child_index - 1) // 2
        self.array[child_index] = temp

    def down_adjust(self, parent_index, array):
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
        # 如果待下沉节点有左孩子节点，则进行循环的下沉操作
        while child_index < length:
            # 如果有右孩子，且右孩子大于左孩子值，则定位到右孩子
            if child_index + 1 < length and array[child_index + 1] > array[child_index]:
                child_index += 1
            # 如果父节点大于任何一个孩子的值，直接跳出
            if temp >= array[child_index]:
                break
            # 无需真正的交换，单向赋值即可
            array[parent_index] = array[child_index]
            parent_index = child_index
            child_index = parent_index * 2 + 1
        array[parent_index] = temp


if __name__ == '__main__':
    queue = PriorityQueue()
    queue.enqueue(3)
    queue.enqueue(5)
    queue.enqueue(10)
    queue.enqueue(2)
    queue.enqueue(7)
    print(queue.dequeue())
    print(queue.dequeue())
