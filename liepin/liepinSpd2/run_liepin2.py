# !/usr/bin/env python
# -*- coding: utf-8 -*-

# 获取settings.py模块的设置
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from liepinSpd2.spiders.liepinJob import LiepinSpdier

settings = get_project_settings()
process = CrawlerProcess(settings=settings)

# 可以添加多个spider类
process.crawl(LiepinSpdier)

# 启动爬虫，会阻塞，直到爬取完成
process.start()