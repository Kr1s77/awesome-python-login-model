#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

import requests

# 定义请求url
url = "https://movie.douban.com/j/search_subjects"

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
# 循环构建请求参数并且发送请求
for page_start in range(0, 100, 20):
    params = {
        "type": "movie",
        "tag": "热门",
        "sort": "recommend",
        "page_limit": "20",
        "page_start": page_start
    }
    response = requests.get(
        url=url,
        headers=headers,
        params=params
    )

    # 方式一 直接转换json方法
    # results = response.json()
    # 方式二：手动转换
    # 获取字符串
    content = response.content
    # 转换成字符串
    results = json.loads(content)

    # 解析结果
    for movie in results["subjects"]:
        print(movie["title"], movie["rate"])
