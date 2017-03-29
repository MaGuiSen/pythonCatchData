from scrapy import Spider, Request, Selector
from ..utils import query_params, gen_request_uuid
from scrapy.exceptions import CloseSpider
import json, time, scrapy, logging


class DoubanNovel(Spider):
    is_finished = 0
    name = 'douban-novel'
    allowed_domain = ["book.douban.com"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page_limit = 20
    start_urls = [
        'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=0&type=T'
    ]

    def start_requests(self):

        for url in self.start_urls:
            if self.is_finished:
                pass
            else:
                yield Request(url=url, headers=self.headers, method='GET', callback=self.parse,
                              errback=self.requestError)

    def parse(self, response):
        books = []
        sel = Selector(response)
        info = sel.xpath('//li[@class="subject-item"]')
        if len(info) == 0:
            raise CloseSpider('---------------------End Search!---------------')

        for subject_item in info:
            cover = subject_item.xpath('div[1]/a/img/@src').extract()[0]
            site = subject_item.xpath('div[@class="info"]')[0]
            pub = site.xpath('div[@class="pub"]/text()').extract()[0].encode('utf-8')
            score = site.xpath('div[2]/span[2]/text()').extract_first()
            pub = pub.strip().split('/')
            book = {
                'title': site.xpath('h2/a/@title').extract()[0].encode('utf-8'),
                'detail_url': site.xpath('h2/a/@href').extract()[0].encode('utf-8'),
                'author': pub[0],
                'price': pub[-1],
                'cover': cover,
                'create_at': int(time.time()),
                'score': score
            }
            summary = site.xpath('p/text()').extract()
            book['summary'] = summary[0].encode('utf-8') if (len(summary) != 0) else ''
            book['douban_id'] = book['detail_url'].split('/')[-2]
            books.append(book);
            yield {
                    'item_type': 'douban_novel_item',
                    'item_data': book
                }
        time.sleep(3)
        site = sel.xpath('//span[@class="next"]/a/@href').extract()[0]
        temp = response.url.split('/')
        new_url = temp[0]
        i = 1
        while i < len(temp) - 2:
            new_url += '/' + temp[i]
            i += 1
        new_url += site
        new_url = new_url.encode('utf-8')
        yield scrapy.Request(new_url, callback=self.parse)

    def requestError(self, response):
        # body = response.body
        pass
