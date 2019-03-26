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


class TieBaSpier():

    def __init__(self):
        # 初始化
        pass

    def get_url_list(self):
        """获取url列表"""
        pass

    def get_content(self):
        """发送请求获取响应内容"""
        pass

    def get_items(self):
        """从响应中提取数据"""
        pass

    def save_items(self):
        """保存数据"""
        pass

    def run(self):
        """运行程序"""
        pass


if __name__ == '__main__':
    spider = TieBaSpier()
    spider.run()
