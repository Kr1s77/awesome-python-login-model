# -*- coding: utf-8 -*-
'''
Required
- requests 
- bs4
'''
# 输入密码不可见模块导入
import getpass
import hashlib
import requests
from bs4 import BeautifulSoup


class Leipin(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'passport.liepin.com',
            'User-Agent': "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            'X-Requested-With': 'XMLHttpRequest',
            'Upgrade-Insecure-Requests': '1',
        }
        self.proxies = {
            'HTTP': 'http://120.198.231.88:80',
            # 'HTTP':'http://222.174.71.46:9999',
        }  # 测试所用代理
        self.session = requests.session()
        self.accountUrl = 'https://passport.liepin.com/h/account'
        self.loginUrl = 'https://passport.liepin.com/h/login.json'
        self.Dir = 'E:\\python\\authcode.jpg'  # authcode folder 根据自己情况选择文件夹

    def _md5(self):
        md5 = hashlib.md5()
        md5.update(str.encode(password))
        psw = md5.hexdigest()
        return psw

    def _getAuthcode(self):
        r = self.session.get(self.accountUrl, headers=self.headers, timeout=10, proxies=self.proxies)
        page = BeautifulSoup(r.text)
        selector = page.find_all('div', class_="ui-tab-toggle hide")[0]
        imageUrl = selector.select('div > img')[0]['src']
        authcodeUrl = 'https://passport.liepin.com{}'.format(imageUrl)
        response = self.session.get(authcodeUrl)
        if response.status_code == 200:
            with open(self.Dir, 'wb') as f:
                f.write(response.content)
        authcode = input('plz input authcode:')
        return authcode

    def login(self):
        payload = {
            'user_login': self.username,
            'isMd5': 1,
            'user_pwd': self._md5(),
            'user_kind': 2,  # 根据你是否为正式会员而定，根据自身情况可能需要修改
            'verifycode': self._getAuthcode(),
            'url': '',
        }
        del self.headers['Upgrade-Insecure-Requests']
        self.headers['Origin'] = 'https://passport.liepin.com'
        self.headers['Referer'] = 'https://passport.liepin.com/h/account'
        response = self.session.post(self.loginUrl, headers=self.headers, data=payload, timeout=10,
                                     proxies=self.proxies, allow_redirects=False)
        return response.status_code, response.text


if __name__ == '__main__':
    userName = input("请输入你的用户名:")
    password = getpass.getpass("password:")
    lp = Leipin(userName, password)
    print(lp.login())
