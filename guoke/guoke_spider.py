# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode
from requests import codes
import os
from multiprocessing.pool import Pool
from bs4 import BeautifulSoup as bsp
import json
import time
import re

"""
info:
author:CriseLYJ
github:https://github.com/CriseLYJ/
update_time:2019-3-7

"""


def get_index(offset):
    base_url = 'http://www.guokr.com/apis/minisite/article.json?'
    data = {
        'retrieve_type': "by_subject",
        'limit': "20",
        'offset': offset
    }
    url = base_url + urlencode(data)
    # print(url)
    try:
        resp = requests.get(url)
        if codes.ok == resp.status_code:
            return resp.json()
    except requests.ConnectionError:
        return None


# 解析出文章的url
def get_url(json):
    if json.get('result'):
        result = json.get('result')
        for item in result:
            if item.get('cell_type') is not None:
                continue
            yield item.get('url')
    """
    try:
        result=json.load(json)
        if result:
            for i in result.get('result'):
                yield i.get('url')
    """


# 解析文章详情页
def get_text(url):
    html = requests.get(url).text
    print(html)
    soup = bsp(html, 'lxml')
    title = soup.find('h1', id='articleTitle').get_text()
    autor = soup.find('div', class_="content-th-info").find('a').get_text()
    article_content = soup.find('div', class_="document").find_all('p')
    all_p = [i.get_text() for i in article_content if not i.find('img') and not i.find('a')]  # 去除标签
    article = '\n'.join(all_p)
    yield {"title": title, "autor": autor, "article": article}


def save_article(content):
    try:
        if content.get('title'):
            file_name = str(content.get('title')) + '.txt'
            with open(file_name, 'w', encoding='utf-8') as f:
                # f.write(json.dumps(content,ensure_ascii=False))
                f.write('\n'.join([str(content.get('title')), str(content.get('autor')), str(content.get('article'))]))
                print('Downloaded article path is %s' % file_name)
        else:
            file_name = str(content.get('title')) + '.txt'
            print('Already Downloaded', file_name)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % content)


def main(offset):
    result = get_index(offset)
    all_url = get_url(result)
    for url in all_url:
        article = get_text(url)
        for art in article:
            # print(art)
            save_article(art)


GROUP_START = 0
GROUP_END = 7

if __name__ == '__main__':
    for i in range(GROUP_START, GROUP_END + 1):
        main(offset=i * 20 + 18)
        time.sleep(1)
