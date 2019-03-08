# -*- coding:utf-8 -*-
import re
import os
import time
import json
import sys
import subprocess
import requests
import hashlib
from bs4 import BeautifulSoup

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-6
"""


class Lagou_login(object):
    def __init__(self):
        self.session = requests.session()
        self.CaptchaImagePath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'captcha.jpg'
        self.HEADERS = {'Referer': 'https://passport.lagou.com/login/login.html',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36'
                                      ' Core/1.53.4882.400 QQBrowser/9.7.13059.400',
                        'X-Requested-With': 'XMLHttpRequest'}

    # 密码加密
    def encryptPwd(self, passwd):
        # 对密码进行了md5双重加密
        passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
        # veennike 这个值是在js文件找到的一个写死的值
        passwd = 'veenike' + passwd + 'veenike'
        passwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
        return passwd

    # 获取请求token
    def getTokenCode(self):
        login_page = 'https://passport.lagou.com/login/login.html'

        data = self.session.get(login_page, headers=self.HEADERS)

        soup = BeautifulSoup(data.content, "lxml", from_encoding='utf-8')
        '''
            要从登录页面提取token，code， 在头信息里面添加
            <!-- 页面样式 --><!-- 动态token，防御伪造请求，重复提交 -->
            <script type="text/javascript">
                window.X_Anti_Forge_Token = 'dde4db4a-888e-47ca-8277-0c6da6a8fc19';
                window.X_Anti_Forge_Code = '61142241';
            </script>
        '''
        anti_token = {'X-Anit-Forge-Token': 'None',
                      'X-Anit-Forge-Code': '0'}
        anti = soup.findAll('script')[1].getText().splitlines()
        anti = [str(x) for x in anti]

        anti_token['X-Anit-Forge-Token'] = re.findall(r'= \'(.+?)\'', anti[1])[0]
        anti_token['X-Anit-Forge-Code'] = re.findall(r'= \'(.+?)\'', anti[2])[0]

        return anti_token

    # 人工读取验证码并返回
    def getCaptcha(self):
        captchaImgUrl = 'https://passport.lagou.com/vcode/create?from=register&refresh=%s' % time.time()
        # 写入验证码图片
        f = open(self.CaptchaImagePath, 'wb')
        f.write(self.session.get(captchaImgUrl, headers=self.HEADERS).content)
        f.close()
        # 打开验证码图片
        if sys.platform.find('darwin') >= 0:
            subprocess.call(['open', self.CaptchaImagePath])
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', self.CaptchaImagePath])
        else:
            os.startfile(self.CaptchaImagePath)

        # 输入返回验证码
        captcha = input("请输入当前地址(% s)的验证码: " % self.CaptchaImagePath)
        print('你输入的验证码是:% s' % captcha)
        return captcha

    # 登陆操作
    def login(self, user, passwd, captchaData=None, token_code=None):
        postData = {'isValidate': 'true',
                    'password': passwd,
                    # 如需验证码,则添加上验证码
                    'request_form_verifyCode': (captchaData if captchaData != None else ''),
                    'submit': '',
                    'username': user
                    }
        login_url = 'https://passport.lagou.com/login/login.json'

        # 头信息添加tokena
        login_headers = self.HEADERS.copy()
        token_code = self.getTokenCode() if token_code is None else token_code
        login_headers.update(token_code)

        # data = {"content":{"rows":[]},"message":"该帐号不存在或密码错误，请重新输入","state":400}
        response = self.session.post(login_url, data=postData, headers=login_headers)
        data = json.loads(response.content.decode('utf-8'))

        if data['state'] == 1:
            return response.content
        elif data['state'] == 10010:
            print(data['message'])
            captchaData = self.getCaptcha()
            token_code = {'X-Anit-Forge-Code': data['submitCode'], 'X-Anit-Forge-Token': data['submitToken']}
            return self.login(user, passwd, captchaData, token_code)
        else:
            print(data['message'])
            return False


if __name__ == "__main__":

    username = input("请输入你的手机号或者邮箱\n >>>:")
    passwd = input("请输入你的密码\n >>>:")

    lg = Lagou_login()
    passwd = lg.encryptPwd(passwd)

    data = lg.login(username, passwd)
    if data:
        print(data)
        print('登录成功')
    else:
        print('登录不成功')
