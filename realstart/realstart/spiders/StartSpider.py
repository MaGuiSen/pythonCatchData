import scrapy


class QuotesSpider(scrapy.Spider):
    name = "baidu"

    def start_requests(self):
        urls = [
            'http://ilitary.china.com/important/11132797/20170404/30387049.html',
            # 'http://news.china.com/socialgd/10000169/20170405/30388618.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log('Saved fileddddddddddddddddddddddddddddddddddddddd')
