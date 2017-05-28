#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def extract_num(value):
    # 从字符串中提取出数字
    match_result = re.match(".*?(\d+).*", value)
    if match_result:
        nums = int(match_result.group(1))
    else:
        nums = 0
    return nums


if __name__ == '__main__':
    print(get_md5("http://jobbole.com".encode("utf-8")))