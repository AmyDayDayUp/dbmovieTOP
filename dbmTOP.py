# 爬取豆瓣电影TOP25/50/.../250的片名、评分、评价人数、链接
# using beautifulsoup
# sos(part of code): https://blog.csdn.net/danielntz/article/details/51861168

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import datetime

# 自行键入地址 or 回车默认
url = input('Enter - ')
if len(url) < 1:
    url = 'https://movie.douban.com/top250'

# 键入需要爬取的页数
count = input('Enter number of pages: ')
today = datetime.date.today()

print("豆瓣电影TOP" + str(25*int(count)) + "\n" + str(today) + "\n" +"影片名               评分       评价人数          链接 ")    

lis = list()
lis.append(url)

for url in lis:
    #print('Retrieving: ', url)
    if len(lis) == int(count) + 1: 
        print('End')
        break
    else:
        # 被反爬虫机制拦截：模拟浏览器访问
        # sos: https://blog.csdn.net/sinat_37812785/article/details/104247874
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'}
        burl = Request(url, headers=headers)
        html = urlopen(burl).read()
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all('div', class_='info'):    
            m_name = tag.find('span', class_='title').get_text()        
            m_rating_score = float(tag.find('span',class_='rating_num').get_text())          
            m_people = tag.find('div',class_="star")  
            m_span = m_people.findAll('span')  
            m_peoplecount = m_span[3].contents[0]  
            m_url=tag.find('a').get('href')  
            print( m_name+"        "  +  str(m_rating_score)   + "           " + m_peoplecount + "    " + m_url )  
        nurl = soup.find('span', class_='next')
        nurl_ = 'https://movie.douban.com/top250' + nurl.find('a').get('href') 
        lis.append(nurl_)
