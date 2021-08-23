# coding:utf-8


from __future__ import absolute_import


try:
    from .SDK基类 import Base
except ImportError:
    from SDK基类 import Base

from time import time,sleep
from threading import Thread
import json

import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import numpy as np 
from io import BytesIO

class JD(Base):

    def __init__(self):
        super(JD,self).__init__()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Referer':'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
        })

    # def g_tk(self,string:str=None,cookieName:str='wq_skey'):
    #     if not string:
    #         string = self.cookies.get(cookieName,'')
    # 	r = 5381
    #     for t in range(len(string)):
    #         r += (r << 5) + ord(string[t])
    #     return 2147483647 & r
    def g_tk(self,string:str=None,cookieName:str='wq_skey'):
        if not string:
            string = self.cookies.get(cookieName,'')
        r = 5381
        for t in range(len(string)):
            r += (r << 5) + ord(string(t))
            return 2147483647 & r

    def login(self):
        t = int(time()*1000)
        url = f'https://qr.m.jd.com/show?appid=133&size=147&t={t}'
        img = self.get(url).content
        return img
    
    def checkState(self,cookieName:str='wlfstk_smdl',timeout=30):
        token = self.cookies.get(cookieName)
        def run():
            nonlocal timeout
            while timeout > 0:
                res = self.get(f'https://qr.m.jd.com/check?callback=a&isNewVersion=1&_format_=json&appid=133&token={token}',headers=self.head)
                data = json.loads(res.text[2:-1])
                if data['code'] == 200:
                    ticket = data['ticket']
                    res = self.get(f'https://passport.jd.com/uc/qrCodeTicketValidation?t={ticket}',headers=self.head)
                    data = json.loads(res.text)
                    if not data['returnCode']:
                        print(data['url'])
                        res = self.get(data['url'],headers=self.head)
                    break
                else:
                    print(data['msg'])
                timeout -= 1
                sleep(1)
        thr = Thread(target=run)
        return thr



if __name__ == '__main__':
    jd = JD()
    img = jd.login()
    plt.imshow(mpimg.imread(BytesIO(img)))
    plt.show()
    thr = jd.checkState()
    thr.start()
    thr.join()
    res = jd.get(f'https://wq.jd.com/user/info/QueryJDUserInfo?sceneid=80027&sceneval=2&g_login_type=1&g_tk={jd.g_tk()}&g_ty=ls&_format_=json',headers=jd.head)
    print(res.text)