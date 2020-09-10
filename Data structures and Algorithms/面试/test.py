import re

# with open('/Users/didi/Desktop/My_Study/Data structures and Algorithms/log.txt', 'r') as f:
#     alllines = f.readlines()
#
# with open('/Users/didi/Desktop/My_Study/Data structures and Algorithms/log.txt', 'w+') as f:
#     for eachline in alllines:
#         a = re.sub('response', 'hi', eachline)
#         f.writelines(a)

with open('/Users/didi/Desktop/My_Study/Data structures and Algorithms/log.txt', 'r+') as f1:
    with open('/Users/didi/Desktop/My_Study/Data structures and Algorithms/log2.txt', 'w+') as f2:
        str1 = 'response'
        str2 = 'hi'
        for ss in f1.readlines():
            tt = re.sub(str1, str2, ss)
            f2.write(tt)