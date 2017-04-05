    def parseContent(self,content):
        return (author,board,time)
    #content = content[timeIndex+58:]
    #return (author,board,time,content)
    def parse2(self,response):
        hxs =HtmlXPathSelector(response)
        item = response.meta['item']
        items = []
        content = hxs.select('/html/body/center/table[1]/tr[2]/td/textarea/text()').extract()
        parseTuple = self.parseContent(content)
        item['author'] = parseTuple[0].decode('utf-8')
        item['board'] =parseTuple[1].decode('utf-8')
        item['time'] = parseTuple[2]
        #item['content'] = parseTuple[3]
        items.append(item)
        return items
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        title= hxs.select('/html/body/center/table/tr[position()>1]/td[3]/a/text()').extract()
        url= hxs.select('/html/body/center/table/tr[position()>1]/td[3]/a/@href').extract()
        for i in range(0, 10):
            item = bbsItem()
            item['link'] = urljoin_rfc('http://bbs.nju.edu.cn/', url[i])
            item['title'] = title[i][:]
            items.append(item)
        for item in items:
            yield Request(item['link'],meta={'item':item},callback=self.parse2)
        yield items