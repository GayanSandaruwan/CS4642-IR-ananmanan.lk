import scrapy

class MoeSpider(scrapy.Spider):
    name = 'moespider'
    start_urls = ['http://www.moe.gov.lk/english/index.php']

    def parse(self, response):
        for province in response.css('ul.megamenue-level1'):
            yield {
		'province': province.xpath('li/a/text()').extract_first()
		}

        #for next_page in response.css('div.prev-post > a'):
        #    yield response.follow(next_page, self.parse)
