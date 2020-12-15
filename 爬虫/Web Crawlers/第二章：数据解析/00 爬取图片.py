"""
Case: 如何爬取一张图片
Author: yangwen
Time: 2020/11/30 10:21 下午
"""
import requests

if __name__ == '__main__':
    url = 'https://pic.qiushibaike.com/system/pictures/12172/121721100/medium/DNXDX9TZ8SDU6OK2.jpg'

    # content返回的是二进制形式的图片数据
    img_data = requests.get(url=url).content

    with open('./qiutu.jpg', 'wb') as fp: # 'wb'以二进制的形式写入
        fp.write(img_data)

    print('Finish!!!')

