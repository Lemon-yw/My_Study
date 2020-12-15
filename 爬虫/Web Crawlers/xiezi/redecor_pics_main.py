"""
Case: 爬取 https://reworks.fi/首页全部的challenge详情 -- 图片
Author: yangwen
Time: 2020/11/30 9:48 下午
"""
import requests
import re
import os
import json

from lxml import etree

if __name__ == '__main__':
    if not os.path.exists('./redecor_pics_main'):
        os.mkdir('./redecor_pics_main')

    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.67 Safari/537.36 '
    }
    # 图片计数
    count = 0

    # # 爬取初始页面challenge详情 #
    # url = 'https://reworks.fi/'
    # # 获取首页数据
    # page_text = requests.get(url=url, headers=headers).text
    # # 使用xpath进行数据解析
    # tree = etree.HTML(page_text)
    # div_list = tree.xpth('//div[@class="columns is-multiline"]/div')
    # for div in div_list:
    #     fig_title = div.xpath('./figure/@title')[0] + '.jpg'
    #     attr_style = div.xpath('./figure/@style')[0]
    #     ex = r'.*?url\("(.*?)"\) .*?cover'
    #     fig_url = re.findall(ex, attr_style, re.S)[0]
    #     try:
    #         fig_data = requests.get(url=fig_url, headers=headers).content
    #     except:
    #         print('图片地址解析错误！！！ Try next...')
    #         continue
    #     fig_path = './redecor_pics_main/' + fig_title
    #
    #     with open(fig_path, 'wb') as fp:
    #         fp.write(fig_data)
    #         count += 1
    #         print('第%d张图片:' % count, fig_title, '下载成功！！！')
    print("----------------首页图片爬取结束----------------")

    # 爬取动态加载图片 #
    # 获取第一个fig_id
    # a_href = div_list[-1].xpath('.//a/@href')[0]
    # fig_id = re.findall(r'\d+', a_href)[0]
    # fig_id = "2007"     # (60th load)
    # episode = 60
    # count += 1050

    fig_id = "2011"
    count += 1068
    # 获取动态加载数据
    try:
        while True:
            post_url = 'https://api.redecor.com/graphql'
            # 请求新图片依赖参数: "after": fig_id (最后一张图片)
            print('fig_id:', fig_id)
            # print('number of pictures:', episode * 18)
            payload = {"operationName": "ALL_CHALLENGES_QUERY",
                       "variables": {"type": "closed", "after": fig_id, "limit": 18},
                       "query": "query ALL_CHALLENGES_QUERY($type: ChallengeState = all, "
                                "$after: ID = null, $limit: Int = 18) "
                                "{\n  listChallenges(type: $type, after: $after, limit: $limit) {\n    id\n    title\n "
                                "dateEnd\n    thumb\n    designs(limit: 1, orderBy: rating) {\n      thumb\n      "
                                "__typename\n    }\n    __typename\n  }\n}\n"}
            fig_json = requests.post(url=post_url, headers=headers, data=json.dumps(payload)).json()
            challenges_list = fig_json['data']['listChallenges']
            # 获取最后一个fig_id， 作为下一次请求的after参数
            fig_id = challenges_list[-1]['id']
            # episode += 1
            # 图片存储
            for challenges in challenges_list:
                if challenges['designs']:
                    new_fig_url = challenges['designs'][0]['thumb']
                else:
                    print('图片地址错误！！！ Try next...')
                    continue
                try:
                    new_fig_data = requests.get(url=new_fig_url, headers=headers).content
                except:
                    print('图片地址解析错误！！！ Try next...')
                    continue
                new_fig_title = challenges['title'] + '.jpg'
                new_fig_path = './redecor_pics_main/' + new_fig_title

                with open(new_fig_path, 'wb') as fp:
                    fp.write(new_fig_data)
                    count += 1
                    print('第%d张图片:' % count, new_fig_title, '下载成功！！！')
            print("----------------Load more Challenges----------------")
    except:
        print("====================Redecor图片爬取结束，共%d张图片====================" % count)
