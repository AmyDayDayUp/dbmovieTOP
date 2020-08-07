# 爬取豆瓣电影TOP25/50/.../250的片名、评分、评价人数、链接
# using beautifulsoup

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import datetime
import sys
import os

# 自行键入地址 or 回车默认
url = input('Enter - ')
if len(url) < 1:
    url = 'https://movie.douban.com/top250'

# 键入需要爬取的页数
count = input('Enter number of pages: ')
today = datetime.date.today()

# 打印结果保存为 dbmtop.txt
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
 
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass
path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('dbmtop.txt')

print(path)
print('------------------')

# 打印标题、表头
print("豆瓣电影TOP" + str(25*int(count)) + " " + str(today))
# 格式调整（对齐、中文空格填充）, rf:https://www.pythonf.cn/read/53132
# 制表符，rf:https://blog.csdn.net/yedouble/article/details/77816588
print('{:<30}\t{:<9}\t{:<18}\t{:<30}'.format('影片名','评分','评价人数','链接',chr(12288))) 

lis = list()
lis.append(url)

for url in lis:
    if len(lis) == int(count) + 1: 
        print('End')
        break
    else:
        # 被反爬虫机制拦截：模拟浏览器访问
        # rf: https://blog.csdn.net/sinat_37812785/article/details/104247874
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36'}
        burl = Request(url, headers=headers)
        html = urlopen(burl).read()
        soup = BeautifulSoup(html, "html.parser")
        # 豆瓣部分代码 rf: https://blog.csdn.net/danielntz/article/details/51861168
        for tag in soup.find_all('div', class_='info'):    
            m_name = tag.find('span', class_='title').get_text()        
            m_rating_score = float(tag.find('span',class_='rating_num').get_text())          
            m_people = tag.find('div',class_="star")  
            m_span = m_people.findAll('span')  
            m_peoplecount = m_span[3].contents[0]  
            m_url=tag.find('a').get('href') 
            print('{:<30}\t{:<9}\t{:<18}\t{:<30}'.format(m_name,str(m_rating_score),m_peoplecount,m_url,chr(12288))) 
        nurl = soup.find('span', class_='next')
        nurl_ = 'https://movie.douban.com/top250' + nurl.find('a').get('href') 
        lis.append(nurl_)
print('------------------')
