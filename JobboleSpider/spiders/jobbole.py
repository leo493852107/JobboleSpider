# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request

import re
import datetime
from urllib import parse

from JobboleSpider.items import JobboleArticleItem
from JobboleSpider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        1. 获取文章列表页中的文章url并交给scrapy下载后进行解析
        2. 获取下一页的url并交给scrapy进行下载, 下载完成后交给parse

        '''

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail, meta={"front_image_url": image_url})

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        # 提取文章的具体字段
        # 通过xpath选取元素
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first("").strip().replace("·","").strip()
        # thumb_up_num = int(response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract_first(""))
        # bookmark_num = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract_first("")
        # match_result = re.match(".*?(\d+).*", bookmark_num)
        # if match_result:
        #     bookmark_num = int(match_result.group(1))
        # else:
        #     bookmark_num = 0
        # comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract_first("")
        # match_result = re.match(".*?(\d+).*", comment_num)
        # if match_result:
        #     comment_num = int(match_result.group(1))
        # else:
        #     comment_num = 0
        # content = response.xpath("//div[@class='entry']").extract_first("")
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ','.join(tag_list)

        article_item = JobboleArticleItem()
        # 通过css选择器选取元素
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        title = response.css(".entry-header h1::text").extract_first("")    # 标题
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first("").strip().replace("·","").strip()   #发布时间
        thumb_up_num = int(response.css(".vote-post-up h10::text").extract_first(""))   # 点赞数
        bookmark_num = response.css(".bookmark-btn::text").extract_first("")    # 收藏数
        match_result = re.match(".*?(\d+).*", bookmark_num)
        if match_result:
            bookmark_num = int(match_result.group(1))
        else:
            bookmark_num = 0
        comment_num = response.css("a[href='#article-comment'] span::text").extract_first("")   #评论数
        match_result = re.match(".*?(\d+).*", comment_num)
        if match_result:
            comment_num = int(match_result.group(1))
        else:
            comment_num = 0
        content = response.css("div.entry").extract()   # 内容
        tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ','.join(tag_list)   #   标签


        article_item["url_obj_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["thumb_up_num"] = thumb_up_num
        article_item["bookmark_num"] = bookmark_num
        article_item["comment_num"] = comment_num
        article_item["content"] = content
        article_item["tags"] = tags

        yield article_item



        pass


