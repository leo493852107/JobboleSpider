# JobboleSpider

## 本项目使用 python3


### 入门
> * 1.use xpath or css selector to get data from html,
> * 2.design article item
> * 3.use pipeline to filter data
> * 4.install MySQLdb, insert data into mysql database with sync(original)/async(Twisted) method.
> * 5.use ItemLoader, rewrite ItemLoader, create some rule functions to make code beauty.

### 进阶
> * 自定义Middleware：`RandomUserAgentMiddleware`和`RandomProxyMiddleware`
用来切换请求头和代理服务器
> * 写了`crawl_xici_ip.py`脚本用来保存西刺数据，用`IPManager`来过滤无效的`ip`
> * `ocr.py`是之前大神写的识别学校emis学生登录二维码用的，简单识别几位数字
> * 在`lagou.py`中使用`custom_settings`限制了爬虫访问的间隔时间`"DOWNLOAD_DELAY": 3`
，貌似不会302了
> * 动态获取网页有很多种形式，推荐使用chrome，比较稳定
> * [`scrapy` 暂停和重启](https://doc.scrapy.org/en/latest/topics/jobs.html)
>
```python
scrapy crawl lagou -s JOBDIR=crawl_status_info/001
```
将爬取的信息保存在`crawl_status_info`文件夹下，如果要另外爬取可以放在002目录下

> *


### 参考
> * [知乎模拟登陆参考](https://github.com/xchaoinfo/fuck-login)
> * [`fake_useragent`](https://github.com/hellysmile/fake-useragent)牛逼的神器，随意切换 `User-Agent`


### 注意的地方

> * 1. parse.urljoin
```python
from urllib import parse

parse.urljoin(response.url, post_url)
```
/up/xx.jpg --> www.xxx.com/up/xx.jpg

www.xxx.com/up/xx.jpg 就保持原样

> * 2. `re.match`和`re.search`

>> * re.match 尝试从字符串的开始匹配一个模式
>> * re.search 函数会在字符串内查找模式匹配,只到找到第一个匹配然后返回，如果字符串没有匹配，则返回None。


