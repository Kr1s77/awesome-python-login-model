#!/usr/bin/env python3
# coding: utf-8
# v2ex.py


'''
Required
- requests
- lxml
'''


import requests
from io import StringIO
from lxml import etree


class V2EX:
    login_url = 'https://www.v2ex.com/signin'


    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

        session = requests.Session()
        session.headers = {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"
                }
        self.session = session


    def get_login_parameters(self):
        response = self.session.get(self.login_url)

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(response.text), parser)
        elements = tree.xpath('//form[@method="post" and @action="/signin"]/table[@cellpadding="5" and @cellspacing="0" and @border="0" and @width="100%"]//tr[position()<last()]/td[2]/input')
        user_name_key = elements[0].xpath('@name')[0]
        password_key = elements[1].xpath('@name')[0]
        once = elements[2].xpath('@value')[0]
        return user_name_key, password_key, once


    def login(self, user_name_key, password_key, once):
        # 必须带上 referer
        self.session.headers.update({'referer': self.login_url})
        d = {
                user_name_key: self.user_name,
                password_key: self.password,
                'once': once,
                'next': '/'
                }
        response = self.session.post(self.login_url, d)
        flag = False
        if "条未读提醒" in response.text:
            flag = True
        return flag


    def test_login(self):
        user_name_key, password_key, once = self.get_login_parameters()
        return self.login(user_name_key, password_key, once)


if __name__ == '__main__':
    v2ex = V2EX("user_name", "password")
    print("login\t%r" % v2ex.test_login())


