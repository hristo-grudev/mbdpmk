import scrapy


class MbdpmkItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
