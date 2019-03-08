# ！/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-8
"""


class loginTB(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # 设置一个智能等待
        self.wait = WebDriverWait(self.driver, 5)

    def login(self, key, pw):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.driver.get(url)
        try:
            # 寻找密码登陆按钮
            login_links = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='密码登录']"))
            )
            login_links.click()
        except TimeoutException as e:
            print("找不到登陆入口，原因是：", e)
        else:
            # 输入账号密码
            input_key = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='TPL_username']"))
            )
            input_pw = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='TPL_password']"))
            )
            input_key.clear()
            input_pw.clear()
            input_key.send_keys(key)
            input_pw.send_keys(pw)
            self.driver.find_element_by_xpath('//*[@id="J_SubmitStatic"]').click()
            try:
                # 试探能否找到个人信息，如果找不到说明登录失败
                user_info = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='m-userinfo']"))
                )
                print('已经登陆成功，进入了个人中心')
            except TimeoutException:
                try:
                    self.driver.find_element_by_xpath("//div[@class='avatar-wrapper']")
                    print('已经登录成功，进入了淘宝网首页')
                except:
                    try:
                        # 尝试找手机验证框，如果能找到说明要手机验证
                        frame = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//div[@class="login-check-left"]/iframe'))
                        )
                        print('本次登录需要进行手机验证...')
                    except TimeoutException:
                        # 找不到手机验证说明密码账号输入错误，要重新输入
                        print('登录失败，目测是账号或密码有误，请检查后重新登录...')
                        key = input('请重新输入账号：').strip()
                        pw = input('请重新输入密码：').strip()
                        self.login(key, pw)
                    else:
                        self.driver.switch_to.frame(frame)
                        phone_num = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//button[@id="J_GetCode"]'))
                        )
                        phone_num.click()
                        phone_key = input('请输入手机验证码：').strip()
                        key_send = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//input[@id="J_Phone_Checkcode"]'))
                        )
                        key_send.send_keys(phone_key)
                        go_button = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]'))
                        )
                        go_button.click()
                        user_info = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='m-userinfo']"))
                        )
                        print('手机验证登陆成功！！！')


if __name__ == '__main__':
    t = time.time()
    l = loginTB()
    l.login('username', 'password')
    print('登录完成，耗时{:.2f}秒'.format(float(time.time() - t)))
