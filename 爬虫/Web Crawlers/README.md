## 爬虫模板

```python
import requests
import os
from lxml import etree

if __name__ == '__main__':
    url = 'https://www.aqistudy.cn/historydata/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.198 Safari/537.36 '
    }
    
    # 获取url页面数据
    page_text = requests.get(url=url, headers=headers).text
    
    # 使用xpath进行数据解析
    tree = etree.HTML(page_text)
```