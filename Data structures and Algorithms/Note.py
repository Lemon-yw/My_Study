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
读取文件问题
"""
# 按行读取文件
with open('log.txt', 'r') as f:
    for line in f:
        print(line, end='')

# 转换为列表，去掉换行符，去掉行首行尾的空白字符
with open('log.txt', 'r') as f:
    content = [line.strip() for line in f]
    # f.read().splitlines() 可去掉换行符，不可去掉空白字符
    print(content)

# 按行读取文件内容并得到当前行号
'''
文件对象是可迭代的（按行迭代），使用enumerate()即可在迭代的同时，得到数字索引(行号),
enumerate()的默认数字初始值是0，如需指定1为起始，可以设置其第二个参数为1。
'''
with open('log.txt', 'r') as f:
    for number, line in enumerate(f, start=1):
        print(number, line, end='')

'''
读取日志文件，搜索关键字，打印关键字前5行
'''


def search(lines, pattern, history=5):
    previous_lines = []
    for line in lines:
        if len(previous_lines) < history and pattern in line:
            previous_lines.append(line)
    return previous_lines


if __name__ == '__main__':
    with open('log.txt', 'r') as f:
        # 去掉换行符
        f = f.read().splitlines()
        print(search(f, 'response'))

        # 追加
        f.write('\n... and more')
        print(open('log.txt').read())

