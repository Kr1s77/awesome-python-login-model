#!/usr/bin/env python
# encoding: utf-8

import requests
from lxml import etree
try:
    import cookielib
except:
    import http.cookiejar as cookielib


class GithubLogin(object):

    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url ='https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'

        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')

    def load_cookie(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print('cookie 不成功')

    def get_param(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        field_one = selector.xpath('//div/input[2]/@value')
        print(field_one)
        return field_one
        pass


    def post_param(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.get_param()[0],
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        self.session.cookies.save()

        pass


    def bool_login(self):
        self.load_cookie()
        response = self.session.get(self.logined_url, headers=self.headers)
        selector = etree.HTML(response.text)
        flag = selector.xpath('//div[@class="column two-thirds"]/dl/dt/label/text()')
        print(u'个人设置Profile包括: %s'%flag)
        pass

if __name__ == "__main__":
    Github = GithubLogin()
    Github.post_param(email='******', password='******')
    # Github.bool_login()