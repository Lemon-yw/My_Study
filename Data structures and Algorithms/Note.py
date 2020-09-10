"""
python 常用 & 易混
"""

"""
列表索引问题

正数索引从0开始，负数索引从-1开始。
nums = [1, 2, 3, 4, 5, 6, 7]
k = 3

print(num[0])   # 7
print(num[-1])  # 7

print(nums[k:])  # [4, 5, 6, 7]
print(nums[:k])  # [1, 2, 3]

print(nums[-k:])  # [5, 6, 7]
print(nums[:-k])  # [1, 2, 3, 4]
"""

"""
字符串转化成列表

a = 'ab,cd,ef'
print(a.split(','))   # ['ab', 'cd', 'ef']

列表转化为字符串

a = ['a', 'b']
print(''.join(a))   # ab
"""
