#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Required
- requests (必须)
- pillow (可选)
'''

import requests
import re
import time
import sys
import json  
import rsa
import os.path
import binascii
import datetime
from bs4 import BeautifulSoup
try:
    import cookielib
except:
    import http.cookiejar as cookielib

try:
    from PIL import Image
except:
    pass
    
session = requests.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")

def rsaEncrypt(password):
    url = 'http://passport.bilibili.com/login?act=getkey'
    try:
        getKeyRes = session.get(url)
        token = json.loads(getKeyRes.content.decode('utf-8'))
        pw = str(token['hash'] + password).encode('utf-8')

        key = token['key']
        key = rsa.PublicKey.load_pkcs1_openssl_pem(key)

        pw = rsa.encrypt(pw, key)
        password = binascii.b2a_base64(pw)
        return password
    except:
        return False

def get_vdcode():
    t = str(int(time.time()*1000))
    captcha_url = 'https://passport.bilibili.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha
    
def login(user, password):
    post_url = 'https://passport.bilibili.com/login/dologin'
    payload = {
        'act': 'login',
        'gourl': '',
        'keeptime': '2592000',
        'userid': user,
        'pwd': password,
        'vdcode': get_vdcode(),
    }
    if payload["vdcode"] == None:
        return False

    try:
        resp = session.post(post_url, data=payload)
        session.cookies.save()

        soup = BeautifulSoup(resp.content, 'lxml')
        s = str(soup.select('center')[0])
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        s = s.replace(' ', '')
        s = s.split('>')
        s = s[2]
        s = s.replace('<br/', '')
        flash(s)
        return False
    except requests.exceptions.ConnectionError as e:
        flash(e)
        return False
    except:
        return True

def isLogin():
    url = 'https://account.bilibili.com/home/userInfo'
    resp = session.get(url, allow_redirects=False)
    if  resp.status_code == 200 and resp.json()['code'] == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名：')
        password = input('请输入密码：')
        login(account, rsaEncrypt(password))
