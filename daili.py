#60.255.186.169
#8888
import requests
from lxml import etree
head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}

proxy_ip = {
    'http': '60.255.186.169:8888'

}
res = requests.get('http://ip.filefab.com/index.php',
                   proxies = proxy_ip,verify = False)

html = etree.HTML(res.text)
print(html.xpath("//*[@id='ipd']/span/text()"))