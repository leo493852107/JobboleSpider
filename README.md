# JobboleSpider


### 入门
> * 1.use xpath or css selector to get data from html,
> * 2.design article item
> * 3.use pipeline to filter data
> * 4.install MySQLdb, insert data into mysql database with sync(original)/async(Twisted) method.
> * 5.use ItemLoader, rewrite ItemLoader, create some rule functions to make code beauty.


### 注意的地方

#### 1. parse.urljoin
```python
from urllib import parse

parse.urljoin(response.url, post_url)
```
/up/xx.jpg --> www.xxx.com/up/xx.jpg

www.xxx.com/up/xx.jpg 就保持原样