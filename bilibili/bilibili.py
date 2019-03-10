from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from PIL import Image
from io import BytesIO
from time import sleep
import random

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7
"""


class BiliBili():
    """
    登陆B站, 处理验证码
    电脑的缩放比例需要为100%, 否则验证码图片的获取会出现问题
    """

    def __init__(self, username, password):
        """
        初始化
        """
        self.browser = webdriver.Chrome()
        self.url = 'https://passport.bilibili.com/login'
        self.browser.get(self.url)
        self.wait = WebDriverWait(self.browser, 5)
        self.username = username
        self.password = password

    def get_button(self):
        """
        获取滑动块, 并且返回
        :return: button
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
        return button

    def get_screenshot(self, button):
        """
        获取网页两次截图:
            1. 鼠标悬停于button的截图
            2. 鼠标点击button后的截图
        :param button: 滑动块
        :return: 两次截图的结果
        """
        ActionChains(self.browser).move_to_element(button).perform()
        screenshot1 = self.browser.get_screenshot_as_png()
        screenshot1 = Image.open(BytesIO(screenshot1))
        ActionChains(self.browser).click_and_hold(button).perform()
        screenshot2 = self.browser.get_screenshot_as_png()
        screenshot2 = Image.open(BytesIO(screenshot2))
        return (screenshot1, screenshot2)

    def get_position(self, button):
        """
        获取验证码图片的位置
        :return: 位置的四个点参数
        """
        ActionChains(self.browser).move_to_element(button).perform()
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_box')))
        sleep(2)
        location = img.location
        size = img.size
        print(location, size)
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], \
                                   location['x'] + size['width']
        return top, bottom, left, right

    def get_geetest_image(self, button, name1='captcha1.png', name2='captcha2.png'):
        """
        获取两次验证码的截图:
            1. 鼠标悬停于button的截图
            2. 鼠标点击button后的截图
        :param button: 滑动块
        :param name1: 原始验证码保存的名字
        :param name2: 缺块验证码保存的名字
        :return: 两次验证码截图的结果
        """
        top, bottom, left, right = self.get_position(button)
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot(button)
        captcha1 = screenshot[0].crop((left, top, right, bottom))
        captcha1.save(name1)
        captcha2 = screenshot[1].crop((left, top, right, bottom))
        captcha2.save(name2)
        return (captcha1, captcha2)

    def login(self):
        """
        打开浏览器,并且输入账号密码
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.element_to_be_clickable((By.ID, 'login-username')))
        password = self.wait.until(EC.element_to_be_clickable((By.ID, 'login-passwd')))
        sleep(1)
        username.send_keys(self.username)
        sleep(1)
        password.send_keys(self.password)

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1: 原始验证码
        :param img2: 缺块验证码
        :param x: 像素点的x坐标
        :param y: 像素点的y坐标
        :return: 像素是否相同
        """
        pixel1 = img1.load()[x-1, y]
        pixel2 = img2.load()[x-1, y]
        threshold = 100
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 原始验证码
        :param img2: 缺块验证码
        :return: 第二个缺块的左侧的x坐标
        """
        left = 60  # 大致忽略掉第一个缺块
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """
        获取滑块移动轨迹的列表
        :param distance: 第二个缺块的左侧的x坐标
        :return: 滑块移动轨迹列表
        """
        track = []
        current = 0
        mid = distance * 2 / 3
        t = 0.2
        v = 0
        distance += 10  # 使滑块划过目标地点, 然后回退
        while current < distance:
            if current < mid:
                a = random.randint(1, 3)
            else:
                a = -random.randint(3, 5)
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            current += move
            track.append(round(move))
        for i in range(2):
            track.append(-random.randint(2, 3))
        for i in range(2):
            track.append(-random.randint(1, 4))
        print(track)
        return track

    def move_button(self, button, track):
        """
        将滑块拖动到指定位置
        :param button: 滑动块
        :param track: 滑块运动轨迹列表
        :return: None
        """
        ActionChains(self.browser).click_and_hold(button).perform()
        for i in track:
            ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()
            sleep(0.0005)
        sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        """
        串接整个流程:
            1. 输入账号密码
            2. 获取滑动块
            3. 获取两张验证码图片
            4. 获取滑块移动轨迹
            5. 将滑块拖动至指定位置
        :return:
        """
        self.login()
        button = self.get_button()
        captcha = self.get_geetest_image(button)
        left = self.get_gap(captcha[0], captcha[1])
        print(left)
        track = self.get_track(left)
        # 如果尝试登陆失败, 则重新验证, 最多三次
        times = 0
        while times < 3:
            self.move_button(button, track)
            try:
                success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'gt_info_type'), '验证通过:'))
                print(success)
            except TimeoutException as e:
                times += 1
                print('fail')
            else:
                print('success')
                return None


if __name__ == '__main__':
    ACCOUNT = input('请输入您的账号:')
    PASSOWRD = input('请输入您的密码:')

    test = BiliBili(ACCOUNT, PASSOWRD)  # 输入账号和密码
    test.crack()
