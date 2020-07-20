"""
循环队列
"""


class MyQueue:
    def __init__(self, capacity):
        self.list = [None] * capacity
        self.front = 0
        self.rear = 0

    def enqueue(self, element):
        if (self.rear+1) % len(self.list) == self.front:
            raise Exception("队列已满 !")
        self.list[self.rear] = element
        self.rear = (self.rear+1) % len(self.list)

    def dequeue(self):
        if self.rear == self.front:
            raise Exception("队列为空 !")
        de_element = self.list[self.rear]
        self.front = (self.front+1) % len(self.list)
        return de_element

    def output(self):
        i = self.front
        while i != self.rear:
            print(self.list[i])
            i = (i+1) % len(self.list)


if __name__ == '__main__':
    myQueue = MyQueue(6)

    myQueue.enqueue(3)  # 3
    myQueue.enqueue(5)  # 3 5
    myQueue.enqueue(6)  # 3 5 6
    myQueue.dequeue()   # 5 6
    myQueue.dequeue()   # 6
    myQueue.enqueue(2)  # 6 2
    myQueue.enqueue(4)  # 6 2 4

    myQueue.output()
