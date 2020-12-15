"""
Case: 爬取搜狗指定词条对应的搜索结果页面（简易网页采集器）
Author: yangwen
Time: 2020/11/29 9:06 下午
"""
# UA：User-Agent（请求载体的身份标识）
# UA检测：门户网站的服务器会监测对应请求的载体身份标识：
# if 检测到身份标识为某一款浏览器: 说明该请求是一个正常请求
# else: 为不正常的请求，服务器端很有可能拒绝该次请求

# UA伪装：让爬虫对应的请求载体身份标识伪装成某一款浏览器

import requests

if __name__ == '__main__':
    # UA伪装：将对应的User-Agent封装到一个字典中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }

    url = 'https://www.sogou.com/web'
    # 处理url携带的参数：封装到字典中
    kw = input('Enter a word: ')
    param = {
        'query': kw
    }
    # 发送带参数的请求，并且请求过程中处理了参数
    response = requests.get(url=url, params=param, headers=headers)

    page_text = response.text
    fileName = kw + '.html'
    with open(fileName, 'w', encoding='utf-8') as fp:
        fp.write(page_text)

    print(fileName, '保存成功！！！')
