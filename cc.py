# # -*- coding: UTF-8 -*-
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
#
# body = '''
#     <tbody><tr>
#         <td>
#           <strong>中文名：</strong>
#           <span>刘德华</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>英文名：</strong>
#           <span>Andy Lau,Lau Tak Wah</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>其它外文名：</strong>
#           <span>Lau TAK Wah</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>别名：</strong>
#           <span>华仔，老大，华哥，华Dee，刘天王，华神，刘主席</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>性别：</strong>
#           <span>男</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>出生年月：</strong>
#           <span>
#             <a title="" href=""></a><a href="http://www.baike.com/wiki/1961%E5%B9%B49%E6%9C%8827%E6%97%A5" target="_blank">1961年9月27日</a>
#           </span>
#         </td> </tr> <tr>
#         <td>
#           <strong>国籍：</strong>
#           <span><a href="http://www.baike.com/wiki/%E4%B8%AD%E5%9B%BD" title="中国" target="_blank"><img src="http://www.huimg.cn/datamodule/flagicon/22/chn.png"></a>中国</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>籍贯：</strong>
#           <span>广东<a href="http://www.baike.com/wiki/%E6%96%B0%E4%BC%9A" target="_blank">新会</a></span>
#         </td> </tr> <tr>
#         <td>
#           <strong>出生地：</strong>
#           <span>香港新界大埔镇泰亨村</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>民族：</strong>
#           <span>汉族</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>毕业院校：</strong>
#           <span>可立中学，第十期无线艺员培训班</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>身高：</strong>
#           <span>174cm</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>宗教信仰：</strong>
#           <span>佛教</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>体重：</strong>
#           <span>63kg</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>职业：</strong>
#           <span>演员、歌手、填词人、电影人</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>音乐代表作品：</strong>
#           <span><a href="http://www.baike.com/wiki/%E5%BF%98%E6%83%85%E6%B0%B4" target="_blank">忘情水</a>、<a href="http://www.baike.com/wiki/%E5%86%B0%E9%9B%A8" target="_blank">冰雨</a>、<a href="http://www.baike.com/wiki/%E7%BB%83%E4%B9%A0" target="_blank">练习</a>、<a href="http://www.baike.com/wiki/%E4%B8%AD%E5%9B%BD%E4%BA%BA" target="_blank">中国人</a>、<a href="http://www.baike.com/wiki/%E7%AC%A8%E5%B0%8F%E5%AD%A9" target="_blank">笨小孩</a></span>
#         </td> </tr> <tr>
#         <td>
#           <strong>音乐类型：</strong>
#           <span>流行音乐</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>影视代表作品：</strong>
#           <span><a href="http://www.baike.com/wiki/%E6%9A%97%E6%88%98" target="_blank">暗战</a>、<a href="http://www.baike.com/wiki/%E6%97%A0%E9%97%B4%E9%81%93" target="_blank">无间道</a>、<a href="http://www.baike.com/wiki/%E7%9B%B2%E6%8E%A2" target="_blank">盲探</a>、<a href="http://www.baike.com/wiki/%E5%A4%A9%E8%8B%A5%E6%9C%89%E6%83%85" target="_blank">天若有情</a>等</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>出道地区：</strong>
#           <span>香港</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>活跃年代：</strong>
#           <span>上世纪80年代至今</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>经纪公司：</strong>
#           <span>东亚唱片、映艺娱乐</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>星座：</strong>
#           <span>天秤座</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>血型：</strong>
#           <span>AB型</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>爱好：</strong>
#           <span><a href="http://www.baike.com/wiki/%E4%BF%9D%E9%BE%84%E7%90%83" target="_blank">保龄球</a>、羽毛球、台球、驾驶</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>特长：</strong>
#           <span>唱歌、跳舞、拍戏</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>其他信息：</strong>
#           <span>第一部书:《浓情爱不完》；自传体散文集《我是这样长大的》</span>
#         </td> </tr>
#       </tbody>
#       <tbody><tr>
#         <td>
#           <strong>姓名：</strong>
#           <span>孔丘</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>别称：</strong>
#           <span>孔子，尼父，孔夫子</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>字号：</strong>
#           <span>仲尼</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>所处时代：</strong>
#           <span>东周春秋末期</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>民族族群：</strong>
#           <span>华夏族</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>出生地：</strong>
#           <span>鲁国陬邑（今山东曲阜）</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>出生时间：</strong>
#           <span>公元前551年9月28日</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>去世时间：</strong>
#           <span>公元前479年4月11日</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>主要作品：</strong>
#           <span>《六经》，《春秋》</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>主要成就：</strong>
#           <span>开创儒学，编纂《春秋》，修订《六经》，创办私学</span>
#         </td> </tr>
#       </tbody>
#       <tbody><tr>
#         <td>
#           <strong>中文名：</strong>
#           <span>奥巴马</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>其它外文名：</strong>
#           <span>Barack Hussein Obama II</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>别名：</strong>
#           <span>巴拉克·欧巴马</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>性别：</strong>
#           <span>男</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>出生年月：</strong>
#           <span>
#             <a title="" href=""></a><a href="http://www.baike.com/wiki/1961%E5%B9%B48%E6%9C%884%E6%97%A5" target="_blank">1961年8月4日</a>
#           </span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>国籍：</strong>
#           <span>美国</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>民族：</strong>
#           <span>非裔美国人</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>毕业院校：</strong>
#           <span>哥伦比亚大学、哈佛大学</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>宗教信仰：</strong>
#           <span>基督新教</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>政党：</strong>
#           <span>美国民主党</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>职位：</strong>
#           <span>第44任美国总统（第56~57届）</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>在职时间：</strong>
#           <span>8年</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>第一夫人：</strong>
#           <span>米歇尔·拉沃恩·奥巴马</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>主要事件：</strong>
#           <span>时代周刊年度风云人物</span>
#           <span>任期内清除本·拉登</span>
#           <span>第44任美国总统</span>
#         </td> </tr>
#       </tbody>
#       <tbody><tr>
#         <td>
#           <strong>中文名：</strong>
#           <span>习近平</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>籍贯：</strong>
#           <span><a href="http://www.baike.com/wiki/%E9%99%95%E8%A5%BF%E5%AF%8C%E5%B9%B3" target="_blank">陕西富平</a>人</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>民族：</strong>
#           <span>汉</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>国籍：</strong>
#           <span><a href="http://www.baike.com/wiki/%E4%B8%AD%E5%9B%BD" title="中国" target="_blank"><img src="http://www.huimg.cn/datamodule/flagicon/22/chn.png"></a>中国</span>
#         </td> </tr> <tr>
#         <td>
#           <strong>职业：</strong>
#           <span>政治家</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>毕业院校：</strong>
#           <span><a href="http://www.baike.com/wiki/%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6" target="_blank">清华大学</a></span>
#         </td> </tr> <tr>
#         <td>
#           <strong>政党：</strong>
#           <span>中国共产党</span>
#         </td>
#         <td class="jg">
#         </td><td>
#           <strong>代表作品：</strong>
#           <span>《之江新语》</span>
#         </td> </tr>
#       </tbody>
# '''
# value = []
# selectors = Selector(text=body)
# contents = selectors.xpath('//strong/text()').extract()
# for ss in contents:
#     if ss in value:
#         continue
#     else:
#         value.append(ss)
# print len(value)
# for ss in value:
#     print ss.replace(u'：', '')
#
# hh = '''
# member
# Record company
# Music Album
# Fan name
# Debut date
# Gain honor
# Team member
# Sport event
# motion state
# Effectiveness Club
# Former club
# Conventional foot
# Field position
# uniform number
# personal honor
# Login height
# Login weight
# Sports team
# Important event
# image
# Moral
# Participation events
# Service unit
# major awards
# Member of family
# Subordinate works
# Debut time
# Residence
# Team honor
# Classic quotations
# partner
# Apprentice
# major
# Retirement time
# Party time
# Interpretation
# Chinese full name
# Full name in English
# Developers
# Publisher
# Issue date
# Former
# Successor
# Name
# father
# succession
# Technical features
# mother
# Abbreviation
# years
# Official position
# parent
# To star
# author
# ability
# companion
# Chinese name
# Chinese alias
# spouse
# The Chinese Zodiac
# I was
# Abdication date
# Affiliated company
# Enemy
# Debut
# Standing time
# Shoe size
# Career high marks
# Name
# Agent
# Role provenance
# Term of office
# Marital status
# Awards
# Political outlook
# Latin name
# Location
# Stage name
# '''
# print hh.lower()
# print hh.replace(u' ', '_').lower()
#
#

# 迭代器
def Fod():
    a = 0
    b = 0
    while a < 2:
        yield b
        b = a + 1
        a += 1
    c = 3
    yield c
    yield Cod()
    print 'ddd'

def Cod():
    d = 44
    return d

for item in Fod():
    print item
print Fod()
print Fod().next()