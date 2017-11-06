import requests
head ={
    'Host': 'so.gushiwen.org',
    'Connection': 'keep-alive',
    'Content-Length': '309',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://so.gushiwen.org',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://so.gushiwen.org/user/login.aspx?from=http://so.gushiwen.org/user/collect.aspx',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}
url = 'http://so.gushiwen.org/user/collect.aspx'
sess = requests.session()
sess.cookies.set('pgv_pvid','853613830')
sess.cookies.set('gswEmail','1090509990%40qq.com')
sess.cookies.set('idsShiwen2017','%2c7722%2c71137%2c49386%2c71138%2c71139%2c71250%2c64945%2c69086%2c71131%2c10835%2c')
sess.cookies.set('codeyzgswso','2c66a3bd52ee50d1')
sess.cookies.set('__qc_wId','347')
sess.cookies.set('ASP.NET_SessionId','yzgdnqcxjl3dbgykvyfv4agg')
sess.cookies.set('gsw2017user','167606%7c6A5471B38CFFFF27880E4F7E9679CF7A')
sess.cookies.set('Hm_lvt_04660099568f561a75456483228a9516','1509607003,1509611511,1509611997')
sess.cookies.set('Hm_lpvt_04660099568f561a75456483228a9516','1509612193')
# res = sess.post(url,head)
# print(res.text)


def capitalize(func):
    def wrapper(word):
        return func(word).capitalize()
    return wrapper


@capitalize
def greetings(word='hi there'):
    return word.lower()


q=greetings(word='ADSDSD')

print(q)
