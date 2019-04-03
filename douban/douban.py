#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-04-04
"""

"""
模拟登陆豆瓣
"""


class DouBanLogin(object):
    def __init__(self, account, password):
        self.url = "https://accounts.douban.com/j/mobile/login/basic"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        """初始化数据"""
        self.data = {
            "ck": "",
            "name": account,
            "password": password,
            "remember": "true",
            "ticket": ""
        }
        self.session = requests.Session()

    def get_cookie(self):
        """模拟登陆获取cookie"""
        html = self.session.post(
            url=self.url,
            headers=self.headers,
            data=self.data
        ).json()
        if html["status"] == "success":
            print("恭喜你，登陆成功")

    def get_user_data(self):
        """获取用户数据表明登陆成功"""
        # TODO: 这里填写你用户主页的url
        url = "这里填写你用户主页的url"
        # 获取用户信息页面
        html = self.session.get(url).text
        print(html)

    def run(self):
        """运行程序"""
        self.get_cookie()
        self.get_user_data()


if __name__ == '__main__':
    account = input("请输入你的账号:")
    password = input("请输入你的密码:")
    login = DouBanLogin(account, password)
    login.run()
