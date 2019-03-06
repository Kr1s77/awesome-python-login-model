#coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
from pyquery import PyQuery as pq
from config import settings as SET
import re

#browser_for_login为正常浏览器，用于登录
browser_for_login = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
#无头模式
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser,10)

total_num_of_products = SET['total_products']
total_num_of_products_cur = 0

choice_list=[]
ban_list=[]



#所有的sleep为了是减慢速度, 防止被检查异常
def do_try(url):
    try:
        browser.switch_to.window(browser.window_handles[1])
        browser.get(url)
        time.sleep(2)
        button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a'))
        )
        #如果按钮不是‘申请使用’，则说明该商品申请出错或者已经申请过了，则跳回到试用商品列表界面
        if button.text!='申请试用':
            browser.switch_to.window(browser.window_handles[0])
            return False
        button.click()
        #等待关注商铺的信息出来，然后点击关注即可。如果无需关注，则可能会抛出超时异常
        button2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'))
        )
        time.sleep(1)
        button2.click()

        time.sleep(2)
        browser.switch_to.window(browser.window_handles[0])
        return True
    except TimeoutException:
        browser.switch_to.window(browser.window_handles[0])     #抛出超时异常则返回到试用商品列表界面即可
        return True


def get_try(page):
    url='https://try.jd.com/activity/getActivityList'+'?page='+str(page)
    browser.get(url)

    time.sleep(2)

    html = browser.page_source
    #print(html)

    #利用PyQuery获得所有关于试用商品跳转的class=item的<li>标签
    doc = pq(html)
    #因为已经申请过的商品的<li>标签中的class除了item，还有applied，故将其删除之后申请便可跳过已申请的商品
    doc('.applied').remove()
    items = doc('.root61 .container .w .goods-list .items .con .clearfix .item').items()
    #print(type(items))
    #print(items)
    items=list(items)

    for item in items:
        #获得每个商品的标题，如果进行商品过滤则有可能有用
        title = item('.p-name').text()

        if check_name(title) == False:
            continue

        price_text = item('.p-price').text()[6:]
        price = float(price_text)
        if price < float(SET['price_limit']):
            continue
        try_url = 'https:'+item('.link').attr('href')
        print('价格: ',price)
        print(title)
        #print(try_url)
        time.sleep(1)
        global total_num_of_products_cur
        global total_num_of_products
        if do_try(try_url) == True:
            total_num_of_products_cur +=1
            print("申请成功")
            print('')
        else :
            print("申请失败")
            print('')

        #到达指定个数之后退出
        if total_num_of_products_cur >= total_num_of_products:
            return



def Control_try(total_page):
    browser.execute_script('window.open()')
    browser.switch_to.window(browser.window_handles[0])
    for page in range(1,total_page+1):
        print('开始申请第'+str(page)+'页')
        get_try(page)
        global total_num_of_products
        global total_num_of_products_cur
        if total_num_of_products_cur >= total_num_of_products:
            return
        print('第'+str(page)+'页申请完成')

#成功登录后将browser_for_login的cookies取出放到无头browser中即可
def login():
    browser_for_login.get('https://passport.jd.com/new/login.aspx')
    while browser_for_login.current_url!='https://www.jd.com/':
        time.sleep(2)

    cookies = browser_for_login.get_cookies()
    browser_for_login.close()
    browser.get('https://www.jd.com')
    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.get('https://www.jd.com')

def auto_showdown():
    if SET['auto_shutdown'] == True:
        print('\n5秒后将自动关机')
        time.sleep(5)
        os.system('shutdown -s -t 1')

def deal_file():
    global choice_list
    global ban_list
    if SET['choice']==True:
        with open('choice.txt','r') as f:
            choice_list = re.split('[ |.|,|!|\n]',f.read())
            f.close()

    if SET['ban']==True:
        with open('ban.txt','r') as f:
            ban_list = re.split('[ |.|,|!|\n]',f.read())
            f.close()

def check_name(title):
    is_choice = False
    if len(choice_list)==0:
        is_choice = True
    for ch in choice_list:
        if ch in title:
            is_choice = True
            break

    if is_choice == False:
        return False
    is_ban = False
    for ba in ban_list:
        if ba in title:
            is_ban = True
            break

    if is_ban == True:
        return False
    return True


if __name__ == '__main__':
    deal_file()
    login()
    #申请前SET['total_num_of_page']页
    Control_try(SET['total_num_of_page'])
    browser.close()
    print('申请完成')
    auto_showdown()
