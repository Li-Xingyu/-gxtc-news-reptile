# -*- coding: UTF-8 -*- 
from bs4 import BeautifulSoup
import requests
import re
import urllib
from openpyxl import Workbook
wb = Workbook()
sheet = wb.active
sheet['A1'] = '标题'
sheet['B1'] = '来源'
sheet['C1'] = '作者'
sheet['D1'] = '发布日期'
sheet['E1'] = '内容'
sheet['F1'] = '图片'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }

def getnews():
    k=2
    #proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080", }
    for a in range(4,120):
        urllist=""
        url=""
        url = 'http://www.gxtc.edu.cn/Category_20/Index_'+str(a)+'.aspx'
        newslist=requests.get(url,headers=headers).text       
        urllist=re.findall('<a href="(.*?)" target="_blank" title="',newslist)  #获取当前页新闻url
        for j in range(11,len(urllist)-1):
            news=""
            newscontent=""
            newscontent2=""
            imgurl=""
            url2='http://www.gxtc.edu.cn'+ urllist[j]	      #构造新闻链接
            #print url2
            news=requests.get(url2,headers=headers)
            news.encoding='UTF-8'
            #print news.text
            title=re.findall('<h2 class="title">(.*?)</h2>',news.text)    #获取标题
            source=re.findall('<span>(.*?)</span>',news.text)             #获取来源
            imglist= re.findall('<img alt="" src="(.*?)"',news.text)      #获取图片列表
            soup = BeautifulSoup(news.text,'html.parser')
            s_list = soup.select('#fontzoom p span')
            p_list = soup.select('#fontzoom p')
            for s in s_list:
                newscontent=newscontent+s.text
            for p in p_list:
                newscontent2=newscontent2+p.text
            newscontent=newscontent+newscontent2
            print newscontent                                             #合并文章内容
            for l in range(0,len(imglist)-1):
                imgurl=imgurl+('http://www.gxtc.edu.cn'+ imglist[l]+'\n')  
            sheet['A'+str(k)] = title[0]
            sheet['B'+str(k)] = source[0]
            sheet['C'+str(k)] = source[1]
            sheet['D'+str(k)] = source[2]                       #作者
            sheet['E'+str(k)] = newscontent
            sheet['F'+str(k)] = imgurl
            #print(newscontent)
            #print re.findall('<img alt="" src="(.*?)"',news.text)
            k=k+1
            wb.save('news.xlsx')    
if __name__ == '__main__':
    getnews()