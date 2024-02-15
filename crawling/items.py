from scrapy.item import Item, Field

class AllInfoItem(Item):
    title = Field()
    content = Field()
    links = Field()
    url = Field()

class URLItem(Item):
    url = Field()