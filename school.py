# import requests
# from lxml import etree
# import json
# from w3lib.html import remove_tags
# #//div[@class="infobox"]//tr/td[1]
# url = 'http://www.qianmu.org/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
# head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
# res = requests.get(url,headers = head)
# html = etree.HTML(res.text)
# school_url_list = html.xpath('//*[@id="content"]/table/tbody/tr/td[2]/a/@href')
# school_mes = {}
# my_list= ['国家','州省','城市','本科生人数','研究生人数','师生比','国际学生比例','网址']
# home_list = ['国家','州省','城市']
# b=0
# for school_url in school_url_list:
#     a = 0
#     b += 1
#     addr = ''
#     name = school_url.split('/')[-1]
#     school_mes[name]={}
#     res2 = requests.get(school_url,headers = head)
#     school_html = etree.HTML(res2.text)
#     tags = school_html.xpath("//div[@class='infobox']//tr/td[1]/p//text()")
#
#     for i in range(len(tags)):
#         if tags[i] in my_list:
#             try:
#                 text = school_html.xpath("//div[@class='infobox']//tr["+str(i+1)+"]/td[2]/p//text()")[0]
#             except IndexError as e:
#                 text =""
#             if tags[i] in home_list:
#                 a+=1
#                 addr+=text
#                 if a == 3:
#                     school_mes[name]['地址']= addr
#             else:
#                 school_mes[name][tags[i]] = text
#
# a = json.dumps(school_mes)
# with open('school.txt','w') as f:
#     f.write(a)
import json
with open('school.txt','r') as f:
    d = f.read()
print(json.loads(d))