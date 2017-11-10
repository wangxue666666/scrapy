# scrapy总结

###创建项目后settings的基本配置以及配置介绍

```python
USER_AGENT ='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
#是否遵循爬虫规则限制
ROBOTSTXT_OBEY = False
#Scrapy downloader 并发请求(concurrent requests)的最大值,默认: 16  
CONCURRENT_REQUESTS = 32
#下载器在下载同一个网站下一个页面前需要等待的时间,该选项可以用来限制爬取速度,减轻服务器压力。同时也支持小数:0.25 以秒为单位  
DOWNLOAD_DELAY = 3  
#默认请求头
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   #'Accept-Language': 'en',
}
#下载的中间件
DOWNLOADER_MIDDLEWARES = {
   #'myspider.middlewares.MyCustomDownloaderMiddleware': 543,
      # 'scrapy_splash.SplashCookiesMiddleware': 723,
      # 'scrapy_splash.SplashMiddleware': 725,
      # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
       'myspider.middlewares.PhantomJSMiddleware': 100,
       'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,#禁止内置的中间件
}
#配置项目管道 
ITEM_PIPELINES = {
   'myspider.pipelines.WbtcPipeline': 300,
   #可以定义多个,先运行优先级高的数字越小优先级越高
   #'myspider.pipelines.WbtcPipeline2': 400,

}

#将termianl中的日志写入文件以便以后使用
LOG_FILE='Test.log'
```



 ### 连接数据库

MySQL

​	首先进行数据库的配置

```python
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'scrapy'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'wangxue'
```

​	在pipelines.py中创建一个类

```python
from scrapy.conf import settings
import pymysqls
class WbtcPipeline(object):
    def __init__(self):
      	#这个导入和上面配置不对应正常应该为setting['MYSQL_HOST']
        self.dbpool = pymysql.connect(MYSQL_HOST,MYSQL_USER, MYSQL_PASSWD, MYSQL_DBNAME,charset ='utf8')
        self.cursor = self.dbpool.cursor()
    def process_item(self, item, spider):
        self._conditional_insert(item)
        return item

    def _conditional_insert(self, item):
        self.cursor.execute(
            "insert into home_list(title,room,money,addr) values('%s','%s','%s','%s')"%(item['title'],item['room'],item['money'],item['addr_end'])
        )
        self.dbpool.commit()

    def close_spider(self,spider):
        self.cursor.close()
        self.dbpool.close()

```

​	网上找到的一个比较通用的数据库的操作可以进行增加和修改，前提是数据库的字段名和item的对应的字段名字相同

```python
def process_item(self, item, spider):
    if isinstance(item, WhoscoredNewItem):
        table_name = item.pop('table_name')
        col_str = ''
        row_str = ''
        for key in item.keys():
            col_str = col_str + " " + key + ","
            row_str = "{}'{}',".format(row_str, item[key] if "'" not in item[key] else item[key].replace("'", "\\'"))
            sql = "insert INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE ".format(table_name, col_str[1:-1],
                                                                                    row_str[:-1])
        for (key, value) in six.iteritems(item):
            sql += "{} = '{}', ".format(key, value if "'" not in value else value.replace("'", "\\'"))
        sql = sql[:-2]
        self.cursor.execute(sql)  # 执行SQL
        self.cnx.commit()  # 写入操作
```



### 连接mongodb

```python
#mangodb配置
MDB_HOST = 'localhost'
MDB_PROT = 27017
```

​	

```python
from pymongo import MongoClient
class GupiaospiderPipeline(object):
    def __init__(self):
        self.conn = MongoClient(settings['MDB_HOST'], settings['MDB_PROT'])
        self.db = self.conn[settings['MDB_DATABASE']]
        self.collection = self.db[settings['MDB_TABLE']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

    def close_spider(self,spider):
        self.conn.close()
```

## 切记要在setting.py文件中挂载对应的项目管道

```python
ITEM_PIPELINES = {
  'gupiaospider.pipelines.GupiaospiderPipeline': 300,
}
```



### scrapy中CrawlSpider爬虫使用情况

​	这个爬虫对比Spider相对来说使用起来比较简单但是也有一定的局限性，扒取的网站一定要是那种比较规则的，而且可以扒取链接相对较多并且结构清新的网站。

```python
#首先导入爬虫在导入抓去a标签下链接的模块
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class BookSpider(CrawlSpider):
    name = 'booker'
    start_urls = ['http://mayishensuanzi.quanwenyuedu.io/']
    section = 0
    book_path = os.path.abspath(os.path.dirname(__file__)) + '\\file\\'
    	#deny不允许扒取正则
        text_link = LinkExtractor(allow='/(\d+).html$', deny=(r'big5'))
    rules = (
        # callback是字符串，生成Rule对象，follow为True时可以支持爬虫递归的抓取
        Rule(text_link, callback='get_text', follow=True),
    )
    .....................
```



### 如何扒取js动态加载的数据

​	1、第一种相对简单可以直接用浏览器的控制台或者抓包软件抓取发起ajax请求的网页地址，对其直接发起请求即可

​	2、第二种相对麻烦在请求ajax地址的同时提交了一些表单数据并在后台服务器进行了验证，这个时候我们可以观察一下表单的内容

```
id	2
sky	0695551907e4a5b41dd81d94fd25df7a
t	1510304860
_type	ajax
rndval	1510282750372
```

​	很多时候如rndval这个参数一般都是由时间戳变化而来的，这个时候我们可以伪造一个form表单进行提交

