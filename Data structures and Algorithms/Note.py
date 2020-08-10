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
滑动窗口框架

def findAnagrams(s, p):
    res = []
    window = {}     # 记录窗口中各个字符数量的字典
    needs = {}      # 记录目标字符串中各个字符数量的字典
    for c in p: needs[c] = needs.get(c, 0) + 1  # 统计目标字符串的信息
    
    length, limit = len(p), len(s)
    left = right = 0                    # 定理两个指针，分别表示窗口的左、右界限
    
    while right < limit:
        c = s[right]                    # c 是将移入窗口的字符
        if c not in needs:              # 当遇到不需要的字符时
            window.clear()              # 将之前统计的信息全部放弃
            left = right = right + 1    # 从下一位置开始重新统计
        else:
            window[c] = window.get(c, 0) + 1            # 统计窗口内各种字符出现的次数
            if right-left+1 == length:                  # 当窗口大小与目标字符串长度一致时
                # 如果窗口内的各字符数量与目标字符串一致就将left添加到结果中
                if window == needs: res.append(left)    
                window[s[left]] -= 1                    # 并将移除的字符数量减一
                left += 1                               # left右移
            right += 1                                  # right右移
    return res
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

