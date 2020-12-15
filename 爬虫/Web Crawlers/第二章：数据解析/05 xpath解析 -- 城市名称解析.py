"""
Case: 解析出所有城市名称
Author: yangwen
Time: 2020/12/2 8:08 下午
"""
import requests
from lxml import etree

if __name__ == '__main__':
    url = 'https://www.aqistudy.cn/historydata/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    page_text = requests.get(url=url, headers=headers).text

    tree = etree.HTML(page_text)
    # 解析到热门城市和所有城市对应的a标签
    # //div[@class="bottom"]/ul/li/          热门城市a标签的层级关系
    # //div[@class="bottom"]/ul/div[2]/li/a  全部城市a标签的层级关系
    a_list = tree.xpath('//div[@class="bottom"]/ul/li/a | //div[@class="bottom"]/ul/div[2]/li/a')
    print('a_list:', a_list)
    all_city_names = []
    for a in a_list:
        city_name = a.xpath('./text()')[0]
        all_city_names.append(city_name)
    print(all_city_names, len(all_city_names))
