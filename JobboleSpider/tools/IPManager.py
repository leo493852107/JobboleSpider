#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import MySQLdb

from JobboleSpider.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD

conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME, charset="utf8")
cursor = conn.cursor()


class IPManager(object):
    def delete_ip(self, ip):
        sql = """
            DELETE FROM xicidaili WHERE ip_address='{0}'
        """.format(ip)
        cursor.execute(sql)
        conn.commit()
        return True

    def check_ip(self, ip, port):
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        proxy_dic = {
            "http": proxy_url
        }
        try:
            # 设置访问返回时间，超过1s就扔掉
            response = requests.get(http_url, proxies=proxy_dic, timeout=1)
        except Exception as e:
            print("无效ip")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("有效ip")
                return True
            else:
                print("无效ip")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        sql = """
            SELECT ip_address, port FROM xicidaili ORDER BY RAND() LIMIT 1
        """
        result = cursor.execute(sql)
        for ip_info in cursor.fetchall():
            ip, port = ip_info
            available = self.check_ip(ip, port)

            if available:
                return "http://{0}:{1}".format(ip, port)
            else:
                # 无效ip重新获取
                return self.get_random_ip()


if __name__ == "__main__":
    manager = IPManager()
    manager.get_random_ip()

