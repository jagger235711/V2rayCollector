import scrapy
import re
import base64
import json
import time
from urllib.parse import urlparse
from ..items import ProxyItem

class TelegramCrawlerSpider(scrapy.Spider):
    name = "telegram_crawler"
    allowed_domains = ["t.me"]
    # start_urls = []  # 通过构造函数传入实际URL
    start_urls = ['https://t.me/s/wxgmrjdcc']  # 通过构造函数传入实际URL
    
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
        regex_patterns = {
            'ss': r'(?m)(...ss:|^ss:)\/\/.+?(%3A%40|#)',
            'vmess': r'(?m)vmess:\/\/[A-Za-z0-9+/=]+',
            'trojan': r'(?m)trojan:\/\/.+?(%3A%40|#)',
            'vless': r'(?m)vless:\/\/.+?(%3A%40|#)',
            'hysteria2': r'(?m)hysteria2:\/\/.+?(%3A%40|#)'
        }
        # regex_patterns = {
        #     # SS协议
        #     'ss': r'(?m)(?:^|[^a-zA-Z0-9])ss:\/\/[A-Za-z0-9+\/=%_-]+(?:@[a-zA-Z0-9_.-]+:[0-9]+)?(?:\?[a-zA-Z0-9%=&_-]+)?(?:#[^\s"\'<>()]+)?',

        #     # VMess协议
        #     'vmess': r'(?m)(?:^|[^a-zA-Z0-9])vmess:\/\/[A-Za-z0-9+\/=_-]+(?=[^\w\/+]|$)',

        #     # Trojan协议
        #     'trojan': r'(?m)(?:^|[^a-zA-Z0-9])trojan:\/\/[^@\s]+@[a-zA-Z0-9_.-]+:[0-9]+(?:\?[a-zA-Z0-9%=&_-]+)?(?:#[^\s"\'<>()]+)?',

        #     # VLESS协议
        #     'vless': r'(?m)(?:^|[^a-zA-Z0-9])vless:\/\/[^@\s]+@[a-zA-Z0-9_.-]+:[0-9]+(?:\?[a-zA-Z0-9%=&_.-]+)?(?:#[^\s"\'<>()]+)?',

        #     # Hysteria2协议
        #     'hysteria2': r'(?m)(?:^|[^a-zA-Z0-9])hysteria2:\/\/[^@\s]+@[a-zA-Z0-9_.-]+:[0-9]+(?:\?[a-zA-Z0-9%=&_.-]+)?(?:#[^\s"\'<>()]+)?'

        # }

        # 实现类似go的ExtractConfig逻辑
        for proto, pattern in regex_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                # 排除长度小于20的匹配
                if len(match) < 20:
                    continue
                if isinstance(match, tuple):  # 处理分组匹配
                    match = match[0]
                
                # 处理ss协议的特殊情况
                if proto == 'ss' and match.startswith('ss://'):
                    prefix = match.split('ss://')[0]
                    if prefix and prefix != 'vle':  # 排除vless误匹配
                        config = f'ss://{match.split("ss://")[1]}'
                        configs.append({'type': proto, 'config': config})
                else:
                    config = match
                    configs.append({'type': proto, 'config': config})

        # 去重处理
        unique_configs = []
        seen = set()
        for config in configs:
            if config['config'] not in seen:
                seen.add(config['config'])
                unique_configs.append(config)
                
        return unique_configs
