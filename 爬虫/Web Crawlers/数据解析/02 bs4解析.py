"""
Case: 爬取三国演义小说所有的章节标题和章节内容
Author: yangwen
Time: 2020/12/1 4:55 下午
"""
import requests
import os
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 创建一个文件夹用来保存爬取的所有图片
    if not os.path.exists('./sanguoBook'):
        os.mkdir('./sanguoBook')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    # 对首页的页面数据进行爬取 #
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    page_text = requests.get(url=url, headers=headers).text

    # 在首页中解析出章节的标题和详情页的url #
    # 实例化BeautifulSoup对象，将页面源码数据加载到该对象中
    soup = BeautifulSoup(page_text, 'lxml')
    # 解析章节标题和详情页的url
    li_list = soup.select('.book-mulu > ul > li')
    for li in li_list:
        title = li.a.string
        detail_url = 'https://www.shicimingju.com' + li.a['href']
        # 对详情页发起请求，解析章节内容
        detail_page_text = requests.get(url=detail_url, headers=headers).text
        # 解析出详情页中相关的章节内容
        detail_soup = BeautifulSoup(detail_page_text, 'lxml')
        # 解析章节内容
        # replace(u'\xa0', u' ')消除NBSP
        content = detail_soup.find('div', class_='chapter_content').text.replace(u'\xa0', u'')
        # 章节内容存储路径
        imgPath = './sanguoBook/' + title

        with open(imgPath, 'w', encoding='utf-8') as fp:
            fp.write(title + content + '\n')
            print(title, '爬取成功！！！')


