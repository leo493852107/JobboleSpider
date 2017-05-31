#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

from scrapy.selector import Selector

import os
import time


# 6.phantomjs
# phantomjs_path = os.path.join(os.path.dirname(__file__), "phantomjs")
# browser = webdriver.PhantomJS(executable_path=phantomjs_path)
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.9.kZkv4Y&id=538218798736&cm_id=140105335569ed55e27b&abbucket=16&sku_properties=10004:709990523;5919063:6536025;12304035:116177")
# print(browser.page_source)
# browser.close()


# chromedriver_path = os.path.join(os.path.dirname(__file__), "chromedriver")


# 5.设置 chromedriver 不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_opt)
# browser.get("https://www.taobao.com/")


# browser = webdriver.Chrome(executable_path=chromedriver_path)

# 4.模拟下拉操作
# browser.get("https://www.oschina.net/blog")
# time.sleep(5)
# for i in range(5):
#     # 执行js代码模拟下拉动作
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)



# 3.模拟登陆微博
# browser.get("http://weibo.com/")
# 等待页面加载
# time.sleep(5)
# browser.find_element_by_css_selector("#loginname").send_keys("183959607xx")
# browser.find_element_by_css_selector(".info_list.password input[name='password']").send_keys("xx")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()



# 2.模拟登陆知乎
# browser.get("https://www.zhihu.com/#signin")
# browser.find_element_by_css_selector('.view-signin input[name="account"]').send_keys("18395960706")
# browser.find_element_by_css_selector('.view-signin input[name="password"]').send_keys("testabc123")
# browser.find_element_by_css_selector('.view-signin .sign-button').click()



# 1.模拟淘宝
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.9.kZkv4Y&id=538218798736&cm_id=140105335569ed55e27b&abbucket=16&sku_properties=10004:709990523;5919063:6536025;12304035:116177")
# print(browser.page_source)
# t_selector = Selector(text=browser.page_source)
# print(t_selector.css(".tm-promo-price .tm-price::text").extract_first())

# browser.quit()


