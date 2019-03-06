# !/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re
from datetime import datetime
import pandas as pd
import time

from liepinSpd.items import LiepinspdItem


class LiepinSpdier(scrapy.Spider):
    name = 'liepin'
    data = pd.read_csv('G:\workspace\y2019m02\company500.csv', encoding='utf-8')
    companylist=data['股票简称']
    start_urls = []
    for company in companylist:
        start_urls.append(f'https://www.liepin.com/zhaopin/?key={company}')

    # 公司主要基本信息
    def parse(self, response):
        # company = response.meta['company']
        text = response.text
        # print(text)
        # 抓取公司基本信息
        # try:
        company_name = response.xpath('//div[@class="name-and-welfare"]//h1/text()')[0].extract()
        # print(company_name)
        comp_sum_tag = response.xpath('//div[@class="comp-summary-tag"]/a/text()').extract()
        # 好几个
        stage=comp_sum_tag[0]
        # print(stage)
        size=comp_sum_tag[1]
        # print(size)
        city=comp_sum_tag[2]
        # print(city)
        industry=comp_sum_tag[3]
        # print(industy)
        #公司标签,list
        comp_clearfix = str(response.xpath('//ul[@class="comp-tag-list clearfix"]//span/text()').extract())
        # print(comp_clearfix)
        #简历处理率   *%转化为float
        rate_num = response.xpath('//p[@class="rate-num"]//span/text()')[0].extract()
        rate_num=int(rate_num)/100
        # print(rate_num)

        job_count = int(re.search(r'<small data-selector="total">. 共([0-9]+) 个', text).group(1))
        # print(job_count)
        #注册资本(万元)
        if '注册资本' in text and '万元人民币' in text:
            registered_capital = float(re.search(r'<li>注册资本：(.*?)万元人民币</li>', text).group(1))
        else:
            registered_capital =0.0
        # print(registered_capital)
        origin_site=re.search(r'"wapUrl":"(.*?)",', text).group(1)
        item = LiepinspdItem()
        # 匹配股票代码,判断如果股票简称全部在公司名内,则匹配股票代码
        data = pd.read_csv('G:\workspace\y2019m01\/first_lagou\company300.csv', encoding='gbk')
        try:
            for i in range(len(data)):
                n = 0
                for j in data.loc[i, '股票简称']:
                    if j in company_name:
                        n += 1
                if n == len(data.loc[i, '股票简称']):
                    item['ticker'] = data.loc[i, '股票代码']
                    # print(n, item['ticker'], company_name)
                # else:
                #     item['ticker'] ='未匹配'
        except BaseException as e:
            print('ticker匹配错误')

        item['as_of_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['company_name'] = company_name
        item['stage'] = stage
        item['size'] = size
        item['city'] = city
        item['industry'] = industry
        item['comp_clearfix'] = comp_clearfix
        item['rate_num'] = rate_num
        item['job_count'] = job_count
        item['registered_capital'] = registered_capital
        item['spider_time'] = datetime.strptime(str(datetime.now())[:10], '%Y-%m-%d').date()
        item['origin_site'] = origin_site

        yield item
        # except BaseException as e:
        #     print('error and pass')

