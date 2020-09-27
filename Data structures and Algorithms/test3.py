# 先读取文件，将文件中的数据抽取出来：
# 说明：这个有一个要注意的地方是文件是被”\n”,”/”两种格式分割而来的，因此需要split两次。
def getWords(filepath):
    file = open(filepath)
    wordOne = []
    while file:
        line = file.readline()
        wordOne.extend(line.split('/'))
        if not line:  # 若读取结束了
            break
    wordtwo = []
    for i in wordOne:
        wordtwo.extend(i.split())
    return wordtwo


# 然后定义一个dict，遍历数据，代码如下所示：
def getWordNum(words):
    dictWord = {}
    for i in words:
        dictWord[i] = dictWord.get(i, 0) + 1
    # 字典排序
    dictWord_order = sorted(dictWord.items(), key=lambda x: x[1], reverse=True)
    return dictWord_order


if __name__ == '__main__':
    filepath = 'log.txt'
    words = getWords(filepath)
    dictword = getWordNum(words)
    print(dictword)
