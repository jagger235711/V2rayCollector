import scrapy

class ProxyItem(scrapy.Item):
    type = scrapy.Field()  # 代理类型: vmess/vless/ss/trojan/hysteria2
    config = scrapy.Field()  # 代理配置
    source = scrapy.Field()  # 来源频道
    timestamp = scrapy.Field()  # 爬取时间戳
