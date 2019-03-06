# !/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re
import json
from datetime import datetime
import pandas as pd
import time
'''修改DEFAULT_CIPHERS'''
from twisted.internet.ssl import AcceptableCiphers
from scrapy.core.downloader import contextfactory
contextfactory.DEFAULT_CIPHERS = AcceptableCiphers.fromOpenSSLCipherString('DEFAULT:!DH')

from liepinSpd2.items import Liepinspd2Item


class LiepinSpdier(scrapy.Spider):
    name = 'liepin'
    companylist=['7894126', '7941798', '5464493', '8280653', '8657147', '5696000', '6918711', '8801813', '7909112', '929719', '8635277', '9208490', '9427534', '7873563', '869131', '1983198', '8521820', '8441886', '9425884', '8269623', '8143143', '8144649', '8571478', '8646314', '9086358', '8361354', '8090600', '9652027', '9662729', '8029798', '8024700', '9274661', '8614537', '1852098', '845611', '7910884', '1947829', '6657987', '8463020', '8130349', '8323671', '723421', '1573297', '9582057', '1866404', '1074696', '8586065', '4811624', '857922', '7975388', '7931578', '6615613', '8243943', '682357', '8916773', '1050201', '950043', '7939262', '1730543', '9469426', '7883086', '8628525', '7868218', '8096323', '7862738', '7023768', '8862767', '9538671', '7953390', '515361', '2104592', '993518', '8212985', '1766564', '892388', '8646248', '9857531', '1043007', '8042835', '8980779', '571837', '7862722', '7935093', '8130825', '9111311', '8051561', '9107424', '856576', '7862125', '7947928', '854827', '4209085', '859352', '7931740', '7939262', '548548', '7916182', '8354065', '9740398', '8155722', '2331894', '884195', '9651734', '8534019', '7855573', '9617356', '886895', '2431058', '1939058', '8246296', '9145034', '8161625', '4450360', '540933', '4817469']
    start_urls = []
    for company in companylist:
        start_urls.append(f'https://www.liepin.com/company/{company}/')

    # 公司主要基本信息
    def parse(self, response):
        text = response.text
        #职位总页数
        totalPage =int(re.search(r'var totalPage = ([0-9]+);', text).group(1))
        compId=re.search(r'"pcUrl":"https://www.liepin.com/company/([0-9]+)/',text).group(1)
        for i in range(1, totalPage + 1):
            print(f'第{i}页')
            url = f'https://www.liepin.com/company/{compId}/pn{i}'
            yield scrapy.Request(url,callback=self.parse_list)

    def parse_list(self, response):
        text = response.text
        urls = response.xpath('//div[@class="job-info"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_job)

    def parse_job(self,response):
        item=Liepinspd2Item()
        text = response.text
        as_of_date = datetime.now()
        company_name = response.xpath('//div[@class="title-info"]//a/@title')[0].extract()
        # print(company_name)
        job_name=response.xpath('//div[@class="title-info"]/h1/@title')[0].extract()
        #薪资/城市/经验/学历
        job_label=response.xpath('//li[@data-title=""]/span/text()').extract()
        salary=response.xpath('//p[@class="job-item-title"]/text()')[0].extract().strip(' \r\n')
        city=response.xpath('//p[@class="basic-infor"]//a/text()')[0].extract()
        work_year=response.xpath('//div[@class="job-qualifications"]/span/text()')[1].extract()
        education=response.xpath('//div[@class="job-qualifications"]/span/text()')[0].extract()
        pub_time=response.xpath('//p[@class="basic-infor"]/time/@title')[0].extract()
        job_describe=' '.join(response.xpath('//div[@class="content content-word"]/text()').extract())
        function=re.search(r'所属部门：</span><label>(.*?)</label></li>',text).group(1)

        data = pd.read_csv('G:\workspace\y2019m01\/first_lagou\company300.csv', encoding='gbk')
        try:
            for i in range(len(data)):
                n = 0
                for j in data.loc[i, '股票简称']:
                    if j in company_name:
                        n += 1
                if n == len(data.loc[i, '股票简称']):
                    item['ticker'] = data.loc[i, '股票代码']
        except BaseException as e:
            print('ticker匹配错误')

        item['as_of_date'] = as_of_date
        item['company_name'] = company_name
        item['job_name'] = job_name
        item['job_label'] = job_label
        item['salary'] = salary
        item['city'] = city
        item['education'] = education
        item['work_year'] = work_year
        item['pub_time'] = (datetime.strptime(pub_time, u"%Y年%m月%d日").date())  # 最后确定一下格式
        item['job_describe'] = job_describe
        item['function'] = function
        item['spider_time'] = datetime.strptime(str(datetime.now())[:10], '%Y-%m-%d').date()
        # item['origin_site'] = url
        # print(item['pub_time'],item['ticker'],item['company_name'])
        yield item
        # except BaseException as e:
        #     print('111error and pass')
        #     time.sleep(1)

        # company_name = response.xpath('//div[@class="name-and-welfare"]//h1/text()')[0].extract()
        # # print(company_name)
        # job_names=response.xpath('//div[@class="job-info"]/a[@class="title"]/text()').extract()
        # #薪资/城市/经验/学历
        # condition_clearfixs=response.xpath('//p[@class="condition clearfix"]/@title').extract()
        # pub_times=response.xpath('//p[@class="time-info clearfix"]/time/@title').extract()
        # urls=response.xpath('//div[@class="job-info"]/a/@href').extract()
        # for job_name, condition_clearfix, pub_time,url in zip(job_names, condition_clearfixs, pub_times,urls):
        #     # try:
        #     item['job_name']=job_name.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
        #     item['salary']=condition_clearfix.split('_')[0]
        #     item['city']=condition_clearfix.split('_')[1]
        #     item['education']=condition_clearfix.split('_')[2]
        #     item['work_year']=condition_clearfix.split('_')[3]
        #     item['pub_time']=pub_time#最后确定一下格式
        #     data = pd.read_csv('G:\workspace\y2019m01\/first_lagou\company300.csv', encoding='gbk')
        #     try:
        #         for i in range(len(data)):
        #             n = 0
        #             for j in data.loc[i, '股票简称']:
        #                 if j in company_name:
        #                     n += 1
        #             if n == len(data.loc[i, '股票简称']):
        #                 item['ticker'] = data.loc[i, '股票代码']
        #                 print(n, item['ticker'], company_name)
        #     except BaseException as e:
        #         item['ticker'] = 'None'
        #         print('ticker匹配错误')
        #     item['as_of_date'] = as_of_date
        #     item['company_name'] = company_name
        #     item['spider_time'] = datetime.strptime(str(datetime.now())[:10], '%Y-%m-%d').date()
        #     item['origin_site'] = url
        #     print(item['pub_time'],item['ticker'],item['company_name'])
        #     yield item