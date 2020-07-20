"""
链表的增、删、改、查
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class MyLinkList:
    def __init__(self):
        # 节点数量
        self.size = 0
        self.head = None
        self.last = None

    # 判断索引是否越界
    def judge(self, index):
        if index < 0 or index > self.size:
            raise Exception("超出链表节点范围！")

    # 获取节点
    def get(self, index):
        self.judge(index)

        p = self.head
        for i in range(index):
            p = p.next
        return p

    # 插入节点
    def insert(self, index, data):
        self.judge(index)

        node = Node(data)
        # 空链表
        if self.size == 0:
            self.head = node
            self.last = node
        # 插入头部
        elif index == 0:
            node.next = self.head
            self.head = node
        # 插入尾部
        elif index == self.size:
            self.last.next = node
            self.last = node
        # 插入中间
        else:
            pre_node = self.get(index - 1)
            node.next = pre_node.next
            pre_node.next = node
        self.size += 1

    # 删除节点
    def remove(self, index):
        self.judge(index)

        # 暂存被删除的节点，用于返回
        # 删除头节点
        if index == 0:
            rm_node = self.head
            self.head = self.head.next
        # 删除尾节点
        elif index == self.size:
            pre_node = self.get(index - 1)
            rm_node = pre_node.next
            pre_node.next = None
            self.last = pre_node
        # 删除中间节点
        else:
            pre_node = self.get(index - 1)
            rm_node = pre_node.next
            pre_node.next = pre_node.next.next
        self.size -= 1
        return rm_node

    # 打印节点值
    def output(self):
        p = self.head
        while p:
            print(p.data)
            p = p.next


if __name__ == '__main__':
    linkedList = MyLinkList()

    linkedList.insert(0, 3)  # 3
    linkedList.insert(0, 4)  # 4 3
    linkedList.insert(2, 9)  # 4 3 9
    linkedList.insert(3, 5)  # 4 3 9 5
    linkedList.insert(1, 6)  # 4 6 3 9 5
    linkedList.remove(0)     # 6 3 9 5

    linkedList.output()
