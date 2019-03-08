import requests
import re

headers_login = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'account.guokr.com',
    'Pragma': 'no-cache',
    'Cookie': '__utmt=1; __utma=253067679.2102330349.1540780238.1540780238.1541122809.2; __utmb=253067679.12.9.1541122812936; __utmc=253067679; __utmz=253067679.1540780238.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=253067679.|1=Is%20Registered=No=1; session=afcf1b0f-c71b-43d2-8046-f60ae28f9b45',
    'Referer': 'https://account.guokr.com/sign_in/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36'
}

session = requests.Session()

url = 'https://account.guokr.com/sign_in/'
resp = session.get(url, headers=headers_login)
html = resp.text

csrf_token = re.search(r'id="csrf_token[\s\S]*?(\d+[\s\S]*?)"', html).group(1)
captcha_rand = re.search(r'id="captchaRand[\s\S]*?(\d+)', html).group(1)
img_url = 'https://account.guokr.com/captcha/' + captcha_rand
with open('captcha.jpg', 'wb') as fw:
    fw.write(session.get(img_url, headers=headers_login).content)

username = input('请输入用户名：')
password = input('请输入密码：')
captcha = input('请输入验证码 : ')

data = {
    'csrf_token': csrf_token,
    'username': username,
    'password': password,
    'captcha': captcha,
    'captcha_rand': captcha_rand,
    'permanent': 'y ',
}

response = session.post(url, data=data)
with open('response.html', 'w', encoding='utf-8') as fw:
    fw.write(response.text)

# print(response.cookies)
# print(session.cookies)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36'
}
homepage = 'https://www.guokr.com/i/0210199872/'
with open('homepage.html', 'w', encoding='utf-8') as fw:
    res = session.get(homepage, headers=headers)
    fw.write(res.text)
