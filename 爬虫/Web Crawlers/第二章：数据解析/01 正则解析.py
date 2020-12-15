"""
Case: 爬取糗事百科首页推荐中所有的图片
Author: yangwen
Time: 2020/11/30 10:29 下午
"""
import requests
import re
import os

if __name__ == '__main__':
    # 创建一个文件夹用来保存爬取的所有图片
    if not os.path.exists('./qiutuLibs'):
        os.mkdir('./qiutuLibs')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    # 设置一个通用的url模板
    url = 'https://www.qiushibaike.com/8hr/page/%d/'
    # 爬取每一页的图片
    for pageNum in range(1, 7):
        new_url = format(url % pageNum)

        # 使用通用爬虫对url对应的一整张页面进行爬取
        page_text = requests.get(url=new_url, headers=headers).text

        # 使用聚焦爬虫将页面中所有的糗图进行解析/提取
        # 正则解析：提取出来的是()中的 .*?
        # 包含转义时在最前面加r，表示这些转义只会被解析为正常地转义
        ex = r'<a class="recmd-left multi".*?<img src="(.*?)\?imageView.*?</a>'
        # re.S: 单行匹配     re.M: 多行匹配
        img_src_list = re.findall(ex, page_text, re.S)
        # print(img_src_list)

        for src in img_src_list:
            # 拼接出完整的图片url
            src = 'https:' + src
            # 请求图片的二进制数据
            img_data = requests.get(url=src, headers=headers).content
            # 生成图片名称
            img_name = src.split('/')[-1]
            # 图片存储路径
            imgPath = './qiutuLibs/' + img_name

            with open(imgPath, 'wb') as fp:
                fp.write(img_data)
                print(img_name, '下载成功！！！')
