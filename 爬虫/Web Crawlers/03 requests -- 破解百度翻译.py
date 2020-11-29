"""
Case: 破解百度翻译
Author: yangwen
Time: 2020/11/29 9:43 下午
"""
import requests
import json

if __name__ == '__main__':
    # 1.指定url
    post_url = 'https://fanyi.baidu.com/sug'
    # 2.进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    # 3.post请求参数处理（同get请求一致）
    word = input('Enter a word: ')
    data = {
        'kw': word
    }
    # 4.请求发送
    response = requests.post(url=post_url, headers=headers, data=data)
    # 5.获取响应数据：json()方法返回的是obj（如果确认响应数据是json类型的，才可以使用json()）
    # 如何确认响应数据类型：抓包查看Content-Type
    dic_data = response.json()

    # 6.持久化存储
    fileName = word + '.json'
    with open(fileName, 'w', encoding='utf-8') as fp:
        # 中文不能使用ascii进行编码，故设为False
        json.dump(dic_data, fp=fp, ensure_ascii=False)
    print('翻译成功！！！')
