import scrapy
import re
import base64
import json
import time
import pandas as pd
from urllib.parse import urlparse
from ..items import ProxyItem

class TelegramCrawlerSpider(scrapy.Spider):
    name = "telegram_crawler"
    allowed_domains = ["t.me"]
    channelsPath='./resource/channels.csv'
    # start_urls = []  # 通过构造函数传入实际URL
    # 读取csv文件 将第一列转为list
    async def start(self):
        start_urls=pd.read_csv(self.channelsPath, usecols=[0], header=None)[0].tolist()
        for url in start_urls:
            yield scrapy.Request(self.change_url_to_telegram_web_url(url))
    
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'RETRY_TIMES': 3,
        'DOWNLOAD_TIMEOUT': 30,
    }
    seen_configs = set()  # 用于去重

    def __init__(self, config_names="", *args, **kwargs):
        super(TelegramCrawlerSpider, self).__init__(*args, **kwargs)
        self.config_names = config_names
        self.config_ids = {
            'ss': 0,
            'vmess': 0,
            'trojan': 0,
            'vless': 0,
            'hysteria2': 0
        }

    def parse(self, response):
        self.logger.debug(f"Processing URL: {response.url}")
        self.logger.debug(f"Response status: {response.status}")
        self.logger.debug(f"Response headers: {response.headers}")
        
        # 检查页面是否包含有效内容
        if "This channel is private" in response.text:
            self.logger.error("Channel is private, please join the channel first")
            return
        elif "This channel doesn't exist" in response.text:
            self.logger.error("Channel does not exist, please check the URL")
            return
        elif "Cloudflare" in response.text:
            self.logger.error("Blocked by Cloudflare protection")
            return
            
        # 检查是否被重定向
        if response.url != response.request.url:
            self.logger.warning(f"Redirected from {response.request.url} to {response.url}")
            
        # 解析页面内容
        messages = response.css('.tgme_widget_message_text')
        self.logger.info(f"Found {len(messages)} messages on page")
        
        for message in messages:
            text = message.get()
            self.logger.debug(f"Processing message: {text[:100]}...")
            # 提取代理配置
            configs = self.extract_configs(text)
            self.logger.debug(f"Extracted {len(configs)} configs from message")
            
            for config in configs:
                if config['config'] not in self.seen_configs:
                    self.seen_configs.add(config['config'])
                    # 添加配置名称
                    final_config = self.add_config_name(config['config'], config['type'])
                    yield ProxyItem(
                        type=config['type'],
                        config=final_config,
                        source=response.url,
                        timestamp=int(time.time())
                    )

    def add_config_name(self, config, config_type):
        """添加配置名称，类似go的AddConfigNames函数"""
        if not self.config_names:
            return config    
        # 其他协议直接追加名称
        self.config_ids[config_type] += 1
        return f"{config}{self.config_names} - {self.config_ids[config_type]}"

    def extract_configs(self, text):
        configs = []
        # 使用go的正则表达式模式
        # pattern_telegram_user = r'(?:@)(\w{4,})'
        # pattern_url = r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))'
        # pattern_shadowsocks = r"(?<![\w-])(ss://[^\s<>#]+)"
        # pattern_trojan = r"(?<![\w-])(trojan://[^\s<>#]+)"
        # pattern_vmess = r"(?<![\w-])(vmess://[^\s<>#]+)"
        # pattern_vless = r"(?<![\w-])(vless://(?:(?!=reality)[^\s<>#])+(?=[\s<>#]))"
        # pattern_reality = r"(?<![\w-])(vless://[^\s<>#]+?security=reality[^\s<>#]*)"
        # pattern_tuic = r"(?<![\w-])(tuic://[^\s<>#]+)"
        # pattern_hysteria = r"(?<![\w-])(hysteria://[^\s<>#]+)"
        # pattern_hysteria_ver2 = r"(?<![\w-])(hy2://[^\s<>#]+)"
        # pattern_juicity = r"(?<![\w-])(juicity://[^\s<>#]+)"
        regex_patterns = {
            # 'ss': r'(?m)(?<![\w-])(ss://[^\s<>#]+)',#直接放弃ss节点，可用概率较低
            'vmess': r'(?m)(?<![\w-])(vmess://[^\s<>#]+)',
            'trojan': r'(?m)(?<![\w-])(trojan://[^\s<>#]+)',
            'vless': r'(?m)(?<![\w-])(vless://(?:(?!=reality)[^\s<>#])+(?=[\s<>#]))',
            'hysteria2': r'(?m)(?<![\w-])(hysteria2://[^\s<>#]+)'
        }
   

        # 实现类似go的ExtractConfig逻辑
        for proto, pattern in regex_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):  # 处理分组匹配
                    match = match[0]
                # 排除长度小于20的匹配
                if len(match) < 20:
                    continue
                
                config = match
                configs.append({'type': proto, 'config': config})
                
        return configs
   
    def change_url_to_telegram_web_url(self,input_str):
        if '/s/' not in input_str:
            index = input_str.find('/t.me/')
            if index != -1:
                modified_url = input_str[:index + len('/t.me/')] + 's/' + input_str[index + len('/t.me/'):]
                return modified_url
        return input_str    