# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests, pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
from time import sleep

# 连接数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='zkyr1006',
                             db='python',
                             charset='utf8')

cursor = connection.cursor()
sql = "USE python;"
cursor.execute(sql)
connection.commit()

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2145291155',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def create_sheet(bozhu):
    try:
        weibo = '''
            CREATE TABLE weibo(
                ID  VARCHAR (255) NOT NULL PRIMARY KEY,
                text VARCHAR (255),
                attitudes VARCHAR (255),
                comments VARCHAR (255), 
                reposts VARCHAR (255) 
            )
        '''
        # 序号 INT  NOT NULL PRIMARY KEY AUTO_INCREMENT,
        cursor.execute(weibo)
        connection.commit()
    except:
        pass


def url_get():
    # # 自动保持cookie,不需要自己维护cookie内容
    # cookies = {}
    # s = requests.session()
    # with open('E:\example\豆瓣读书爬虫\cookie.txt')as file:
    #     raw_cookies = file.read()
    #     for line in raw_cookies.split(';'):
    #         key, value = line.split('=', 1)
    #         cookies[key] = value
    #         # 完善header
    # header = {'Upgrade-Insecure-Requests': '1',
    #           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    #           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #           'Accept-Encoding': 'gzip, deflate, br',
    #           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #           }
    # # get请求，应答解码
    # response = s.get(url=xl_url, headers=header,cookies=cookies)
    browser = webdriver.PhantomJS()
    browser.get(url='https://m.weibo.cn/')
    wb_name = browser.find_element_by_class_name("W_input")
    wb_name.send_keys(input('输入博主ID：'))
    sleep(10)
    search = browser.find_element_by_class_name('W_ficon ficon_search S_ficon')
    search.click()
    sleep(5)
    bz_num = browser.find_element_by_class_name('name_txt')
    bz_num.click()
    sleep(5)
    # 开启了一个新页面，需要跳转到新页面
    handles = browser.window_handles
    browser.switch_to_window(handles[1])


# https://m.weibo.cn/api/container/getIndex?type=uid&value=2145291155&containerid=1076032145291155
# 拼接url
def get_page(page):
    # 查询字符串
    params = {
        'type': 'uid',
        'value': '2145291155',
        'containerid': '1076032145291155',
        'page': page
    }
    # 调用urlencode() 方法将params参数转化为 URL 的 GET请求参数
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


# 存储数据，存储到数据库
def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for index, item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog')
                # weibo = {}
                # weibo['id'] = item.get('id')
                # weibo['text'] =
                # weibo['attitudes'] = item.get('attitudes_count')
                # weibo['comments'] = item.get('comments_count')
                # weibo['reposts'] = item.get('reposts_count')
                weibo = []
                weibo.append(item.get('id'))
                weibo.append(pq(item.get('text')).text())
                weibo.append(item.get('attitudes_count'))
                weibo.append(item.get('comments_count'))
                weibo.append(item.get('reposts_count'))
                # 遇见重复数据，pass，是根据主键来判断，如果是重复数据，忽略，但是报警告
                try:
                    sql = '''INSERT INTO weibo (ID,text,attitudes,comments,reposts)
                          VALUES (%s,%s,%s,%s,%s) '''
                    cursor.execute(sql, weibo)
                    connection.commit()
                except:
                    pass
            yield weibo


if __name__ == '__main__':
    for page in range(1, 17):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)

cursor.close()

# 可以爬任意指定博主所有微博，以博主名建立表，分别储存信息
# 使用selenium+PhantomJS抓取对应博主主页链接
