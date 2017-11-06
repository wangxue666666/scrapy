#//span[@class='dy-name ellipsis fl']
#//h3[@class='ellipsis']
from lxml import etree
import requests
import re
head={
'Connection': 'keep-alive',
'Accept': 'text/plain, */*; q=0.01',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
'Referer': 'https://www.douyu.com/directory/all',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.8',

}
page= 120
fist_name= None
ready =new_home_name= []
# while True:
print(page)
url ='http://www.douyu.com/directory/all?page='+str(page)+'&isAjax=1'
response = requests.get(url,headers=head,verify =False)
html = etree.HTML(response.text)

home_name = html.xpath("//h3[@class='ellipsis']/text()")
for home in home_name:
    new_home_name.append(re.sub(r'(\r\n *)|( *)','',home ))
a = list(set(new_home_name))
new_home_name = a[1:]
print(new_home_name)
    # username = html.xpath("//span[@class='dy-name ellipsis fl']/text()")
    # if page == 1:
    #     fist_name = new_home_name[0]
    # else:
    #     if fist_name == new_home_name[0]:
    #         print(new_home_name[0])
    #         break
    # for i in range(len(username)):
    #     ready.append([new_home_name[i],username[i]])
