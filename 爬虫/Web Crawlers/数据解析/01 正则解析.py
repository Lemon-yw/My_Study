"""
Case: 爬取糗事百科中糗图板块下所有的糗图图片
Author: yangwen
Time: 2020/11/30 10:29 下午
"""
import requests
import re

if __name__ == '__main__':
    url = 'https://www.qiushibaike.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }

    # 使用通用爬虫对url对应的一整张页面进行爬取
    page_text = requests.get(url=url, headers=headers).text

    # 使用聚焦爬虫将页面中所有的糗图进行解析/提取
    # 正则解析：提取出来的是()中的 .*?
    ex = '<a class="recmd-left image".*?<img src="(.*?)?imageView.*?</a>'
    # re.S: 单行匹配     re.M: 多行匹配
    img_src_list = re.findall(ex, page_text, re.S)
    print(img_src_list)
