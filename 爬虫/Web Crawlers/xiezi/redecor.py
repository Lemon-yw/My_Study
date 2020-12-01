"""
Case: 爬取全部的challenge详情
Author: yangwen
Time: 2020/11/30 9:48 下午
"""
import requests
import re

if __name__ == '__main__':
    url = 'https://www.redecor.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }