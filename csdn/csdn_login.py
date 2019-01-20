# -*-coding;utf-8 -*-

import requests
from bs4 import BeautifulSoup


# 获取登陆页面
session = requests.session()
url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'


def get_post_headers():
    return {
        'Host': 'passport.csdn.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'http://www.csdn.net/'
    }


def get_post_data():
    username = input('请输入用户名:\n')
    password = input('请输入密码:\n')

    login_page = session.get(url, headers=get_post_headers()).text
    # 提取lt, execution, _eventId
    soup = BeautifulSoup(login_page, 'html.parser')
    lt = soup.find(attrs={'name': 'lt'})['value']
    execution = soup.find(attrs={'name': 'execution'})['value']
    submit = soup.find(attrs={'name': '_eventId'})['value']
    return dict(username=username, password=password, lt=lt, execution=execution, _eventId=submit)


# 返回登录过后的session
def login(post_data):
    session.post(url, data=post_data, headers=get_post_headers())
    return session

if __name__ == '__main__':
    session = login(get_post_data())
    # 检查是否正常登录
    home_page = 'http://my.csdn.net/my/mycsdn'
    # 这里headers不能用前面那个，因为Host等参数发生改变了，否则会出现500状态码
    headers = {
        'Host': 'my.csdn.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'Accept'
    }
    resp = session.get(home_page, headers='')
    print(resp.text)