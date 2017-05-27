#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
re.match 尝试从字符串的开始匹配一个模式
re.search函数会在字符串内查找模式匹配,只到找到第一个匹配然后返回，如果字符串没有匹配，则返回None。

2017.5.26 错误
{
    "r": 1,
    "errcode": 1991829,
    "data": {"captcha":"验证码会话无效 :(","name":"ERR_VERIFY_CAPTCHA_SESSION_INVALID"},
    "msg": "验证码会话无效 :("
}


'''

import requests
import os

# python2, python3
try:
    import cookielib
except:
    import http.cookiejar as cookielib

try:
    from PIL import Image
except:
    pass

import re
import time


agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
headers = {
    "Host": "www.zhihu.com",
    "Referer": "http://www.zhihu.com",
    "User-Agent": agent
}


# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    # 获取登录时需要用到的_xsrf
    index_url = "https://www.zhihu.com"
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = '.*name="_xsrf" value="(.*?)"'
    _xsrf = re.findall(pattern, html)

    return _xsrf[0]


def get_captcha():
    # 获取 验证码
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + '&type=login'
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()

    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        img = Image.open('captcha.jpg')
        img.show()
        img.close()
    except:
        print('请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))

    captcha = input('please input the captcha\n>')
    return captcha


def get_index():
    response = session.get("https://www.zhihu.com/", headers=headers)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def zhihu_login(account, password):
    # 知乎登录
    if re.match("1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password,
            "captcha": get_captcha()
        }
    elif "@" in account:
        print("email登录")
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xsrf": get_xsrf(),
            "email": account,
            "password": password,
            "captcha": get_captcha()
        }

    response_text = session.post(post_url, data=post_data, headers=headers)
    session.cookies.save()


isLogin()

# zhihu_login("leo493852107@163.com", "testabc123")


