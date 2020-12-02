"""
Case: 爬取58二手房中的房源信息
Author: yangwen
Time: 2020/12/1 10:43 下午
"""
import requests
from lxml import etree

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    # 爬取页面源码数据
    url = 'https://bj.58.com/ershoufang/'
    page_text = requests.get(url=url, headers=headers).text

    # 数据解析
    tree = etree.HTML(page_text)
    # 存储li标签的对象
    li_list = tree.xpath('//ul[@class="house-list-wrap"]/li')

    with open('./58.txt', 'w', encoding='utf-8') as fp:
        for li in li_list:
            # 局部解析
            title = li.xpath('./div[2]//a/text()')[0]
            fp.write(title + '\n')
            print(title)
