#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from scrapy.selector import Selector
import MySQLdb

from JobboleSpider.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD

conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME, charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }

    for i in range(1, 100):
        result = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=result.text)

        ip_list = []
        all_trs = selector.css("#ip_list tr")
        for tr in all_trs[1:]:
            ip_address = tr.xpath('td[2]/text()').extract_first()
            port = tr.xpath('td[3]/text()').extract_first()
            speed_str = tr.css('.bar::attr(title)').extract_first()
            if speed_str:
                speed = float(speed_str.split('秒')[0])

            ip_list.append((ip_address, port, speed))

        for item in ip_list:
            sql = '''
                INSERT INTO xicidaili(ip_address, port, speed) VALUES (
                  '{0}', '{1}', {2}
                ) ON DUPLICATE KEY UPDATE ip_address=VALUES(ip_address)
            '''.format(item[0], item[1], item[2])


            cursor.execute(sql)
            conn.commit()



if __name__ == "__main__":
    crawl_ips()
