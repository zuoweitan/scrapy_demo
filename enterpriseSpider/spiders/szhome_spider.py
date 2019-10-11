import scrapy

from enterpriseSpider.items import SZHomeSpiderItem


class SZHomeSpider(scrapy.Spider):
    name = "SZHomeSpider"

    start_url = 'http://bol.szhome.com/search.html?xzq=0&zone=0&dtyx=0&dtst=0&price=0&hx=0&xszt=0&ord=0&prif=0&prit=0' \
                '&kwd=&page=%d'

    page_no = 1

    def start_requests(self):
        for i in range(self.page_no):
            yield scrapy.Request(self.start_url % (i + 1), self.parse)

    def parse(self, response):
        lpinfo_divs = response.xpath('//div[@class="lpinfo"]')
        for div in lpinfo_divs:
            item = SZHomeSpiderItem()
            item['name'] = div.xpath('.//a[@class="imgbox"]/@title').extract_first()
            field_address = div.xpath('.//div[@class="address"]/p/text()').extract_first()
            split_items = field_address.split('-')
            if len(split_items) > 1:
                item['field'] = split_items[0]
                address = split_items[1]
                if address is not None:
                    address = address.replace('位于', "")
                item['address'] = address
            detail_url = div.xpath('.//a[@class="imgbox"]/@href').extract_first()
            yield scrapy.Request(response.urljoin(detail_url), self.parse_detail,  meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        dl = response.xpath('//dl[@class="midinfo"]//dd')
        for index, dd in enumerate(dl):
            if index == 1:
                parking_number = dd.xpath('./text()').extract_first()
                if parking_number is not None:
                    parking_number = parking_number.replace('车位数：', "")
                item['parking_number'] = parking_number
                dd_info = dd.xpath('.//span/text()').extract()
                if len(dd_info) > 1:
                    category = dd_info[0]
                    if category is not None:
                        category = category.replace('类型：', "")
                    item['category'] = category
                    number = dd_info[1]
                    if number is not None:
                        number = number.replace('总房源：', "")
                    item['number'] = number
            if index == 2:
                developer = dd.xpath('./text()').extract_first()
                if developer is not None:
                    developer = developer.replace('开发商：', "")
                item['developer'] = developer
        yield item
