'''
读取大型日志文件，搜索关键字，打印关键字前5行
'''
from collections import deque


# 定义一个搜索关键字的函数
def search_keyword(lines, pattern, history=5):
    """
    搜索关键字的生成器函数
    :param lines: 含有多行内容的可迭代对象
    :param pattern: 要搜索的关键字
    :param history: 保留的含有关键字的条目数
    """
    # 创建只能容纳 5 个元素的队列
    previous_lines = deque(maxlen=history)

    for line in lines:

        # 判断每行是否含有目标关键字
        if pattern in line:
            # 当每次匹配成后就把此行添加到队列中，
            # 并且返回这个队列，以便稍后打印里面的
            # 元素时可以看到其中数量的变化
            previous_lines.append(line)
            yield previous_lines


if __name__ == '__main__':
    with open(r'/Users/didi/Desktop/My_Study/Data structures and Algorithms/log.txt') as f:
        for prevlines in search_keyword(f, 'response', 5):
            for pline in prevlines:
                print(pline, end='')
            print('\n', '-' * 20)