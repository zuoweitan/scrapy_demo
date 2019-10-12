import scrapy

from enterpriseSpider.items import SZHomeSpiderItem


class SZQFangHomeSpider(scrapy.Spider):
    name = "SZQFangHomeSpider"

    start_url = 'https://shenzhen.qfang.com/office/garden/rent/n%d'

    page_no = 25

    def start_requests(self):
        for i in range(self.page_no):
            yield scrapy.Request(self.start_url % (i + 1), self.parse)

    def parse(self, response):
        lpinfo_divs = response.xpath('//div[@class="list-main fl"]')
        for div in lpinfo_divs:
            item = SZHomeSpiderItem()
            item['name'] = div.xpath('.//a[@class="house-title fl"]/text()').extract_first("").replace("\r\n", "").strip()
            field_address = div.xpath('.//p[@class="meta-items"]/text()').extract_first("").replace("\r\n", "").strip()
            split_items = field_address.split('-')
            if len(split_items) > 1:
                item['field'] = split_items[0]
                item['address'] = split_items[1]
            detail_url = div.xpath('.//a[@class="house-title fl"]/@href').extract_first()
            yield scrapy.Request(response.urljoin(detail_url), self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        item['category'] = "写字楼"
        try:
            ul = response.xpath('//ul[@class="arrange-list clearfix"]/li')
            for index, li in enumerate(ul):
                if index == 1:
                    item['parking_number'] = li.xpath('.//div[@class="text"]/text()').extract_first("").replace("个", "")
                if index == 6:
                    item['number'] = li.xpath('.//div[@class="text"]/text()').extract_first("")
                if index == 8:
                    item['developer'] = li.xpath('.//div[@class="text"]/text()').extract_first("")
        finally:
            yield item
