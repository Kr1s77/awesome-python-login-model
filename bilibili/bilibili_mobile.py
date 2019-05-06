import rsa
import copy
import json
import time
import base64
import hashlib
import requests
import traceback
import urllib.parse


class BiliBili():
    """
    模拟手机端登录B站
    """

    def __init__(self, username, password):
        """
        初始化
        """
        self.username = username
        self.password = password
        self.key_url = "https://passport.bilibili.com/api/oauth2/getKey"
        self.login_url = "https://passport.bilibili.com/api/v3/oauth2/login"
        self.app_key = "27eb53fc9058f8c3"
        self.app_secret = "c2ed53a74eeefe3cf99fbd01d8c9c375"
        self.app_build = "8400"
        # 通用headers
        self.headers = {
            "access_key": '',
            "actionKey": "appkey",
            "appkey": self.app_key,
            "build": self.app_build,
            "device": "phone",
            "mobi_app": "iphone",
            "platform": "ios",
            "ts": "",
            "type": "json"
        }

    def dict_sort_by_key(self, d):
        """
        字典根据key值排序
        """
        return [(k, d[k]) for k in sorted(d.keys())]

    def openssl_public_encrypt(self, plaintext, key):
        """
        加密密码
        """
        key = rsa.PublicKey.load_pkcs1_openssl_pem(key)
        cipher_text = rsa.encrypt(plaintext.encode(), key)
        return cipher_text

    def sign(self, p):
        """
        md5加密headers
        """
        headers = copy.copy(self.headers)
        headers["ts"] = int(time.time())
        p = self.dict_sort_by_key(dict(p, **headers))
        data = urllib.parse.urlencode(p)
        md5 = hashlib.md5()
        md5.update(data.encode() + self.app_secret.encode())
        sign = {"sign": md5.hexdigest()}
        p = dict(p, **sign)
        return p

    def get_key(self):
        """
        获取public_key
        """
        r = requests.post(self.key_url, headers=self.headers, data=self.sign({}))
        try:
            data = json.loads(r.text)
            if data["code"] != 0:
                print("获取public_key失败，返回是：\n", r.text)
            else:
                return data["data"]["key"], data["data"]["hash"]
        except json.decoder.JSONDecodeError:
            print("获取public_key的返回解析失败，不是json格式，返回是：\n", r.text)
        except Exception:
            print("获取public_key失败，未知错误，错误信息是：\n", traceback.format_exc())

    def login(self):
        """
        登录
        """
        key, hash_ = self.get_key()
        if key is None or hash_ is None:
            print("登录失败，无法获取public_key")
            return
        else:
            crypt = self.openssl_public_encrypt(hash_ + self.password, key)
            payload = {
                'seccode': '',
                'validate': '',
                'subid': 1,
                'permission': 'ALL',
                'username': self.username,
                'password': base64.b64encode(crypt),
                'captcha': '',
                'challenge': '',
                'cookies': ''
            }
            r = requests.post(self.login_url, headers=self.headers, data=self.sign(payload))
            try:
                data = json.loads(r.text)
                if data["code"] != 0:
                    print("账号登陆失败" + "-" + data["message"])
                else:
                    print("账号登陆成功")
            except json.decoder.JSONDecodeError:
                print("登录的返回解析失败，不是json格式，返回是：\n", r.text)
            except Exception:
                print("登录失败，未知错误，错误信息是：\n", traceback.format_exc())


if __name__ == '__main__':
    username = input('请输入您的账号:')
    password = input('请输入您的密码:')

    client = BiliBili(username, password)
    client.login()
