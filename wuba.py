from bs4 import BeautifulSoup
import requests

url = 'http://as.58.com/pingbandiannao/31948535519940x.shtml'
# wb_data = requests.get(url)
# soup = BeautifulSoup(wb_data.text,'lxml')
"""
从当前列表页中提取所有出售商品链接
"""
def get_links_from(who_sells=0):
    urls = []
    urls1 = []
    list_view = 'http://su.58.com/pbdn/{}/pn2/'.format(str(who_sells))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text,'lxml')
    for link in soup.select('td.t.t_b a.t'):
        urls1.append(link.get('href'))
    for key,value in enumerate(urls1):
        if key%2 == 1:
            urls.append(value)
    return urls


"""
单页商品中提取商品[title(商品名),price(商品价格),area(卖家区域),date(出售日期),cate(商品分类),views(浏览数量)]
"""
def get_item_info(who_sells=0):
    urls = get_links_from(who_sells)
    for url in urls:
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text,'lxml')
        data = {
            'title':soup.title.text,
            'price':soup.select('.price')[0].text,
            'area':list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span','c_25d') else None,
            'date':soup.select('.time')[0].text,
            'cate':'个人'if who_sells==0 else '商家',
            'views':get_views_from(url)
        }
        print(data)
"""
提取单页浏览数量
"""
def get_views_from(url):
    id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(id)
    js = requests.get(api)
    views = js.text.split('=')[-1]
    return views
    # print(views)

get_item_info()
# # get_links_from()
# get_views_from(url)