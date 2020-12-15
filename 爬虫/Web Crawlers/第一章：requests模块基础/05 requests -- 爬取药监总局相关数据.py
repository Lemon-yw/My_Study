"""
Case: 爬取国家药品监督管理总局中基于中华人民共和国化妆品生产许可证相关数据
Author: yangwen
Time: 2020/11/30 12:04 下午
"""
import requests

if __name__ == '__main__':
    url = 'http://scxk.nmpa.gov.cn:81/xk/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
