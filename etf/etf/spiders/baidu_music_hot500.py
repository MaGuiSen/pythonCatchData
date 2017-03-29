from scrapy import Selector, Request, Spider
from ..utils import query_params, gen_request_uuid
from scrapy.exceptions import CloseSpider
import json, time, scrapy, logging


class BaiduMusicHot500(Spider):
    name = 'baidu-music-hot500'
    allowed_domain = ["hkcna.hk"]
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    headers = {'User-Agent': user_agent}

    start_urls = [
        'http://music.baidu.com/top/dayhot'
    ]

    def parse(self, response):
        sel = Selector(response)
        info = sel.xpath('//div[@class="song-item"]')
        if len(info) == 0:
            raise CloseSpider('---------------------End Search!---------------')

        i = 1
        result = []
        for item in info:
            title = item.xpath('span[@class="song-title "]/a/text()').extract_first().encode('utf-8')
            author = item.xpath('span[@class="singer"]/span[1]/@title').extract_first().encode('utf-8')
            detail_url = item.xpath('span[@class="song-title "]/a/@href').extract_first().encode('utf-8')
            detail_url = detail_url if detail_url.startswith('http') else 'http://music.baidu.com' + detail_url
            cover = item.xpath('span[@class="songlist-album-cover"]/a[1]/img/@src').extract_first().encode(
                'utf-8') if item.xpath('span[@class="songlist-album-cover"]/a[1]/img/@src') else ''

            music_item = {
                'id': i,
                'title': title,
                'author': author,
                'detail_url': detail_url,
                'cover': cover,
                'create_at': int(time.time())
            }
            i += 1
            result.append(music_item)

        yield {
            'item_type': 'baidu_music_hot500',
            'item_list': result
        }
