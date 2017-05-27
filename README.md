# JobboleSpider


### 入门
> * 1.use xpath or css selector to get data from html,
> * 2.design article item
> * 3.use pipeline to filter data
> * 4.install MySQLdb, insert data into mysql database with sync(original)/async(Twisted) method.
> * 5.use ItemLoader, rewrite ItemLoader, create some rule functions to make code beauty.

### 参考
[知乎模拟登陆参考](https://github.com/xchaoinfo/fuck-login)

### 注意的地方

#### 1. parse.urljoin
```python
from urllib import parse

parse.urljoin(response.url, post_url)
```
/up/xx.jpg --> www.xxx.com/up/xx.jpg

www.xxx.com/up/xx.jpg 就保持原样

#### 2. `re.match`和`re.search`

> * re.match 尝试从字符串的开始匹配一个模式
> * re.search 函数会在字符串内查找模式匹配,只到找到第一个匹配然后返回，如果字符串没有匹配，则返回None。
