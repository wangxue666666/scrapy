import scrapy
import json

class WeiboSpdier(scrapy.Spider):
    name = 'weibo'
    head_base = {
        'Host': 'passport.weibo.cn',
        'Connection': 'keep - alive',
        #'Content - Length': '154',
        'Origin': 'https: // passport.weibo.cn',
        'User - Agent': 'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/60.0.3112.78Safari/537.36',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Accept': '* / *',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2Fpub&backTitle=%CE%A2%B2%A9&vt=',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
    }
    login_text = {
        'username':'17862518955',
        'password':'987412365',
    }
    url_base = 'https://m.weibo.cn/feed/friends?version=v4&next_cursor=4171712000062136&page='
    index = 1
    #使用start_requests函数代替代替start_url
    def start_requests(self):
        #使用FormRequest函数，默认请求方式为POST
        yield scrapy.FormRequest(
            url='https://passport.weibo.cn/sso/login',
            formdata=self.login_text,
            headers=self.head_base,
            callback=self.parse,
        )
    def parse(self, response):
        yield scrapy.Request('https://m.weibo.cn/feed/friends?version=v4&next_cursor=4171712000062136&page=1',callback=self.download_json)

    def download_json(self,response):
        #print(response.text)
        jsonobj = json.loads(response.text)
        for ele in jsonobj[0]['card_group']:
            a = ele['mblog']['text']
        self.index += 1
        url_str = self.url_base+str(self.index)
        print(url_str)
        yield scrapy.Request(url_str,callback=self.download_json)
class ZhiHu(scrapy.Spider):
    name = 'zhihu'
    start_urls = 'https://www.zhihu.com/api/v3/feed/topstory?action_feed=True&limit=10&session_token=a479e0dc048e516de77909581486326f&action=down&after_id=19&desktop=true'
    head = {
        'Host': ' www.zhihu.com',
        'Connection': ' keep-alive',
        'accept': ' application/json, text/plain, */*',
        'X-UDID': ' AJACHB1ypgyPTrBpPg8fyMJ1diPwBqE2y10=',
        'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'X-API-VERSION': ' 3.0.53',
        'authorization': ' Bearer Mi4xeW43ckJRQUFBQUFBa0FJY0hYS21EQmNBQUFCaEFsVk5jTHZ2V2dBNjVRZEx0ZEEzVlhNbzBxU3BSbmNWMFpnMjBR|1510108529|a77075822e749d35ad1ba05e6b6d0d30347a07dc',
        'Referer': ' https://www.zhihu.com/',
        'Accept-Encoding': ' gzip, deflate, br',
         'Accept-Language': ' zh-CN,zh;q=0.8',
    }
    cookie = {
        '_zap': 'f42c333a-1a29-449e-b383-79649b6db921',
        'q_c1':'ccb92a5b128c40149b275020561fe846 | 1510108415000 | 1510108415000',
        'r_cap_id': 'MWJmODc3MmVkYTkwNDAyNGI1MzMwOWQyODdjMzBlMmE=|1510108415|1e8a46a29e16d26608cbdc13298281d43bf243f4',
        'd_c0': 'AJACHB1ypgyPTrBpPg8fyMJ1diPwBqE2y10=|1510108415',
        'cap_id': 'YzY5MGE2MmFlNGEzNDMxY2EyNDY0Njc0NWI1ZjdkY2Q=|1510108486|9519cda93c5e63b948d62e023ded95e2b4d77f0e',
        '__utma': '51854390.13263352.1510108416.1510108416.1510108416.1',
        '__utmb': '51854390.0.10.1510108416',
        '__utmz': '51854390.1510108416.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '__utmv':'51854390.000 - - | 3 = entry_date = 20171108 = 1',
        'z_c0': 'Mi4xeW43ckJRQUFBQUFBa0FJY0hYS21EQmNBQUFCaEFsVk5jTHZ2V2dBNjVRZEx0ZEEzVlhNbzBxU3BSbmNWMFpnMjBR|1510108529|a77075822e749d35ad1ba05e6b6d0d30347a07dc',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls,cookies=self.cookie,headers=self.head)

    def parse(self, response):
        print(response.text)
