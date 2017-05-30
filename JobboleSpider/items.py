# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from w3lib.html import remove_tags

import datetime

from JobboleSpider.utils.common import extract_num, lagou_date_convert
from JobboleSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT
import re


class JobbolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def remove_splash(value):
    return value.replace("/", "").strip()


def handle_jobaddr(value):
    address_list = value.split("\n")
    address_list = [item.strip() for item in address_list if item.strip() != "查看地图"]
    return "".join(address_list)


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemLoader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_obj_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    thumb_up_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    bookmark_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(extract_num)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO jobbole_article(title, url, create_date, thumb_up_num)
            VALUES (%s, %s, %s, %s)
        """
        params = (self["title"], self["url"], self["create_date"], self["thumb_up_num"])

        return insert_sql, params


class ZhihuQuestionItem(scrapy.Item):
    # 知乎问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            INSERT INTO zhihu_question(zhihu_id, topics, url, title, content, answer_num,
            comments_num, watch_user_num, click_num, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num),
            comments_num=VALUES(comments_num), watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = "".join(self["url"])
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        watch_user_num = extract_num("".join(self["watch_user_num"][0]))
        click_num = extract_num("".join(self["click_num"][1]))
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topics, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    # 知乎问题回答 item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎answer表的sql语句
        insert_sql = """
            INSERT INTO zhihu_answer(zhihu_id, url, question_id, author_id, content,
            praise_num, comments_num, create_time, update_time, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), praise_num=VALUES(praise_num),
            comments_num=VALUES(comments_num), update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params


class LagouJobItem(scrapy.Item):
    # 拉勾网职位item
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    job_type = scrapy.Field()
    tags = scrapy.Field(
        # 将tag元素串联起来
        output_processor=Join(",")
    )
    publish_time = scrapy.Field(
        input_processor=MapCompose(lagou_date_convert)
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_address = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr)
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO lagou(title, url, url_object_id, salary, job_city,
            work_years, degree_need, job_type, tags, publish_time, job_advantage,
            job_desc, job_address, company_name, company_url, crawl_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title), salary=VALUES(salary),
            job_desc=VALUES(job_desc)
        """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary"],
            self["job_city"], self["work_years"], self["degree_need"], self["job_type"],
            self["tags"], self["publish_time"], self["job_advantage"], self["job_desc"],
            self["job_address"], self["company_name"], self["company_url"],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )
        return insert_sql, params


class LagouJobItemLoader(ItemLoader):
    # 自定义职位信息itemloader
    # 配置默认的output_processor,取出list中的第一个元素
    default_output_processor = TakeFirst()

