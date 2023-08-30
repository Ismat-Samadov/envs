import scrapy


class CombinedSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["qarabazar.az"]
    start_urls = [
        "https://qarabazar.az/searchadv/?text_search=&spage=1&scat=-1&s_adv_country=-1&s_adv_region=0&s_adv_city=0&s_min_cost=&s_max_cost=&s_currency=azn"]

    def parse(self, response):
        # Extract links and follow them
        for href in response.css('a.title_synopsis_adv::attr(href)').getall():
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_content)

        # Follow pagination link for next page (Unicode character "»")
        next_page = response.xpath('//a[span[@class="pageoff"] and span[text()="»"]]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_content(self, response):
        yield {
            'link': response.url,
            'name': response.css('td.name_adder span[itemprop="name"]::text').get(),
            'category': response.css('.name_adder span[style="color: #777"]::text').get(),
            'number': response.css('span[itemprop="telephone"]::text').get(),
        }
