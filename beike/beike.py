"""
info:
author:Forest216
github:https://github.com/Forest216/
update_time:2021-6-16
"""

import requests
from bs4 import BeautifulSoup


header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'referer': 'https://www.jd.com/'
}


def get_url(): #获取url地址 切换城市只需要将nj换为目标城市的缩写即可 如nj南京 sh上海 gz广州 hz杭州 bj北京 wh武汉等待
    url_base='https://nj.zu.ke.com/zufang/pg'
    lists = []
    for i in range(1,11):
        lists.append(url_base+str(i))
    return lists


def get_info(target_url): #返回一个dict型的list，包含各种信息
    house_list = []

    html = requests.get(target_url, headers=header)
    html_bs = BeautifulSoup(html.text, "html5lib")
    goods_div = html_bs.find_all('div', class_='content__list--item')
    for good in goods_div:
        good_temp = {}

        #获取价格
        price_div = good.find_all('span', class_='content__list--item-price')
        price_i = price_div[0].find_all('em')
        price = price_i[0].text
        good_temp['price'] = price

        #获取标题
        title_div = good.find_all('p', class_='content__list--item--title')
        title_em = title_div[0].find_all('a')
        title = title_em[0].text.replace(' ', '').replace('\n', '')
        good_temp['title'] = title

        area_div = good.find_all('p', class_='content__list--item--des')

        detail = area_div[0].text.replace(' ', '').replace('\n', '')  # 江宁-百家湖-朗诗玲珑屿/84.50㎡/南/3室1厅1卫/低楼层（32层）
        area = detail.split('/')[0]
        if area=='精选':
            area = detail.split('/')[1]
        if '-' not in area or len(area.split('-'))<3:
            continue
        location_qu = area.split('-')[0]  # 区划 如栖霞区
        location_big = area.split('-')[1]  # 位置 如仙林
        location_small = area.split('-')[2]  # 小区名 如东方天郡
        size = detail.split('/')[1][:-1]  # 面积 去掉m2
        direction = detail.split('/')[2]  # 朝向
        room = detail.split('/')[3]  # 房间数量 x室x厅
        floor = detail.split('/')[4]  # 楼层

        good_temp['location_qu'] = location_qu
        good_temp['location_big'] = location_big
        good_temp['location_small'] = location_small
        good_temp['size'] = size
        good_temp['direction'] = direction
        good_temp['room'] = room
        good_temp['floor'] = floor

        #图片地址
        image_div = good.find_all('a', class_='content__list--item--aside')
        image_img = image_div[0].find_all('img')
        image = image_img[0].get('data-src')
        good_temp['image'] = image

        #租房页
        link_div = good.find_all('a', class_='content__list--item--aside')
        link = 'https://nj.zu.ke.com' + link_div[0]['href']
        good_temp['link'] = link

        house_list.append(good_temp)
        print(good_temp)



if __name__=='__main__':
    url_lists=get_url()
    for url in url_lists:
        get_info(url)



