"""
Case: 
Author: yangwen
Time: 2020/12/9 12:15 下午
"""
# -*- coding: utf-8 -*-

# import re
#
#
# def url_check(url):
#     ex = r'.*?//(.*?).cdn.*?'
#     ex2 = r'.*?com/(.*?)/.*?'
#     if 'thumb3' == re.findall(ex, url, re.S)[0]:
#         return
#     elif 'd' == re.findall(ex2, url, re.S)[0]:
#         return
#     else:
#         return 1
#
#
# # url = 'https://thumb3.cdn.redecor.com/2011/5YUMl18C_800_ZKh_.jpg'
# url = 'https://d.cdn.redecor.com/d/XchjKh_800_mx.jpg'
# if not url_check(url):
#     # 错误地址
#     print('!!!')
# else:
#     print('***')

import tesserocr

print(tesserocr.file_to_text('image.png'))