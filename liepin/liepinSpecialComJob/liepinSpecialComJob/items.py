# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinspecialcomjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    as_of_date = scrapy.Field()
    ticker = scrapy.Field()
    company_name = scrapy.Field()
    job_name = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    work_year = scrapy.Field()
    pub_time = scrapy.Field()
    education = scrapy.Field()
    origin_site = scrapy.Field()
