# -*- coding: utf-8 -*-

"""
github第二种登录方式
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7
"""

import requests
from lxml import etree


class Login(object):

    def __init__(self, email, password):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'https://github.com/',
            'Host': 'github.com'
        }

        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.session = requests.Session()

        self.email = email
        self.password = password

    # 模拟登录
    def login_GitHub(self):

        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.get_token(),
            'login': self.email,
            'password': self.password
        }

        response = self.session.post(self.post_url, data=post_data, headers=self.headers)

        print(response.status_code)
        print(post_data)

        if response.status_code == 200:
            print("登录成功！")
        else:
            print("登录失败！")

    # 获取token信息
    def get_token(self):

        response = self.session.get(self.login_url, headers=self.headers)

        html = etree.HTML(response.content.decode())

        token = html.xpath('//input[@name="authenticity_token"]/@value')[0]

        return token


if __name__ == '__main__':
    email = input('请输入您的账号： ')
    password = input('请输入您的密码： ')

    login = Login(email, password)
    login.login_GitHub()
