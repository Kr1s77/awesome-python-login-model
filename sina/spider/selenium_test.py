# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests,pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
from time import sleep


cookies={}
# with open('E:\Spider\Ajax_微博\cookie.txt')as file:
#     raw_cookies=file.read()
#     for line in raw_cookies.split(';'):
#         key,value=line.split('=',1)
#         cookies[key]=value
#         # print(cookies)

webdriver.DesiredCapabilities.FIREFOX['firefox.page.settings.userAgent'] = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
browser = webdriver.Firefox()
browser.get(url='https://m.weibo.cn/')
sleep(2)
browser.delete_all_cookies()
browser.add_cookie({'name': '_T_WM', 'value': '52b0151e9490855bae540e40f881320f', 'path': '/',  'expiry': 1530671807, 'secure': False, 'httpOnly': True})
browser.add_cookie({'name': 'SUB', 'value': '_2A252ENWfDeRhGeVH6FQX9SzKyD6IHXVV-vvXrDV6PUJbkdANLWHmkW1NT0iViQc71Gn2lMbDYa_ioQFHVnRmZaqg', 'path': '/',  'expiry': 1559615823, 'secure': False, 'httpOnly': True})
browser.add_cookie({'name': 'SUHB', 'value': '0LcSnbMGfYxAbx', 'path': '/', 'expiry': 1559615823, 'secure': False, 'httpOnly': False})
browser.add_cookie({'name': 'SCF', 'value': 'AlYBAKMIZxonUEvbmR6JgqyYWHL1yaDreGv8vXPl1FRCO7xm1IoOxBvQbDb-ZqzXTud9qRC3AnLVu7nFx_MvHdc.', 'path': '/',  'expiry': 1843439823, 'secure': False, 'httpOnly': True})
browser.add_cookie({'name': 'SSOLoginState', 'value': '1528079823', 'path': '/','expiry': None, 'secure': False, 'httpOnly': False})
browser.add_cookie({'name': 'MLOGIN', 'value': '1', 'path': '/', 'expiry': 1528083425, 'secure': False, 'httpOnly': False})
browser.add_cookie({'name': 'M_WEIBOCN_PARAMS', 'value': 'uicode%3D20000174%26featurecode%3D20000320%26fid%3Dhotword', 'path': '/', 'expiry': 1528080425, 'secure': False, 'httpOnly': True})

sleep(2)
browser.get(url='https://m.weibo.cn/')
sleep(40)
print(browser.get_cookies())





# elem=browser.find_element_by_class_name('btn btnWhite')
# elem.click()
# username=browser.find_element_by_id('loginName')
    # username.send_keys('18401570769')


# browser.refresh()
# print(browser.page_source)
# if browser.find_element_by_class_name()



# wb_name = browser.find_element_by_class_name("W_input")
# wb_name.send_keys(input('输入博主ID：'))
# sleep(10)
# search = browser.find_element_by_class_name('W_ficon ficon_search S_ficon')
# search.click()
# sleep(5)
# bz_num = browser.find_element_by_class_name('name_txt')
# bz_num.click()
# sleep(5)
# # 开启了一个新页面，需要跳转到新页面
# handles = browser.window_handles
# browser.switch_to_window(handles[1])