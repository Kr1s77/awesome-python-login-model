"""
京东试用自动申请程序，每天仅需执行一次即可
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pyquery import PyQuery as pq
import json
import os
import getpass
import base64

#载入自己编写的配置文件
from Config import settings

#全局变量

#打开无界面的chrome浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
#不打印不重要的日志信息
chrome_options.add_argument('log-level=2')
browser = webdriver.Chrome(chrome_options = chrome_options)
#设置浏览器最长等待时间
wait = WebDriverWait(browser, settings['waitTime'])

#打开用于登陆的chrome浏览器
browser_login = webdriver.Chrome()
#设置浏览器最长等待时间
wait_login = WebDriverWait(browser_login, settings['waitTime'])

def readCookies():
    """
    从文件中读取cookies并返回 文件不存在则返回False
    """
    #不存在cookies文件
    if os.path.exists("cookies.json") == False:
        print("cookies文件不存在！")
        return False
    with open("cookies.json","r") as f:
        cookies = json.load(f)
    return cookies

def writeCookies(cookies):
    """
    从浏览器中向文件写入cookies
    """
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

def closeSW(iApplyNum):
    """
    在文件中输出申请个数 iApplyNum
    关闭了浏览器和程序
    """
    #等待5秒
    time.sleep(5)
    #保存浏览器cookies到文件中
    cookies = browser.get_cookies()
    writeCookies(cookies)

    #关闭浏览器
    browser.quit()
    with open("log.txt", 'a') as f:
        #输出申请时间和数量
        f.write( time.ctime() + " 申请数量：" + str(iApplyNum) + '\n')

    #是否关闭电脑
    if settings['shutdown'] == True:
        os.system("shutdown -s -f")

    #退出程序
    exit()

def genekeys():
    #打开正确/屏蔽词文件,并处理
    keys = []
    for line in open("Truekeyword.txt", 'r' ,encoding='UTF-8' ):
        line = line[0:line.find('\n')]
        if line == '':
            continue
        line = line.split('/')
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        if line[0] == '':
            line[0] = []
        else:
            line[0] = line[0].split(' ')
        if line[1] == '':
            line[1] = []
        else:
            line[1] = line[1].split(' ')
        keys.append(line)
    return keys

def goodJudge(goodName, goodPrice, keys):
    """
    根据商品名称和价格判断是否试用该商品
    """
    if goodPrice < settings['goodPrice']:
        return False

    for key in keys:
        booltrue = False
        if key[0] == []:
            booltrue = True
        for tk in key[0]:
            if tk == '':
                continue
            if tk in goodName:
                booltrue = True
                break
        if booltrue == False:
            continue
        for tk in key[1]:
            if tk == '':
                continue
            if tk in goodName:
                return False
    return True

def do_try(url):
    """
    对于某个商品申请试用
    url为申请网址 iApplyNum为当前申请成功的个数
    """
    try:
        #切换到选项卡1
        browser.switch_to.window(browser.window_handles[1])
        #访问商品网页
        browser.get(url)
        #停2秒
        time.sleep(2)

        #获取网页的html源码
        html = browser.page_source

        #初始化pyquery
        doc = pq(html)

        #获取申请试用的botton
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a'))
        )
        #如果上面写的不是申请试用，就申请下一个
        if button.text!='申请试用':
            return False
        #点击申请试用
        button.click()
        #找到关注并申请的按钮
        button2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'))
        )
        
        time.sleep(1)
        #点击关注
        button2.click()
        #此时试用一件商品完成
        time.sleep(2)
        return True
    #抛出超时异常
    except TimeoutException:
        #这件商品不申请了，返回
        return False


def get_try(cid, iApplyNum, maxApplyNum, keys):
    browser.get('https://try.jd.com/activity/getActivityList?page=1&cids='+cid)

    #获取网页的html源码
    html = browser.page_source

    #初始化pyquery
    doc = pq(html)

    #CSS选择器 找出总页数
    pageitem = doc('.root61 .container .w .p-wrap .p-skip').items()
    #为了应对命名空间而采用的粗暴办法
    pagestr = list(pageitem)[0].text()
    pagestr = pagestr[2:]
    pagestr = pagestr[0:pagestr.find('\n')]
    pagenum = int(pagestr)
    print("商品总页数：" + str(pagenum+1) )

    for i in range(pagenum):

        if i >=1:
            #切换到下一页
            browser.get('https://try.jd.com/activity/getActivityList?page='+str(i+1)+'&cids='+cid)
            #停2秒
            time.sleep(2)
        html = browser.page_source
        doc = pq(html)
        #CSS选择器 找出商品列表
        items = doc('.root61 .container .w .goods-list .items .con .clearfix .item').items()
        
        #迭代器转换为list类型
        items=list(items)
        
        #对于每个商品进行处理
        for item in items:
            #按钮为已申请
            if item('.try-item .try-button').text() == '已申请':
                #已经申请过的不申请
                continue
            #商品名称
            itemname = item('.try-item .p-name').text()
            #商品价格
            itempricetext = item('.try-item .p-price').text()
            #截取多余的文本
            #找不到价格 出现暂无报价的情况
            if itempricetext.find('￥') == -1:
                itemprice = 0
            else:
                itempricetext = itempricetext[itempricetext.find('￥')+1:]
                #goodPrice 商品价格
                itemprice = float(itempricetext)
            if goodJudge(itemname, itemprice, keys) == False:
                #不申请了
                continue
            
            itemurl = item('.try-item .link')
            #试用该商品
            if do_try('https:'+itemurl.attr('href')) == True:
                print("申请成功 " +str(itemprice) + "  " + itemname)
                iApplyNum = iApplyNum + 1
            #停3秒
            time.sleep(2)
            browser.switch_to.window(browser.window_handles[0])

            if iApplyNum >= maxApplyNum:
                print("已经成功申请" + str(maxApplyNum) + "件商品 申请结束")
                closeSW(iApplyNum)
            time.sleep(2)
        print(cid+'类:第'+str(i+1)+'页申请完成')
    return iApplyNum


def trycid():
    """
    控制申请类别和数量 返回已申请数量iApplyNum
    """
    keys = genekeys()
    #京东限制 每天最大申请数量
    maxApplyNum = settings['maxApplyNum']
    iApplyNum = 0
    #获取试用类型
    cids = settings['cids']
    browser.get('https://try.jd.com/')
    browser.get('https://try.jd.com/activity/getActivityList')
    #执行js脚本 打开一个新选项卡
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    for cid in cids:
        iApplyNum = get_try(cid, iApplyNum, maxApplyNum, keys)
    return iApplyNum

def login():
    """
    登陆函数
    """
    #必须访问一次京东
    browser_login.get('https://jd.com')
    #读取文件中的cookies
    cookies = readCookies()
    if cookies != False:
        #如果从文件中读取到了cookies，就放入浏览器中
        for cookie in cookies:
            browser_login.add_cookie(cookie)
    #直接去登陆界面
    browser_login.get('https://passport.jd.com/login.aspx')
    #找到账户登陆的窗口
    button_login = browser_login.find_elements_by_css_selector('#content > div.login-wrap > div.w > div > div.login-tab.login-tab-r > a')
    button_login = button_login[0]
    #点击
    button_login.click()
    time.sleep(2)

    #取得用户名和密码的过程
    #如果文件不存在
    if os.path.exists("login.txt") == False:
        username = input("请输入京东用户名:")
        password = getpass.getpass("请输入京东密码(输入不会显示在屏幕上):")
    else:
        #从文件中读入用户名和密码
        with open("login.txt",) as f:
            up = f.read()
        up = up.split('\n')
        username = up[0].encode()
        password = up[1].encode()
        #base64解码
        username = base64.b64decode(username)
        username = username.decode()
        password = base64.b64decode(password)
        password = password.decode()

    #找到输入框
    input_username =  browser_login.find_element_by_name('loginname')
    #输入用户名
    input_username.send_keys(username)
    #找到密码框
    input_password = browser_login.find_element_by_name('nloginpwd')
    #输入密码
    input_password.send_keys(password)
    #找到登录按钮
    button_logOK = browser_login.find_elements_by_id('loginsubmit')
    button_logOK = button_logOK[0]
    time.sleep(2)
    #点击
    button_logOK.click()

    #循环检测是否登陆
    while 1:
        try:
            wait_login.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ttbar-login > div.dt.cw-icon > a'))
            )
            break
        except TimeoutException:
            continue
    print('登陆成功！')
    time.sleep(2)

    #登录成功后 若不存在login.txt，则把用户名和密码写入文件
    if os.path.exists("login.txt") == False:
        #base64编码
        username = username.encode()
        username = base64.b64encode(username)
        password = password.encode()
        password = base64.b64encode(password)
        # 写入文件中
        with open("login.txt", "w") as f:
            f.write(username.decode() +"\n")
            f.write(password.decode())

    #把登陆浏览器的cookie转移到无界面浏览器上
    #取得原浏览器的所有cookie
    cookies = browser_login.get_cookies()
    browser.get('https://www.jd.com')
    #cookies是一个以字典为元素的list
    for cookie in cookies:
        browser.add_cookie(cookie)
    #关闭登陆浏览器
    browser_login.quit()

if __name__ == '__main__':

    #登陆
    login()
    #开始申请 iApplyNum为申请成功的个数
    iApplyNum = trycid()
    #申请结束
    closeSW(iApplyNum)
