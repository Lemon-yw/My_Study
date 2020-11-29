"""
Case: 爬取豆瓣电影分类排行榜 https://movie.douban.com/中的电影详情数据
Author: yangwen
Time: 2020/11/29 10:59 下午
"""
import requests
import json

if __name__ == '__main__':
    url = 'https://movie.douban.com/j/chart/top_list'
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action': '',
        'start': '0',  # 从库中的第几部电影来取
        'limit': '20',  # 一次请求取出的个数
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }

    response = requests.get(url=url, params=param, headers=headers)
    list_data = response.json()
    with open('douban.json', 'w', encoding='utf-8') as fp:
        json.dump(list_data, fp=fp, ensure_ascii=False)
    print('爬取数据结束！！！')
