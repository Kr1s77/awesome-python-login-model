import time
from selenium import webdriver


def login():
    acount_num = input('请输入账号:\n')
    passwd_str = input('请输入密码:\n')
    driver = webdriver.Chrome()
    url = 'http://mail.126.com/'
    driver.get(url)
    time.sleep(30)

    elem = driver.find_element_by_css_selector("iframe[id^='x-URS-iframe']")
    # # 126登陆框是使用iframe进行嵌套的，所以需要先切换到该iframe
    driver.switch_to.frame(elem)

    acount = driver.find_element_by_name('email')
    acount.clear()
    acount.send_keys(acount_num)

    passwd = driver.find_element_by_name('password')
    passwd.clear()
    passwd.send_keys(passwd_str)

    time.sleep(3)
    click_button = driver.find_element_by_id('dologin')
    click_button.click()
    time.sleep(5)
    cur_cookies = driver.get_cookies()[0]
    return cur_cookies


if __name__ == '__main__':
    login()
