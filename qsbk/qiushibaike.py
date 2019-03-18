#!/usr/bin/env python3.6
# coding=utf-8
import requests
from lxml import etree
import os
import sys

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-9
"""
page_init = "https://www.qiushibaike.com/text/"
joke_init = "https://www.qiushibaike.com/article/"
SAVE_PATH = os.path.join(os.getcwd(), 'jokes/')


class Spider(object):
    def __init__(self, page_num):
        self.page_num = int(page_num)
        # 第一页特殊处理
        self.page_urls = ["https://www.qiushibaike.com/text/"]
        # page_url -> joke_url
        self.joke_urls = []
        # joke_url -> joke_name joke_content
        # dict name : content
        self.joke_content = ""
        self.joke_id = 1;
        try:
            os.mkdir(SAVE_PATH)
        except Exception as e:
            print(e)

    def get_page_urls(self):
        if self.page_num > 1:
            # 通过遍历获取到链接
            for n in range(2, self.page_num + 1):
                page_url = page_init + 'page/' + str(n) + '/'
                self.page_urls.append(page_url)

    def get_joke_urls(self):
        for page_url in self.page_urls:
            html = requests.get(page_url).content
            selector = etree.HTML(html)
            qiushi_id = selector.xpath('/html/body/div[@id="content"]/div/div[@id="content-left"]/div/@id')
            for q_id in qiushi_id:
                id = q_id.split('_')[2]
                joke_url = joke_init + id + '/'
                print(joke_url)
                self.joke_urls.append(joke_url)

    def get_joke(self):
        for joke_url in self.joke_urls:
            html = requests.get(joke_url).content
            selector = etree.HTML(html)
            one_joke = selector.xpath('//div[@class="word"]/div/text()')
            self.joke_content = ""
            for words in one_joke:
                self.joke_content += words + '\n'
            self.download()

    def download(self):
        joke_path = SAVE_PATH + str(self.joke_id) + '.txt'
        self.joke_id += 1
        # 笑话路径
        print(joke_path)
        with open(joke_path, "w") as f:
            f.write(self.joke_content)

    def start(self):
        # 获取主页url
        self.get_page_urls()
        # 获取笑话链接
        self.get_joke_urls()
        # 获取笑话
        self.get_joke()
        # 调用下载接口
        self.download()


if __name__ == '__main__':
    # 获取账号
    page_num = input('请告诉我：你想获取多少页的糗事？')

    qb = Spider(page_num)
    # 启动爬虫程序
    qb.start()
