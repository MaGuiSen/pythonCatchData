# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import re
import pymysql
from channel import channel   #这是我们第一个程序爬取的链接信息
import random

# 循环遍历请求到界面，然后解析
#这是上面的那个测试函数，我们把它放在主函数中
def mains(url):
    pass
    wb_data = requests.get("https://book.douban.com/subject/1007305/")
    soup = BeautifulSoup(wb_data.text.encode("utf-8"), "lxml")
    tag = url.split("?")[0].split("/")[-1]
    main_info = soup.select("div.grid-16-8 #info")#主要的信息
    img_douban = soup.select("div.grid-16-8 #mainpic a.nbg img")#图片
    # 根据图片进行下载
    score = soup.select("div.grid-16-8 div.rating_wrap ")  #评分
    mulus = soup.select("div.grid-16-8 #dir_"+str(1007305)+"_full")#1154707当前的图书的id  目录
    tags = soup.select("div.grid-16-8 a.tag ")
    if mulus:
        mulus = mulus[0]
        print (mulus.get_text(",").replace(u"· · · · · ·     (,收起,)",""))
        print ("---------------------------")

    if tags:
        tagList =[]
        for tag in tags:
            tagList.append(tag.get_text())
        print (','.join(tagList))
        print ("---------------------------")

    # 内容简介 (1)内容不多 #link-report > div.intro （2）内容多  #link-report > span.all > div.intro
    neirongjianjie = soup.select("div.grid-16-8 #link-report")
    if neirongjianjie :
        #先判断是否存在#link-report > span.all > div.intro 如果不存在则调用 #link-report > div.intro
        neirongjianjie = neirongjianjie[0]
        neirongDetail = neirongjianjie.select("span.all  div.intro p")
        endDetails = []
        if neirongDetail:
            for detail in neirongDetail:
                endDetails.append(detail.get_text())
        else:
            neirongDetail = neirongjianjie.select("div.intro p")
            for detail in neirongDetail:
                endDetails.append(detail.get_text())
        neirongDetail = "\n".join(endDetails)
        print (neirongDetail)

    # 内容简介 (1)内容不多 #link-report > div.intro （2）内容多  #link-report > span.all > div.intro
    zuozhejianjie = soup.find("span", text=["作者简介"]).parent
    if zuozhejianjie:
        zuozhejianjie = zuozhejianjie.findNextSibling()
        if zuozhejianjie:
            zuozheDetail = zuozhejianjie.select("span.all  div.intro p")
            endDetails = []
            if zuozheDetail:
                for detail in zuozheDetail:
                    endDetails.append(detail.get_text())
            else:
                zuozheDetail = zuozhejianjie.select("div.intro p")
                for detail in zuozheDetail:
                    endDetails.append(detail.get_text())
            zuozheDetail = "\n".join(endDetails)
            print ("---------------------------")
            print (zuozheDetail)

    #丛书信息
    congshuxinxi = soup.find_all("h2", text=["丛书信息"])

mains('')
# start = time.clock()   #设置一个时钟，这样我们就能知道我们爬取了多长时间了
# i = 0
# for urls in channel.split():
#     pass
#     i += 1
#     if i > 10:
#         break
#     。urlss=[urls+"?start={}&type=T".format(str(i)) for i in range(0,980,20)]   #从channel中提取url信息，并组装成每一页的链接
#     for url in urlss:
#         mains(url)  # 执行主函数，开始爬取
#         print(url)  # 输出要爬取的链接，这样我们就能知道爬到哪了，发生错误也好处理
#         time.sleep(int(format(random.randint(0, 15))))  # 设置一个随机数时间，每爬一个网页可以随机的停一段时间，防止IP被封
# end = time.clock()
# print('Time Usage:', end - start)    #爬取结束，输出爬取时间
