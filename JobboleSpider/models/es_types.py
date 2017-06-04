#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


# Define a default Elasticsearch client
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    # 源码自己有问题，什么都不做，避免报错
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])


class ArticleType(DocType):
    # 伯乐在线文章item
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    create_date = Date()
    url = Keyword()
    url_obj_id = Keyword()
    front_image_url = Keyword()
    front_image_path = Keyword()
    thumb_up_num = Integer()
    bookmark_num = Integer()
    comment_num = Integer()
    content = Text(analyzer="ik_max_word")
    tags = Text(analyzer="ik_max_word")

    class Meta:
        index = "jobbole"
        doc_type = "article"


# 先运行一下，创建 Kibana 中 jobbole 数据结构
if __name__ == '__main__':
    ArticleType.init()