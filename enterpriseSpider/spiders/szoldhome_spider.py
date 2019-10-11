import scrapy

from enterpriseSpider.items import SZHomeSpiderItem


class SZOldHomeSpider(scrapy.Spider):
    name = "SZOldHomeSpider"

    start_url = 'http://zf.szhome.com/community.html?xzq=0&zone=0&price=0&ord=0&prif=0&prit=0&kwd=&page=%d'

    page_no = 419

    def start_requests(self):
        for i in range(self.page_no):
            yield scrapy.Request(self.start_url % (i + 1), self.parse)

    def parse(self, response):
        lpinfo_divs = response.xpath('//div[@class="lpinfo"]')
        for div in lpinfo_divs:
            item = SZHomeSpiderItem()
            item['name'] = div.xpath('.//a[@class="imgbox"]/@title').extract_first()
            field_address = div.xpath('.//p[@class="mb mb15"]/text()').extract_first()
            split_items = field_address.split('-')
            if len(split_items) > 1:
                item['field'] = split_items[0]
                address = split_items[1]
                if address is not None:
                    address = address.replace('位于', "")
                item['address'] = address
            detail_url = div.xpath('.//a[@class="imgbox"]/@href').extract_first()
            yield scrapy.Request(response.urljoin(detail_url), self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        try:
            developer = response.xpath('//div[@class="xiaoqu f14 fix"]//li[2]/text()').extract_first()
            item['developer'] = developer
            number = response.xpath('//div[@class="xiaoqu f14 fix"]//li[5]/text()').extract_first()
            item['number'] = number
            parking_number = response.xpath('//div[@class="xiaoqu f14 fix"]//li[6]/text()').extract_first()
            if parking_number is None:
                parking_number = response.xpath('//p[contains(text(),"车位数：")]/text()').extract_first()
            if parking_number is not None:
                item['parking_number'] = parking_number.replace("车位数：", "")
            category = response.xpath('//p[contains(text(),"物业类型：")]/text()').extract_first()
            if category is not None:
                item['category'] = category.replace("物业类型：", "")
        finally:
            yield item
