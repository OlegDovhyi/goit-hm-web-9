import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']
    quotes = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_data = {
                'tags': quote.css('div.tags a.tag::text').getall(),
                'author': quote.css('span small.author::text').get(),
                'quote': quote.css('span.text::text').get(),
            }
            self.quotes.append(quote_data)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            self.save_to_json()

    def save_to_json(self):
        with open('quotes.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.quotes, json_file, ensure_ascii=False, indent=4)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