```python
 def get_ajax_info(self, response):
        form_data = {
            'c': 'book',
            'a': 'ajax',
        }

        zz = re.compile(r'setTimeout.*')
        js = zz.search(response.text)
        js_list = js.group().split("','")

        form_data['id'] = js_list[3]
        form_data['sky'] = js_list[5]
        form_data['t'] = js_list[7].split("'")[0]
        form_data['rndval'] = str(int(time.time() * 1000))
        url_str = ''.join(response.url.split('io/')[:-1]) + 'io/index.php?c=book&a=ajax'
        yield scrapy.FormRequest(
            url=url_str,
            formdata=form_data,
            callback=self.get_text
        )
```

​	3、第三种方式是因为有一些网站发起请求时通过js提交的表单过多而且很多都是很复杂的

这个时候我们可以通过python中的selenium+PhantomJS来实现。这不需要对爬虫的主体进行改造但是需要对其中间件进行一些处理

```python
from scrapy.http import HtmlResponse
from selenium import webdriver
js = 'var q=document.body.scrollTop=10000'


class PhantomJSMiddleware(object):
	#在发起请求需要执行的中间件对请求来的
    def process_request(self, request, spider):
        if 'html' in request.url :
          	#将PhantomJS浏览器和selenium关联在一起
            driver = webdriver.PhantomJS(executable_path=r'H:\docker\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            #提交请求的url
            driver.get(request.url)
            #加载自己想要执行的js这里是暴力将浏览器拖到最下面，因为有些需要下来才能加载
            driver.execute_script(js)
            #给浏览器加载js的事件
            time.sleep(3)
            #将加载完的数据拿下来
            content = driver.page_source.encode('utf-8')
            driver.quit()
            return HtmlResponse(request.url,encoding='utf-8',body=content,request=request)
```

	### 	相同的一定要在setting.py中导入

```python

DOWNLOADER_MIDDLEWARES = {
       'myspider.middlewares.PhantomJSMiddleware': 100,
}
```



### 分布式爬虫的配置

​	分布式爬虫就是将爬虫的部署到不同的服务器上并且将这些爬虫通过统一的管理器管理进行不同的扒取

​	1、首先需要对自己的爬虫进行改造，创建爬虫类时不再是继承自scrapy,spider中的Spider或者CrawlSpdier类。而是继承自scrapy_redis.spider中对性的RedisSpdier和RedisCrawlSpder类配置完之后还需要加上redis_key

```python
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

class BizhiSpider(RedisCrawlSpider):
    name = 'bizhi'
    #start_urls = ['http://desk.zol.com.cn/']
    #值随便取这个相当于start_urls，但是直接开始后所有爬虫会等待，需要在redis中输入键值对键名为
    #redis_key的值 值为需要扒取网站的地址
    redis_key = 'bizhi_key'
    ......
```

###		 注意：相对比较坑的是使用RedisCrawlSpider，其中的Rule规则需要scrapy.spider导入而不是scrapy_redis.spider导入，切记导入使用scrapy-redis时一定要导入本模块中的爬虫

​	2、接下来是对setting.py进行配置

```python
REDIS_URL = 'redis://root密码@10.0.142.251:6379'
#使用模块中的去重规则
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
#使用模块中的调度器来代替默认的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
```

#### 		为了能使别的服务器可以访问我们服务器上的redis我们需要需改redis中的bind:127.0.0.1将其注释掉



### 爬虫遇到错误界面时的操作

```python
import scrapy
class ErrorSpider(scrapy.Spider):
    name = 'espider'
    start_urls =['http://www.baidu.com/sdsf']
    #正常情况下遇到404等错误时这个爬虫会直接停止不会再执行parse函数，但是如果加上这个参数那么爬虫在遇到404错误时依旧会继续打印错误界面的信息
    handle_httpstatus_list = [404]
    def parse(self, response):
      	#meta中存储了很多的信息比较有用的是其中存放了很多的重定向的地址，如果我们请求的网址发生了重定向那么就会其中显示出来
        print(response.meta)
        print(response.status)
```



### *如何查看爬虫的执行状况以及在其执行到一定步骤时执行特定的函数等

```python
from scrapy import Spider, signals
from pydispatch import dispatcher

class TestSignal(Spider):
    name = 'testsignal'

    start_urls = ['http://www.bing.com']

    def __init__(self):
      	#signals封装好了很多爬虫执行各个阶段的标志可以将其用dispatcher同不同的函数关联在一起来实现执行到特定步骤时来执行特定的函数
        dispatcher.connect(self.get_spider_open, signals.spider_opened)
        dispatcher.connect(self.get_spider_close, signals.spider_closed)
        dispatcher.connect(self.get_request_scheduled, signals.request_scheduled)
        dispatcher.connect(self.get_response_downloaded, signals.response_downloaded)
        dispatcher.connect(self.get_item_passed, signals.item_passed)
        dispatcher.connect(self.get_item_scraped, signals.item_scraped)
        dispatcher.connect(self.get_item_dropped, signals.item_dropped)
```

### *一些小型的操作

	### 如果想要限制普通爬虫的访问地址在哪个域名下而不是访问网页中所有的链接可以加上

```python
# 域名限定只能访问这个链接下面的链接
allowed_domains  =['http://www.baidu.com']
```



###*各种内置中间件以及自定义中间件介绍

http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/downloader-middleware.html#scrapy.contrib.downloadermiddleware.DownloaderMiddleware.process_request
