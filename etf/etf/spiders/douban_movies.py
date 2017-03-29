from scrapy import Spider, Request, Selector
from ..utils import query_params, gen_request_uuid
import json, time, scrapy, logging

class DoubanMovies(Spider):
    is_finished = 0
    name = 'douban-movies'
    allowed_domain = ["douban.com"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    headers = {'User-Agent': user_agent,'Referer': 'https://movie.douban.com/explore'}
    page_limit = 20
    start_list = []
    for i in range(0, 50):
        # all https://movie.douban.com/subject_search?start=0&search_text=%E7%94%B5%E5%BD%B1&cat=1002
        # hot
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=' + str(
            i * page_limit)
        start_list.append(url)
    start_urls = start_list

    def start_requests(self):

        for url in self.start_urls:
            if self.is_finished:
                pass
            else:
                yield Request(url=url, headers=self.headers, method='GET', callback=self.parse,errback=self.requestError)

    def parse(self, response):
        hxs = response.body.decode('utf-8')
        hjson = json.loads(hxs)
        if hjson['subjects']:
            for item in hjson['subjects']:
                item_result = {
                    'request_id': gen_request_uuid(),
                    'douban_id': item['id'],
                    'title': item['title'],
                    'detail_url': item['url'],
                    'score': item['rate'],
                    'cover': item['cover'],
                    'create_at': int(time.time())
                }
                # next_url = 'https://movie.douban.com/subject/26630781/'
                next_url = item_result['detail_url']+'?tag=%E7%83%AD%E9%97%A8&from=gaia'
                result = {
                    'item_type': 'douban_movie_item',
                    'item_data': item_result
                }

                yield Request(url=next_url,headers=self.headers,method='GET',meta={"item":result},callback=self.parseDetail,errback=self.requestError)
                # break
        else:
            self.is_finished = 1

    def parseDetail(self,response):
        item = response.meta['item']
        selector = Selector(response)
        xp = '// *[ @ id = "link-report"] / span[1]'
        # xp = '//*[@id="link-report"]/span[1]/text()'
        span_inner = selector.xpath(xp)
        for inner in span_inner:
            format1 = inner.xpath('span')
            if format1:
                item['item_data']['summary'] = '\n'.join((i.strip())for i in format1.xpath('text()').extract())
            else:
                format2 = inner.xpath('text()')
                item['item_data']['summary'] = format2.extract_first().strip()
        return item

    def requestError(self,response):
        # body = response.body
        pass

