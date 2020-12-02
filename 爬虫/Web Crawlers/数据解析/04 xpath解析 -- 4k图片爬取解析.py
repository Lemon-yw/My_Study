"""
Case: 解析下载图片数据
Author: yangwen
Time: 2020/12/2 2:28 下午
"""
import requests
import os
from lxml import etree

if __name__ == '__main__':
    # 创建一个文件夹用来保存爬取的所有图片
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')

    url = 'http://pic.netbian.com/4kfengjing/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    page_text = requests.get(url=url, headers=headers).text

    # 数据解析：src属性值、alt属性值
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="slist"]//li')
    for li in li_list:
        img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0]
        img_name = li.xpath('./a/img/@alt')[0] + '.jpg'
        # 通用处理中文乱码的解决方案
        img_name = img_name.encode('iso-8859-1').decode('gbk')
        # 请求图片url进行持久化存储
        img_data = requests.get(url=img_src, headers=headers).content
        # 图片存储路径
        img_path = './picLibs/' + img_name

        with open(img_path, 'wb') as fp:
            fp.write(img_data)
            print(img_name, '下载成功！！！')
