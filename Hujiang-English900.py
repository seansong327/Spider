# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup

def getHTML(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    myRequest = request.Request(url, headers=header)
    response = request.urlopen(myRequest)
    html = response.read()
    return html.decode("utf-8")

def getContentLinks(html):
    htmlObj=BeautifulSoup(html,'html.parser')
    links1 = [aElement['href'] for aElement in htmlObj.select(".sp-img-content")]
    links2 = [aElement['href'] for aElement in htmlObj.select(".sp-article-list a")]
    return links1+links2

urls = [
    "https://en.hujiang.com/pinpaikouyu/kouyu900/",
    "https://en.hujiang.com/pinpaikouyu/kouyu900_2/",
    "https://en.hujiang.com/pinpaikouyu/kouyu900_3/",
    "https://en.hujiang.com/pinpaikouyu/kouyu900_4/",
    "https://en.hujiang.com/pinpaikouyu/kouyu900_5/",
    "https://en.hujiang.com/pinpaikouyu/kouyu900_6/"]

links=[]
for url in urls:
    links = links + getContentLinks(getHTML(url)) 

class Sentence(object):
    def __init__(self, en, cn):
        self.en = en
        self.cn = cn

def writeLinkContentToFile(url):
    html = getHTML(url)
    htmlObj = BeautifulSoup(html,'html.parser')

    sentenceArr = []
    # remove the lookup link
    for divElement in htmlObj.select(".langs_en"):
        for aElement in divElement.select("a"):
            aElement.replaceWith(aElement.string)
        tempStr = ""
        for child in divElement.children:
            tempStr = tempStr + str(child)
        if tempStr == "" :
            tempStr = divElement.string
        try:
            sentenceArr.append(Sentence(tempStr.replace("\xa0", " "), divElement.next_sibling.string.replace("\xa0", " ")))
        except:
            print(tempStr)
            print(divElement.next_sibling.string)

    myFile = open('test.txt', 'a')
    for sent in sentenceArr:
        myFile.write(sent.en + " | " + sent.cn + "\r\n")
    myFile.close()

for link in links:
    writeLinkContentToFile("https://en.hujiang.com"+link)
