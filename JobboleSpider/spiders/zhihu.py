# -*- coding: utf-8 -*-

'''

参考
1.http://zrz0f.com/2015/10/19/scrapy/
2.https://github.com/shishengjia/ArticleSpider

'''

import scrapy

from scrapy import Selector

import re
import time
import json

from urllib import parse

from io import BytesIO

# import requests

try:
    from PIL import Image
except:
    pass


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    custom_settings = {
        'COOKIES_ENABLED': True
    }

    def parse(self, response):
        # 提取html页面中所有html， 并跟踪这些url进行进一步爬取
        # 如果提取的url中格式为 /question/xxx 就下载之后进入解析函数
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                print("----------------------")
                print(request_url)
                print(question_id)
                print("----------------------")
        pass

    def parse_detail(self, response):
        pass

    def start_requests(self):
        """
        ZhihuSpider的入口,首先在这里进行请求，从登陆页面得到response，并调用before_login函数。
        """
        return [scrapy.Request("https://www.zhihu.com/#signin", headers=self.headers, callback=self.before_login)]

    def before_login(self, response):
        """
        登陆逻辑执行后调用login判断是否登陆成功
        """
        self._xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract_first()

        # 这里为了获得验证码图片，在发送一个取得验证码图片的请求，将登陆延迟到login_after_captcha函数中，scrapy的Requests会自动管理cookies
        # 当然也可以直接通过requests来发送相应请求来获得验证码图片，不过要设置cookies，从response里获得,确保cookies一致
        numbers = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(numbers)

        yield scrapy.Request(captcha_url, headers=self.headers, callback=self.login)

    def login(self, response):
        post_url = "https://www.zhihu.com/login/phone_num"

        with open("captcha.jpg", "wb") as f:
            f.write(response.body)

        try:
            # 显示验证码
            im = Image.open("captcha.jpg")
            im.show()
            im.close()
        except Exception as e:
            print(e)

        captcha = input("输入验证码: ")

        post_data = {
            "_xsrf": self._xsrf,
            "phone_num": "13419516267",
            "password": "ssjusher123",
            "captcha": captcha
        }

        # 尝试登陆
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login,
        )]


    def check_login(self, response):
        # 验证服务器的返回数据是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                # 不指定callback,默认调用parse函数
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)


    # def get_captcha(self, response):
    #     # 显示验证码，接收用户输入，返回验证码。显示图片使用PIL库，在OSX上可以直接调用预览显示图片，别的系统不知道了。
    #     # 使用 BytesIO 读取二进制图片
    #     Image.open(BytesIO(response.body)).show()
    #     return input("输入验证码: \n>")


