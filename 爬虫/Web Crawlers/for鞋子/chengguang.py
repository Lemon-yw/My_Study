"""
Case: 爬取全部榜单，字段：名字、作者、字数、标签、鲜花、人气、评论数
Author: yangwen
Time: 2020/11/30 9:13 下午
"""
import requests

if __name__ == '__main__':
    url = 'https://www.66rpg.com/list/ranking?rank=2&tag=&day=40&page=1&query_peak_date=&sel_state=0&type=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    for page in range(1, 15):
        page = str(page)
        param = {
            'rank': '2',
            'tag': '',
            'day': '40',
            'page': page,
            'query_peak_date': '',
            'sel_state': '0',
            'type': '2',
        }

        page_text = requests.get(url=url, params=param, headers=headers).text
        fileName = 'chengguang/' + page + '.html'
        with open(fileName, 'w', encoding='utf-8') as fp:
            fp.write(page_text)

    print('Finish！！！')
