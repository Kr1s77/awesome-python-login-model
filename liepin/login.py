# -*- coding: utf-8 -*-
# @Time    : 2019/5/8 下午1:53
# @Author  : xuzongyuan
# @Site    : guapier.github.io
# @File    : login.py
# @Software: PyCharm
# @Function: 模拟登录猎聘
import time
import requests
import execjs
import re
import json
import hashlib

headers = {
    'Referer': 'https://www.liepin.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/73.0.3683.103 Safari/537.36',
    'DNT': '1',
}


def loads_jsonp(_jsonp):
    """
    解析jsonp数据格式为json
    :return:
    """
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def get_token(username):
    """
    获取用户token和加密js
    :param username: 用户名
    :return:
    """
    params = (
        ('sign', username),
        ('callback', 'jQuery171029989774566236793_' + timestamp),
        ('_', timestamp),
    )

    response = requests.get('https://passport.liepin.com/verificationcode/v1/js.json', headers=headers, params=params)
    print(response.text)
    return loads_jsonp(response.text)


def login(username, password):
    """
    登录
    :param username: 用户名
    :param password: 密码
    :return:
    """
    result = get_token(username)
    token = result.get('data').get('token')
    js = result.get('data').get('js')
    print(token, js, sep='\n')

    ctx = execjs.compile(js)
    value = ctx.call('encryptData', username)

    m = hashlib.md5()
    m.update(password.encode('utf-8'))

    params = (
        ('callback', 'jQuery17108618602708711502_'+timestamp),
        ('login', username),
        ('pwd', m.hexdigest()),
        ('token', token),
        ('value', value),
        ('url', ''),
        ('_bi_source', '0'),
        ('_bi_role', '0'),
        ('_', timestamp),
    )

    response = requests.get('https://passport.liepin.com/account/individual/v1/login.json', headers=headers,
                            params=params)
    print(response.text)


if __name__ == '__main__':
    timestamp = str(int(time.time() * 1000))
    login('用户名', '密码')

