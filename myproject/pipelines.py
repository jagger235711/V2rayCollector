import logging
import os
import shutil
from datetime import datetime

class ProxyPipeline:
    def open_spider(self, spider):
        # 判断是否在 GitHub Actions 环境中
        IS_GITHUB_ACTIONS = os.environ.get('GITHUB_ACTIONS') == 'true'

        if IS_GITHUB_ACTIONS:
            # GitHub Actions 路径
            self.results_dir = os.path.dirname(os.path.abspath(__file__))+'/results'    
        else:
            # 本地开发路径
            self.results_dir = '../results'
        
        
        # 每次都新建results目录
        logging.info("results_dir:"+ self.results_dir)
        shutil.rmtree(self.results_dir,ignore_errors=True)
        os.makedirs(self.results_dir)
        
        # 初始化各协议文件
        self.protocol_files = {
            'vmess': open(f'{self.results_dir}/vmess.txt', 'a'),
            'vless': open(f'{self.results_dir}/vless.txt', 'a'),
            'ss': open(f'{self.results_dir}/ss.txt', 'a'),
            'trojan': open(f'{self.results_dir}/trojan.txt', 'a'),
            'hysteria2': open(f'{self.results_dir}/hysteria2.txt', 'a'),
            'mixed': open(f'{self.results_dir}/mixed.txt', 'a')
        }

    def close_spider(self, spider):
        # 关闭所有文件
        for file in self.protocol_files.values():
            file.close()

    def process_item(self, item, spider):
        # 写入对应协议文件
        config = item['config'] + '\n'
        self.protocol_files[item['type']].write(config)
        self.protocol_files['mixed'].write(config)
        return item
