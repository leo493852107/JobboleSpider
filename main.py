#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy.cmdline import execute

import sys
import os


'''
    获取 main.py
    os.path.abspath(__file__)

    获取 JobboleSpider 目录
    os.path.dirname( main.py ) 函数
'''

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])