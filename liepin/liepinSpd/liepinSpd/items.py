# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinspdItem(scrapy.Item):
    # define the fields for your item here like:
    as_of_date = scrapy.Field()
    ticker = scrapy.Field()
    company_name = scrapy.Field()
    stage = scrapy.Field()
    size = scrapy.Field()
    city = scrapy.Field()
    industry = scrapy.Field()
    comp_clearfix = scrapy.Field()
    rate_num = scrapy.Field()
    job_count = scrapy.Field()
    registered_capital = scrapy.Field()

    spider_time = scrapy.Field()
    origin_site = scrapy.Field()

