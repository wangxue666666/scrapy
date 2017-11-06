import requests
from lxml import etree

head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}


def upload_img(url):
    req = requests.get(url,headers=head)
    html = etree.HTML(req.text)
    img_list = html.xpath("//img[@class='sell_img']/@src")
    for i in img_list:
        img_req = requests.get(i,headers = head)
        print(i)
        with open("upload\\"+i.split('/')[-1],'wb') as f:
            f.write(img_req.content)
for page in  range(2,100):
    print(page)
    url = 'http://www.gandianli.com/sell/list.php?catid=&page='+str(page)+'&price=0&thumb=0&vip=0&day=0&order=&list=1'
    upload_img(url)
