# 这里需要使用getpass模块才能使输入密码不可见
import getpass
import requests
import hashlib
import time

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7
"""


def get_login(phone, pwd):
    new_time = str(int(time.time()))
    sign = new_time + '_' + hashlib.md5((phone + pwd + new_time).encode("utf-8")).hexdigest()

    print(sign)
    url = "https://appblog.sina.com.cn/api/passport/v3_1/login.php"
    data = {
        "cookie_format": "1",
        "sign": sign,
        "pin": "e3eb41c951f264a6daa16b6e4367e829",
        "appver": "5.3.2",
        "appkey": "2546563246",
        "phone": phone,
        "entry": "app_blog",
        "pwd": pwd
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; nxt-al10 Build/LYZ28N) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 sinablog-android/5.3.2 (Android 5.1.1; zh_CN; huawei nxt-al10/nxt-al10)",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
    }
    r = requests.post(url=url, data=data, headers=headers)
    print(r.json())


if __name__ == '__main__':
    phone = input("你输入你的账号:")
    # 这里输入密码不可见
    pwd = getpass.getpass("password:")

    get_login(phone, pwd)
