"""
数组的插入
"""


class MyArray:
    def __init__(self, capacity):
        self.array = [None] * capacity
        # 数组中元素的个数
        self.size = 0

    def insert(self, index, element):
        # 判断访问下标是否超出范围
        if index < 0 or index > self.size:
            raise Exception("超出数组实际元素范围！")
        # 从右向左循环，到要插入的元素位置为止，逐个元素向右挪一位。
        for i in range(self.size-1, index-1, -1):
            self.array[i+1] = self.array[i]
        # 腾出的位置放入新元素
        self.array[index] = element
        self.size += 1

    def insert_v2(self, index, element):
        # 如果实际元素达到数组容量上线，数组扩容
        if self.size >= len(self.array):
            self.resize()

        self.insert(index, element)

    # 数组扩容
    def resize(self):
        array_new = [None] * len(self.array) * 2
        # 从旧数组拷贝到新数组
        for i in range(self.size):
            array_new[i] = self.array[i]
        self.array = array_new

    def remove(self, index):
        # 判断访问下标是否超出范围
        if index < 0 or index >= self.size:
            raise Exception("超出数组实际元素范围！")
        # 从左到右，从要删除元素的位置开始，逐个元素向左挪动一位
        for i in range(index, self.size - 1):
            temp_size = self.size
            temp_array = self.array
            self.array[i] = self.array[i + 1]
        self.size -= 1
        # 弹出最后一个元素
        self.array.pop()

    # 若数组没有顺序要求(删除元素后可能会打乱数组的顺序，但是时间复杂地为O(1)，非主流方法)
    def remove_v2(self, index):
        self.array[index] = self.array[self.size-1]
        self.array.pop()

    def output(self):
        print(self.array)


if __name__ == '__main__':
    array = MyArray(4)

    # array.insert(0, 10)
    # array.insert(1, 11)
    # array.insert(2, 12)
    # array.insert(3, 13)

    array.insert_v2(0, 10)
    array.insert_v2(1, 11)
    array.insert_v2(2, 12)
    array.insert_v2(3, 13)
    array.insert_v2(4, 14)
    array.insert_v2(2, 15)
    array.insert_v2(2, 16)
    array.insert_v2(2, 17)

    array.output()

    array.remove(0)
    array.output()

    # array.remove_v2(0)
    # array.output()


