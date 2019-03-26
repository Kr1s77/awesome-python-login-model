#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-6
"""

"""
请求URL分析	https://tieba.baidu.com/f?kw=魔兽世界&ie=utf-8&pn=50
请求方式分析	GET
请求参数分析	pn每页50发生变化，其他参数固定不变
请求头分析	只需要添加User-Agent
"""

# 代码实现流程
# 1. 实现面向对象构建爬虫对象
# 2. 爬虫流程四步骤
# 2.1 获取url列表
# 2.2 发送请求获取响应
# 2.3 从响应中提取数据
# 2.4 保存数据

import requests


class TieBa_Spier():

    def __init__(self, max_pn, kw):
        # 初始化
        self.max_pn = max_pn
        self.kw = kw
        self.base_url = "https://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def get_url_list(self):
        """获取url列表"""
        return [self.base_url.format(self.kw, pn) for pn in range(0, self.max_pn, 50)]

    def get_content(self, url):
        """发送请求获取响应内容"""
        response = requests.get(
            url=url,
            headers=self.headers
        )
        # print(response.text)
        return response.content

    def save_items(self, content, idx):
        """从响应内容中提取数据"""
        with open('{}.html'.format(idx), 'wb') as f:
            f.write(content)
        return None

    def run(self):
        """运行程序"""
        # 获取url_list
        url_list = self.get_url_list()

        for url in url_list:
            # 发送请求获取响应
            content = self.get_content(url)

            # 保存数据
            items = self.save_items(content, url_list.index(url) + 1)

            # 测试
            # print(items)


if __name__ == '__main__':
    spider = TieBa_Spier(200, "英雄联盟")
    spider.run()
