

# 列表索引问题

正数索引从0开始，负数索引从-1开始。

```python
nums = [1, 2, 3, 4, 5, 6, 7]
k = 3

print(num[0])   # 7
print(num[-1])  # 7

print(nums[k:])  # [4, 5, 6, 7]
print(nums[:k])  # [1, 2, 3]

print(nums[-k:])  # [5, 6, 7]
print(nums[:-k])  # [1, 2, 3, 4]
```

# 处理字符串的方法

## strip()

* 语法描述：
  * strip() 方法用于移除字符串**头尾指定的字符(默认为空格或换行符)或字符序列**。

* **注意**：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。

* 返回值：返回移除字符串头尾指定的字符生成的新字符串

* 示例

  ```python
  str1 = "0000000123456Awin_Ge3456700000000000"
  print str1.strip('0')		# 123456Awin_Ge34567
  
  str2 = "  Awin_Ge   "            
  print str2.strip()	# Awin_Ge
  
  # 只要头尾包含有指定字符序列中的字符就删除
  str3 = "1234Awin_Ge4321"
  print str3.strip('123')		# 4Awin_Ge4
  ```

##split()

* 语法描述：
  * 通过指定分隔符对字符串进行分割并返回一个列表，默认分隔符为所有空字符，包括空格、换行(\n)、制表符(\t)等

* 返回值：返回分割后的字符串列表

* 示例：

  ```python
  str4 = "This is string example!!!!!!!"
  print str4.split()				# ['This', 'is', 'string', 'example!!!!!!!']
  print str4.split('i',1)		# ['Th', 's is string example!!!!!!!']
  print str4.split('!')			# ['This is string example', '', '', '', '', '', '', '']
  ```

# 读取文件问题

```python
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
```

