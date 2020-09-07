"""
笔试输入输出模板 -- python
"""


'''
1. 一行输入

1.1 例：
        输入：5     读取：5
        输入：abed  读取：abed
1.2 例：
        输入：1 2 3 4
        读取：[1, 2, 3, 4]
'''

# 1.1 输入一个数/字符串
s = input()
print(s)

# 1.2 输入一个数组
s = input()
s = [int(i) for i in s.split()]
print(s)

'''
2. 两行输入

例：
    输入：
        4
        2 1 3 4
    输出：
        [2, 1, 3, 4] 
'''

# 第一行输入数组长度，第二行输入数组，那么读入操作分两步，首先获得数组长度，然后获取数组。
while True:
    s = input()
    if s != "":
        nums = [int(i) for i in input().split()]
        print(nums)
        break
    else:
        break
# input()
# nums = [int(i) for i in input().split()]
# print(nums)

'''
3. 多行输入

例：
    输入：
        4
        2 1 3 4
        1 2 3 4
        5 6 7 8
        8 7 4 5
    输出：
        [[2, 1, 3, 4], [1, 2, 3, 4], [5, 6, 7, 8], [8, 7, 4, 5]]
'''

# 第一行输入操作个数，从第二行还是输入n个数组。
data = []
length = int(input())
n = 0
while n < length:
    s = input()
    if s != "":
        temp = [int(i) for i in s.split()]
        data.append(temp)
        n = n + 1
    else:
        break
print(data)

# 参考：https://blog.csdn.net/sinat_35821976/article/details/89509757#1.%20%E4%B8%80%E8%A1%8C%E8%BE%93%E5%85%A5
