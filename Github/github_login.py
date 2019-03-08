import getpass

import requests
from pyquery import PyQuery as pq

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7
"""


class Login(object):
    def __init__(self):
        base_url = 'https://github.com/'
        # 登陆 url 
        self.login_url = base_url + 'login'
        # 提交表单的 api
        self.post_url = base_url + 'session'
        # 个人资料页面的 url
        self.logined_url = base_url + 'settings/profile'
        # 构造一个会话对象
        self.session = requests.Session()
        # 自定义请求头
        self.session.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }

    def token(self):
        # 请求登陆页面
        response = self.session.get(self.login_url)
        # 提取 authenticity_token 的 value，
        doc = pq(response.text)
        token = doc('input[name="authenticity_token"]').attr("value").strip()
        return token

    def login(self, email, password):
        token = self.token()
        # 构造表单数据
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': email,
            'password': password
        }
        # 发送 POST 请求，它会 302 重定向至 'https://github.com/'，也就是响应 'https://github.com/' 的页面
        response = self.session.post(self.post_url, data=post_data)
        # 可以发现 302 重定向至 'https://github.com/'
        print(f"\n请求 url：{response.url}")
        if response.status_code == 200:
            print("status_code: 200")
            self.home(response.text)

        # 请求个人资料页
        response = self.session.get(self.logined_url)
        if response.status_code == 200:
            print("status_code: 200")
            self.profile(response.text)

    def home(self, html):
        doc = pq(html)
        # 提取用户名
        user_name = doc("summary > span").text().strip()
        print(f"用户名：{user_name}")

        # 提取仓库列表        
        Repositories = doc("div.Box-body > ul > li").text().split()
        for Repositorie in Repositories:
            print(Repositorie)

    def profile(self, html):
        doc = pq(html)
        page_title = doc("title").text()
        user_profile_bio = doc("#user_profile_bio").text()
        user_profile_company = doc("#user_profile_company").attr("value")
        user_profile_location = doc("#user_profile_location").attr("value")
        print(f"页面标题：{page_title}")
        print(f"用户资料描述：{user_profile_bio}")
        print(f"用户资料公司：{user_profile_company}")
        print(f"用户资料地点：{user_profile_location}")

    def main(self):
        email = input("email or username: ")
        # 输入的密码不可见，注意密码一定不能错
        password = getpass.getpass("password:")
        self.login(email=email, password=password)


if __name__ == "__main__":
    login = Login()
    login.main()
