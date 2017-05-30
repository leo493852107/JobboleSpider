# -*- coding: utf-8 -*-

'''

参考
1.http://zrz0f.com/2015/10/19/scrapy/
2.https://github.com/shishengjia/ArticleSpider

'''

import scrapy

from scrapy import Selector
from scrapy.loader import ItemLoader

from JobboleSpider.items import ZhihuQuestionItem, ZhihuAnswerItem
from JobboleSpider.settings import USER_AGENT_LIST


import re
import time
import json
import datetime
import random

from urllib import parse


try:
    from PIL import Image
except:
    pass


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.is_normal%2Cis_collapsed%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&limit={1}offset={2}"

    random_index = random.randint(0, len(USER_AGENT_LIST)-1)
    random_agent = USER_AGENT_LIST[random_index]
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": random_agent
    }

    custom_settings = {
        'COOKIES_ENABLED': True
    }

    def parse(self, response):
        # 提取html页面中所有html， 并跟踪这些url进行进一步爬取
        # 如果提取的url中格式为 /question/xxx 就下载之后进入解析函数
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 去重
        all_urls = list(set(all_urls))
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_all = re.findall("(.*zhihu.com/question/(\d+))(/|$).*", url)
            for match_obj in match_all:
                request_url = match_obj[0]
                question_id = match_obj[1]
                yield scrapy.Request(request_url, meta={"question_id": question_id}, headers=self.headers, callback=self.parse_question)
                # break

    def parse_question(self, response):
        # 处理question页面，从页面中提取出具体的question item
        question_id = int(response.meta.get("question_id", ""))
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css("title", ".QuestionHeader-title::text")
        # item_loader.add_css("content", ".QuestionHeader-detail span::text")
        # 有些只有标题没有内容，先用标题替代内容
        item_loader.add_xpath("content", '//*[@class="QuestionHeader-detail"]/div/div/span/text()|//*[@class="QuestionHeader-main"]/h1/text()')
        item_loader.add_value("url", response.url)
        item_loader.add_value("zhihu_id", question_id)
        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".NumberBoard-value::text")
        item_loader.add_css("click_num", ".NumberBoard-value::text")
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")
        question_item = item_loader.load_item()

        # 传入问题的id，每次请求的数量，以及第一次请求的偏移值
        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        # 处理question的answer
        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        next_url = answer_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else answer["excerpt"]
            answer_item["praise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)


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


