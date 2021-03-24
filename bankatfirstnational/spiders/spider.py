import scrapy

from scrapy.loader import ItemLoader

from ..items import BankatfirstnationalItem
from itemloaders.processors import TakeFirst


class BankatfirstnationalSpider(scrapy.Spider):
	name = 'bankatfirstnational'
	start_urls = ['https://www.bankatfirstnational.com/About-Us/Press-Releases/']

	def parse(self, response):
		post_links = response.xpath('//h2[@class="h3"]/a/@href').getall()
		print(len(post_links))
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		print(response)
		title = response.xpath('//div[@class="bodyCopy"]/h1/text()').get()
		description = response.xpath('//div[@class="bodyCopy"]//text()[normalize-space() and not(ancestor::h1 | ancestor::strong[contains(text(), "Release date")])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//strong[contains(text(), "Release date")]/text()').get()[13:]

		item = ItemLoader(item=BankatfirstnationalItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
