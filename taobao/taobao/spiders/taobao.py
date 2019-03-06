# -*- coding: utf-8 -*-
import scrapy,numpy
from scrapy import Selector
from taobao.items import TaobaoItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import requests,re
from scrapy_splash import SplashRequest
from urllib.parse import urlencode


class comicspider(scrapy.Spider):
    name = 'tb'
    allowed_domains=['www.taobao.com']
    start_urls=['https://www.taobao.com']

    headers1 = {
        'Connection': 'keep-alive',
        'Host': 'www.taobao.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers1)

    def sub_nav(self, response):
        page=Selector(response)
        # 女装、男装、内衣
        # sub_navs1=page.xpath('//ul[@class="service-bd"]/li[position()<2]/a/text()').extract()
        # print(sub_navs1)
        sub_urls1=page.xpath('//ul[@class="service-bd"]/li[position()<2]/a/@href').extract()
        # print(sub_urls1)
        for sub_url in sub_urls1:
            yield scrapy.Request(url=sub_url,callback=self.parse0,headers=self.headers1,dont_filter=True)

    def parse0(self, response):
        headers2 = {
            'Connection': 'keep-alive',
            'Host': 's.taobao.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }
        page=Selector(response)
        # 连衣裙、毛衫/内搭、秋外套……
        sub_navs11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/text()').extract()
        del sub_navs11[-1]
        sub_urls11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/@href').extract()
        del sub_urls11[-1]
        for i in range(0,len(sub_urls11)):
            page_urls=[]
            page_urls.append(sub_urls11[i]+'&sort=sale-desc')
            s=0
            sub_nav=sub_navs11[i]
            for j in range(1,20):
            # for j in range(0, 1):
                senddata = {
                    'sort':'sale-desc',
                    'bcoffset': '0',
                    's': s
                }
                page_url=sub_urls11[i]+'&'+ urlencode(senddata)
                page_urls.append(page_url)
                s+=60
            # print(page_urls)

            for page_url in page_urls:
                yield SplashRequest(page_url,self.parse1,args={'wait':0.5},splash_headers=headers2,dont_filter=True,meta={'sub_nav':sub_nav})
                # yield scrapy.Request(page_url,callback=self.parse1,headers=headers2,dont_filter=True,meta={'sub_nav':sub_nav})

    def parse1(self, response):
        headers3 = {
            'Connection': 'keep-alive',
            'Host': 'item.taobao.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }
        page=Selector(response)
        goods_urls=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div/div[3]/div[2]/a/@href').extract()
        # goods_class=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div[1]/div[3]/div[2]/a/span[@class="H"]/text()').extract()
        goods_class=response.meta['sub_nav']
        areas = page.xpath('//div[@class="row row-3 g-clearfix"]/div[@class="location"]/text()').extract()
        sell_counts=page.xpath('//div[@class="deal-cnt"]/text()').extract()

        # print(goods_urls)
        for i in range(0,len(goods_urls)):
            area=areas[i]
            sell_count=sell_counts[i]
            goods_url='http:'+goods_urls[i]
            yield scrapy.Request(goods_url,self.parse2,headers=headers3,dont_filter=True,
                                 meta={'goods_url':goods_url,
                                       'goods_class':goods_class,
                                       'area':area,
                                       'sell_count':sell_count})

    def parse2(self, response):
        item=TaobaoItem()
        page=Selector(response)
        # print(response.text)
        item['title']=page.xpath('//head/title/text()').extract()[0][:-4]
        item['goods_url']=response.meta['goods_url']
        item['goods_class']=response.meta['goods_class']
        item['price']=page.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()[0]
        item['sell_count']=response.meta['sell_count'][:-3]
        item['area']=response.meta['area']
        # item['trade']=page.xpath('//div[@class="tb-sell-counter"]/a/strong/text()').extract()
        seller= page.xpath('//div[@class="tb-shop-name"]/dl/dd/strong/a/@title').extract()
        if len(seller)==1:
            item['seller']=seller[0]
        else:
            seller=page.xpath('//span[@class="shop-name-title"]/@title').extract()
            if len(seller)==1:
                item['seller'] = seller[0]
            else:
                seller = page.xpath('//span[@class="shop-name-title"]/@title').extract()
                if len(seller) == 1:
                    item['seller'] = seller[0]
                else:
                    item['seller'] = '未知'

        yield item








