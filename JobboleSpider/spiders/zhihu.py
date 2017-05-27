# -*- coding: utf-8 -*-

'''

参考 http://zrz0f.com/2015/10/19/scrapy/

'''

import scrapy

from scrapy import Selector
from scrapy import Request

import re
import time
import os

from io import BytesIO

# import requests

try:
    from PIL import Image
except:
    pass

# # python2, python3
# try:
#     import cookielib
# except:
#     import http.cookiejar as cookielib
#
# # 使用登录cookie信息
# session = requests.session()
# session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
#
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("Cookie 未能加载")


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "http://www.zhihu.com",
        "User-Agent": agent
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com", headers=self.headers, callback=self.init, meta={"cookiejar": 1})]

    def init(self, response):
        self._xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]

        t = str(int(time.time() * 1000))
        captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login'

        return Request(captcha_url, headers=self.headers, callback=self.login, meta={"cookiejar": 1})


    def login(self, response):
        post_url = "https://www.zhihu.com/login/phone_num"

        post_data = {
            "_xsrf": self._xsrf,
            "phone_num": input("input phone_number:\n"),
            "password": input("input password:\n"),
            "captcha": self.get_captcha(response),
        }

        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login,
            meta={"cookiejar":1}
        )]


    def check_login(self, response):
        # 验证服务器的返回数据是否成功
        print(response.body)
        pass


    def get_captcha(self, response):
        # 显示验证码，接收用户输入，返回验证码。显示图片使用PIL库，在OSX上可以直接调用预览显示图片，别的系统不知道了。
        # 使用 BytesIO 读取二进制图片
        Image.open(BytesIO(response.body)).show()
        return input("输入验证码: \n>")


