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
    companylist=['7894126', '7941798', '5464493', '8280653', '8657147', '5696000', '6918711', '8801813', '7909112', '929719', '8635277', '9208490', '9427534', '7873563', '869131', '1983198', '8521820', '8441886', '9425884', '8269623', '8143143', '8144649', '8571478', '8646314', '9086358', '8361354', '8090600', '9652027', '9662729', '8029798', '8024700', '9274661', '8614537', '1852098', '845611', '7910884', '1947829', '6657987', '8463020', '8130349', '8323671', '723421', '1573297', '9582057', '1866404', '1074696', '8586065', '4811624', '857922', '7975388', '7931578', '6615613', '8243943', '682357', '8916773', '1050201', '950043', '7939262', '1730543', '9469426', '7883086', '8628525', '7868218', '8096323', '7862738', '7023768', '8862767', '9538671', '7953390', '515361', '2104592', '993518', '8212985', '1766564', '892388', '8646248', '9857531', '1043007', '8042835', '8980779', '571837', '7862722', '7935093', '8130825', '9111311', '8051561', '9107424', '856576', '7862125', '7947928', '854827', '4209085', '859352', '7931740', '7939262', '548548', '7916182', '8354065', '9740398', '8155722', '2331894', '884195', '9651734', '8534019', '7855573', '9617356', '886895', '2431058', '1939058', '8246296', '9145034', '8161625', '4450360', '540933', '4817469']
    start_urls = []
    for company in companylist:
        start_urls.append(f'https://www.liepin.com/company/{company}/')

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

