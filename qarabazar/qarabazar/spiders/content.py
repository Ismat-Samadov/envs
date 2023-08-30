import scrapy


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["qarabazar.az"]
    start_urls = [
        "https://qarabazar.az/Obyekt-icareye-verilir-160kv-1-9-Hezi-Aslanovda-adv149786.html"]

    def parse(self, response):
        yield {
            'name': response.css('td.name_adder span[itemprop="name"]::text').get(),
            'category': response.css('.name_adder span[style="color: #777"]::text').get(),
            'number': response.css('span[itemprop="telephone"]::text').get()
        }
