#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

page_text = '''
<html>
<title> This is Title </title>
<body>
	<h1> This is h1 </h1>
	<div> This is fisrt div </div>
	<div id="divid">
		<img src="1111.png"/>
		<span id="sp1"> desc 1111.png </span>
		<img src="2222.png"/>
		<span id="sp2"> desc 2222.png </span>
		<p>
			<a href="http://www.xxxxx.com/"> link-of-xxxxxx </a>
		</p>
		<a href="http://www.yyyyyyy.com/"> link-of-yyyyyyyyy </a>
		<br/>
		<a href="http://www.zzzzzzz.com/"> link-of-zzzzzzzzz </a>
	</div>
	<p class="p_classname"> This is p with class name </p>
	<div class="div_classname"> This is div with class name </div>
    <p class="div_classname"> This is div with class name2 </p>

</body>
</html>
'''

bsp = BeautifulSoup(page_text, 'lxml')

# 所有 div 元素集合列表
# print(bsp.find_all('div'))
# print(bsp.select('div'))

# 所有拥有id属性的 div 元素集合列表
# print(bsp.select('div[id]'))

# 所有 class 属性为 div_classname 的 div 元素集合列表
# print(bsp.select('div[class=div_classname]'))
# print(bsp.find_all('div',attrs={'class':'div_classname'}))
# print(bsp.select('div.div_classname'))

#所有id属性为divid的元素
# print(bsp.select('#divid'))

# 所有属性 非空 的 div 元素集合列表
# print([ele for ele in bsp.select('div') if ele.attrs])

# 所有属性为 空 的 div 元素集合列表
# print([ele for ele in bsp.select('div') if not ele.attrs])


# 第一个 div 元素列表，注意下标不是 0，而且类型依然是 列表
# print(bsp.div)
print(bsp.find('div'))
#     #获取内容
# print(bsp.div.text)
# print(bsp.div.string)

# 最后一个 div 元素，类型列表
# print(bsp.select('div')[-1])

# 倒数第2个 div 元素，类型列表
# print(bsp.select('div')[-2])

# 位置为最前面 2 个的div元素
print(bsp.find_all('div',limit=2))
# print(bsp.select('div')[0:2])

# 第一个 标签a 的 href属性值，列表
# print(bsp.a.get('href'))
# print(bsp.find('a').get('href'))
# print(bsp.a.attrs['href'])

#第二a元素的所有属性
# print(bsp.find_all('a')[1].attrs)
# 第 2 个 div 标签下一层所有 a 的 href 属性值
print(bsp.select('div[id=divid] > a'))

# 第 2 个 div 标签以下以下所有层面 a 的 href 属性值
print(bsp.select('div[id=divid] a'))
print(bsp.find('div',attrs={'id':'divid'}).find_all('a'))

# 第 2 个 div 标签下第1个 span 的 id 属性值
print(bsp.select('div[id=divid] span')[0].get('id'))

#剔除最后一个div元素
print(bsp.select('div')[:-1])

#获取所有a元素的href
print([ele.get('href') for ele in bsp.select('a')])
# 查找 div 和 p 的集合

# 等价于 html.xpath('//div[position()<3]/a')


