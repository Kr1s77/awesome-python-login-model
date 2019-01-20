from selenium import webdriver
import time
import requests

# 这个地方是通过观察html代码得到的，因为我先前通过find方法定位switch始终提示我没有这个元素，那么我就猜想它肯定是被隐藏或者嵌套在别的
# frame中了
login_url = 'http://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=http%3A//qzs.qq.com/qzone/v6/portal/proxy.html' \
            '&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&' \
            'appid=549000912&style=22&target=self&s_url=http%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara' \
            '%3Dizone%26specifyurl%3Dhttp%253A%252F%252Fuser.qzone.qq.com%252F1796246076&pt_qr_app=手机QQ空间' \
            '&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=http%3A//qzs.qq.com/qzone/v6/reg/index.html' \
            '&pt_qr_help_link=http%3A//z.qzone.com/download.html'
login_name = input('请输入QQ号:')
login_password = input('请输入QQ密码:')
# 不知是不是selenium的版本问题还是操作平台问题，如今的selenium安装好了使用webdriver.Firefox()/webdriver.Chrome()可能会报错，在ide下并不会
# 提示webdriver.*。遇到这种情况直接删除python安装目录下的selenium文件夹。这样import selenium.webdriver才是导入的site-packges目录下的webdriver模块
driver = webdriver.Chrome(executable_path='D:/webdriver/chromedriver.exe')
driver.get(login_url)
time.sleep(3)

login_type = driver.find_element_by_id('switcher_plogin')

login_type.click()

username = driver.find_element_by_id('u')
username.clear()
password = driver.find_element_by_id('p')
password.clear()
username.send_keys(login_name)
password.send_keys(login_password)

submit = driver.find_element_by_id('login_button')
submit.click()
time.sleep(5)

cookies = driver.get_cookies()
driver.close()

cookie = [item['name'] + "=" + item['value'] for item in cookies]
cookiestr = '; '.join(item for item in cookie)

headers = {'cookie': cookiestr}

# 验证cookie是否正确
myspace = 'http://user.qzone.qq.com/17962460'
content = requests.get(myspace, headers=headers)
print(content.text)