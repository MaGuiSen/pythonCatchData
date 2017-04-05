import scrapy


class QuotesSpider(scrapy.Spider):
    name = "baidu"
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    def start_requests(self):
        urls = [
            'http://www1.tuicool.com/articles/jyQF32V',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log('Saved fileddddddddddddddddddddddddddddddddddddddd')