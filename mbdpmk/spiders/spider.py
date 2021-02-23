import scrapy

from scrapy.loader import ItemLoader
from ..items import MbdpmkItem
from itemloaders.processors import TakeFirst


class MbdpmkSpider(scrapy.Spider):
	name = 'mbdpmk'
	start_urls = ['https://www.mbdp.com.mk/mk/arhiva-na-vesti']

	def parse(self, response):
		post_links = response.xpath('//a[@itemprop="url"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Следно"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@itemprop="articleBody"]//text()[normalize-space() and not(ancestor::p[@style])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = title

		item = ItemLoader(item=MbdpmkItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
