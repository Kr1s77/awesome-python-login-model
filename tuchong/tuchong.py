# -*- coding: utf-8 -*-

'''
Required
- requests (必须)
'''

import rsa
import binascii
import requests
from base64 import b64decode
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 


agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

#pubkey 在页面的js中: http://static.tuchong.net/js/pc/page/welcome_6e7f1cd.js
pubkey = "D8CC0180AFCC72C9F5981BDB90A27928672F1D6EA8A57AF44EFFA7DAF6EFB17DAD9F643B9F9F7A1F05ACC2FEA8DE19F023200EFEE9224104627F1E680CE8F025AF44824A45EA4DDC321672D2DEAA91DB27418CFDD776848F27A76E747D53966683EFB00F7485F3ECF68365F5C10C69969AE3D665162D2EE3A5BA109D7DF6C7A5"
session = requests.session()



def get_crypt_password(message):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)
    return passwd

def get_captcha():
	captcha_url="https://tuchong.com/rest/captcha/image"
	headers={
		'user-agent': agent
	}
	rsp=session.post(captcha_url, data=None, headers=headers).json()
	captcha_id=rsp['captchaId']
	captcha_base64=rsp['captchaBase64']
	captcha_base64=captcha_base64.replace("data:image/png;base64,","")
	with open("captcha.png",'w') as f:
		f.write(b64decode(captcha_base64))
	captcha=input(u'输入当前目录下 captcha.png 上的验证码：')
	return captcha_id,captcha


def login(username,passwd):
	login_url = 'https://tuchong.com/rest/accounts/login'
	headers={
		'user-agent': agent
	}

	passwd_crypt=get_crypt_password(passwd)	
	postdata = {
		'account': username,
        'password': passwd_crypt,
	}

	rsp = session.post(login_url, data=postdata, headers=headers)
	rsp=rsp.json()
	print(rsp)
	#登录成功
	if rsp.has_key('result') and rsp['result']=="SUCCESS":
		print(rsp['message'])
		return 

	#登录失败
	if rsp.has_key('code') and rsp.has_key('message'):
		print("response code:%d, message:%s"%(rsp['code'],rsp['message']))
		if rsp['message'].find("验证码")>=0 : 
			print(rsp['message'])
			captcha=get_captcha()
			postdata={
				'account': username,
	        	'password': passwd_crypt,
				'captcha_id': captcha[0],
				'captcha_token': int(captcha[1])
			}
			rsp = session.post(login_url, data=postdata, headers=headers)
			if str(rsp).find('200'):
				print("登陆成功！")


if __name__ == '__main__':
	username=raw_input(u'用户名：')
	passwd=raw_input(u'密码：')
	login(username,passwd)