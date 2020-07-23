"""
求字符串中的子串
"""


def count_str(input_str):
    result = []
    length = len(input_str)
    for j in range(length):
        for i in range(length - j):
            result.append(input_str[i: i + j + 1])
    return result


"""
反转字符串
"""


def reverse_str(input_str):
    # 方法1
    # result = input_str[::-1]

    # 方法2
    # l = list(input_str)
    # l.reverse()
    # result = "".join(l)

    # 方法3
    input_str = list(input_str)
    i = 0
    j = len(input_str) - 1
    while i < j:
        input_str[i], input_str[j] = input_str[j], input_str[i]
        i += 1
        j -= 1
    result = "".join(input_str)
    return result


"""
无重复字符的最长子串
"""


def lengthOfLongestSubstring(input_str):
    if not input_str:
        return 0

    n = len(input_str)
    lookup = []
    cur_len = 0
    max_len = 0

    for i in range(n):
        val = input_str[i]
        if val not in lookup:
            lookup.append(val)
            cur_len += 1
        else:
            cur_index = lookup.index(val)
            lookup = lookup[cur_index + 1:]
            lookup.append(val)
            cur_len = len(lookup)

        if cur_len > max_len:
            max_len = cur_len

    return max_len


"""
合并有序数组

循环比较两个有序数组头位元素的大小，并把较小的元素放到新数组中，从老数组中删掉,
直到其中一个数组长度为0。然后再把不为空的老数组中剩下的部分加到新数组的结尾。
"""


def merge_sort(a, b):
    result = []
    while len(a) > 0 and len(b) > 0:
        if a[0] <= b[0]:
            result.append(a[0])
            a.remove(a[0])
        if b[0] <= a[0]:
            result.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        result += b
    if len(b) == 0:
        result += a
    return result


if __name__ == '__main__':
    # print("字符串中的子串:", count_str('abc'))

    a = [1, 3, 4, 6, 7, 78, 97, 190]
    b = [2, 5, 6, 8, 10, 12, 14, 16, 18]
    # print("合并后的有序数组:", merge_sort(a, b))
    # print("反转后的字符串:", reverse_str("abcdef"))
    print("无重复字符的最长子串长度:", lengthOfLongestSubstring("pwwkew"))
