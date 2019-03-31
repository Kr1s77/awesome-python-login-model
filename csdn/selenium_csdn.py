from selenium import webdriver


def login(email, password):
    # 1. 驱动
    browser = webdriver.Chrome()

    # 2. 操作浏览器行为
    browser.get("https://passport.csdn.net/login")

    # 3. 找到账号登陆接口并点击
    input_button = browser.find_element_by_xpath('//div[@class="main-select"]/ul/li[2]/a')
    input_button.click()

    # 4. 输入账号密码，并点击登陆
    # 输入账号
    input_element = browser.find_element_by_xpath(
        '//div[@class="col-xs-12 col-sm-12 control-col-pos col-pr-no col-pl-no"]/input')
    input_element.send_keys(email)

    # 输入密码
    input_password = browser.find_element_by_xpath(
        '//div[@class="col-xs-12 col-sm-12 control-col-pos col-pr-no col-pl-no"]/input[@id="password-number"]')
    input_password.send_keys(password)

    # 点击登陆
    touch_button = browser.find_element_by_xpath('//button')
    touch_button.click()


if __name__ == '__main__':
    email = input("请输入你的账号")
    password = input("请输入你的密码:")
    login(email, password)
