import scrapy
import json

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(AuthorsSpider, self).__init__(*args, **kwargs)
        self.processed_authors = set()
        self.data = []

    def parse(self, response):
        # Follow links to author pages
        author_links = response.css('span small.author ~ a::attr(href)').getall()
        for author_link in author_links:
            yield response.follow(author_link, self.parse_author)
    
        next_link = response.css('li.next a::attr(href)').get()
        if next_link:
            yield response.follow(next_link, self.parse)

    def parse_author(self, response):
        author_name = response.css('h3.author-title::text').get()
        author_birthdate = response.css('span.author-born-date::text').get()
        author_birthplace = response.css('span.author-born-location::text').get()
        author_bio = response.css('div.author-description::text').get()

        if author_name and author_name not in self.processed_authors:
            self.processed_authors.add(author_name)
            description = ''.join(map(str.strip, filter(None, author_bio.splitlines())))
            author_data = {
                "fullname": author_name.strip(),
                "born_date": author_birthdate.strip(),
                "born_location": author_birthplace.strip(),
                "description": description.strip()
            }
            self.data.append(author_data)

    def closed(self, reason):
        with open('authors.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4)
        
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
