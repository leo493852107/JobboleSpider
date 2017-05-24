# -*- coding: utf-8 -*-
import scrapy

import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/111249/']

    def parse(self, response):
        # 通过xpath选取元素
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first().strip().replace("·","").strip()
        thumb_up_num = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first())
        bookmark = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first()
        match_result = re.match(".*?(\d+).*", bookmark)
        if match_result:
            bookmark = match_result.group(1)
        comment = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        match_result = re.match(".*?(\d+).*", comment)
        if match_result:
            comment = match_result.group(1)
        content = response.xpath("//div[@class='entry']").extract_first()
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ','.join(tag_list)


        # 通过css选择器选取元素
        title = response.css(".entry-header h1::text").extract_first()
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first().strip().replace("·","").strip()
        thumb_up_num = int(response.css(".vote-post-up h10::text").extract_first())
        bookmark = response.css(".bookmark-btn::text").extract_first()
        match_result = re.match(".*?(\d+).*", bookmark)
        if match_result:
            bookmark = match_result.group(1)
            comment = response.css("a[href='#article-comment'] span::text").extract_first()
        match_result = re.match(".*?(\d+).*", comment)
        if match_result:
            comment = match_result.group(1)
        content = response.css("div.entry").extract()
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ','.join(tag_list)

        pass


