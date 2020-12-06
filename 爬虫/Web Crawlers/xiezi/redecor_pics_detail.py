"""
Case: 爬取https://www.redecor.com/首页每个challenge的详情 -- 图片
Author: yangwen
Time: 2020/11/30 9:48 下午
"""
import requests
import re
import os
import json

from lxml import etree


def get_home_challenge(fig_id, fig_title):
    # 新建文件夹用于存储每个challenge的图片集
    fig_dir_path = './redecor_pics_detail/%s' % fig_title
    if not os.path.exists(fig_dir_path):
        os.mkdir(fig_dir_path)
    # 记录每个challenge图片集里的图片数量
    count = 0

    # 爬取页面challenge详情 #
    fig_id_url = 'https://www.redecor.com/challenge/' + fig_id
    fig_detail_text = requests.get(url=fig_id_url, headers=headers).text
    detail_tree = etree.HTML(fig_detail_text)
    detail_div_list = detail_tree.xpath('//div[@class="columns is-multiline is-mobile"]/div')
    for detail_div in detail_div_list:
        # 获取每个card的图片
        fig_detail_src = detail_div.xpath('.//img/@src')[0]
        try:
            fig_detail_data = requests.get(url=fig_detail_src, headers=headers).content
        except:
            print('图片地址解析错误！！！ Try next...')
            continue
        # 每个challenge爬取30张图片
        if count >= 30:
            break
        else:
            count += 1
        # 获取每个card的作者名
        fig_detail_author = detail_div.xpath('.//h6/text()')[0] + '.jpg'
        if '/' in fig_detail_author:
            fig_detail_author = fig_detail_author.replace('/', '*')
        elif '\\' in fig_detail_author:
            fig_detail_author = fig_detail_author.replace('\\', '*')
        # 以作者名命名文件并存储
        fig_detail_path = fig_dir_path + '/' + fig_detail_author
        try:
            with open(fig_detail_path, 'wb') as fp:
                fp.write(fig_detail_data)
                print(fig_title, '第%d张图片:' % count, fig_detail_author, '下载成功！！！')
        except:
            count -= 1
            continue
    print('################ %s图片下载完成 ################' % fig_title)


def get_dyna_challenge(last_fig_id):
    retry_fig_id = '0'
    try:
        while True:
            post_url = 'https://api.redecor.com/graphql'
            # 请求新图片依赖参数: "after": fig_id (最后一张图片)
            payload = {"operationName": "ALL_CHALLENGES_QUERY",
                       "variables": {"type": "closed", "after": last_fig_id, "limit": 18},
                       "query": "query ALL_CHALLENGES_QUERY($type: ChallengeState = all, "
                                "$after: ID = null, $limit: Int = 18) "
                                "{\n  listChallenges(type: $type, after: $after, limit: $limit) {\n    id\n    title\n "
                                "dateEnd\n    thumb\n    designs(limit: 1, orderBy: rating) {\n      thumb\n      "
                                "__typename\n    }\n    __typename\n  }\n}\n"}
            fig_json = requests.post(url=post_url, headers=headers, data=json.dumps(payload)).json()
            challenges_list = fig_json['data']['listChallenges']
            # 更新最后一个fig_id
            last_fig_id = challenges_list[-1]['id']
            # 记录第一个fig_id
            detail_fig_id = challenges_list[0]['id']
            # 图片的获取与存储
            for challenges in challenges_list:
                # 记录上一个fig_id:
                retry_fig_id = detail_fig_id
                detail_fig_id = challenges['id']
                print('detail_fig_id:', detail_fig_id)
                detail_fig_title = challenges['title']
                get_home_challenge(detail_fig_id, detail_fig_title)
            print("-----------------------Load more Challenges-----------------------")
    except:
        if retry_fig_id != '0':
            return retry_fig_id
        else:
            return last_fig_id


if __name__ == '__main__':
    if not os.path.exists('./redecor_pics_detail'):
        os.mkdir('./redecor_pics_detail')

    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.67 Safari/537.36 '
    }

    # # 爬取初始页面图片详情 #
    # url = 'https://www.redecor.com/'
    # # 获取首页数据
    # page_text = requests.get(url=url, headers=headers).text
    # # 进行数据解析
    # tree = etree.HTML(page_text)
    # div_list = tree.xpath('//div[@class="columns is-multiline"]/div')
    # for div in div_list:
    #     attr_style = div.xpath('./figure/@style')[0]
    #     ex = r'.*?url\("(.*?)"\) .*?cover'
    #     fig_url = re.findall(ex, attr_style, re.S)[0]
    #     try:
    #         fig_data = requests.get(url=fig_url, headers=headers).content
    #     except:
    #         print('图片地址解析错误！！！ Try next...')
    #         continue
    #     a_href = div.xpath('.//a/@href')[0]
    #     fig_id = re.findall(r'\d+', a_href)[0]
    #     print('fig_id:', fig_id)
    #     fig_title = div.xpath('./figure/@title')[0]
    #     get_home_challenge(fig_id, fig_title)
    print("------------------------首页图片爬取结束------------------------")

    # 爬取动态加载图片 #
    # 获取第一个fig_id
    # a_href = div_list[-1].xpath('.//a/@href')[0]
    # last_fig_id = re.findall(r'\d+', a_href)[0]
    last_fig_id = '2320'

    # final fig_id -- stop
    # fig_id = "2007"     # (60th load)
    # episode = 60
    # count += 1050

    # 获取动态加载数据
    try:
        # while True:
        #     post_url = 'https://api.redecor.com/graphql'
        #     # 请求新图片依赖参数: "after": fig_id (最后一张图片)
        #     payload = {"operationName": "ALL_CHALLENGES_QUERY",
        #                "variables": {"type": "closed", "after": last_fig_id, "limit": 18},
        #                "query": "query ALL_CHALLENGES_QUERY($type: ChallengeState = all, "
        #                         "$after: ID = null, $limit: Int = 18) "
        #                         "{\n  listChallenges(type: $type, after: $after, limit: $limit) {\n    id\n    title\n "
        #                         "dateEnd\n    thumb\n    designs(limit: 1, orderBy: rating) {\n      thumb\n      "
        #                         "__typename\n    }\n    __typename\n  }\n}\n"}
        #     fig_json = requests.post(url=post_url, headers=headers, data=json.dumps(payload)).json()
        #     challenges_list = fig_json['data']['listChallenges']
        #     # 更新最后一个fig_id
        #     last_fig_id = challenges_list[-1]['id']
        #     # print('last_fig_id:', last_fig_id)
        #     # 图片的获取与存储
        #     for challenges in challenges_list:
        #         detail_fig_id = challenges['id']
        #         pre_fig_id = detail_fig_id
        #         print('detail_fig_id:', detail_fig_id)
        #         detail_fig_title = challenges['title']
        #         get_home_challenge(detail_fig_id, detail_fig_title)
        #     print("-----------------------Load more Challenges-----------------------")
        for _ in range(1, 10000):
            last_fig_id = get_dyna_challenge(last_fig_id)
            print('last_fig_id:', last_fig_id)
            print("********************网络异常！！！第%d次尝试重新连接********************" % _)
    except:
        print("========================Redecor图片爬取结束========================")
