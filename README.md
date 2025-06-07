# V2rayCollector - V2ray订阅收集与转换工具

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/username/V2rayCollector/Collector.yml)
![GitHub License](https://img.shields.io/github/license/username/V2rayCollector)

## 项目简介

V2rayCollector 是一个自动化工具，用于从 Telegram 频道抓取 V2ray 节点配置，并从订阅链接汇总节点信息。项目主要功能包括：

- 自动爬取 Telegram 频道中的节点分享信息
- 支持多种订阅链接格式的解析
- 节点去重与有效性检测
- 自动转换为多种客户端配置格式
- 定期自动更新节点列表

### 支持节点类型

| 节点类型       | 支持状态 | 备注                     |
|----------------|----------|--------------------------|
| VLESS          | ✅        | 支持XTLS等高级功能       |
| VMESS          | ✅        | 支持AEAD加密             |
| Shadowsocks    | ✅        | 支持多种加密方式         |
| ShadowsocksR   | ✅        |                          |
| Trojan         | ✅        | 支持TLS 1.3              |
| Hysteria2      | ✅        | 新一代QUIC协议           |

## 快速开始

### 环境要求

- Python 3.8+

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/username/V2rayCollector.git
cd V2rayCollector
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```


## 项目结构

```
V2rayCollector/
├── .github/workflows/    # GitHub Actions工作流配置
│   └── Collector.yml     # 自动收集节点的工作流
├── myproject/            # 爬虫项目目录
│   ├── spiders/          # Scrapy爬虫
│   ├── pipelines.py      # 数据处理管道
│   └── settings.py       # 爬虫配置
├── resource/             # 资源文件
│   ├── channels.csv      # Telegram频道列表
│   └── subList.csv       # 订阅链接列表
├── results/              # 生成结果
│   ├── mixed_tested.json # 测试通过的节点(JSON)
│   └── ...               # 其他格式结果文件
├── tool/                 # 工具目录
│   ├── subconverter/     # 订阅转换工具
│   └── speedTest_singtools/ # 节点测速工具
└── README.md             # 项目文档
```

## 使用方法

### 1. 收集节点

运行爬虫收集Telegram频道中的节点：
```bash
cd myproject
scrapy crawl telegram_crawler
```

### 2. 测试节点速度

使用sing-box工具测试节点速度：
```bash
./tool/speedTest_singtools/singtools -c ./tool/speedTest_singtools/config.json
```

### 3. 转换订阅格式

使用subconverter转换订阅格式：
```bash
./tool/subconverter/subconverter -g --config ./tool/subconverter/generate.ini
```

## 配置文件说明

### channels.csv 格式
```
channel_url,[废弃字段]
https://t.me/sample_channel,false
```

### subList.csv 格式
```
url
https://example.com/subscribe
```

## 结果文件

生成的结果文件位于`results/`目录下：

- `mixed.txt`: 原始混合节点列表
- `mixed_tested.txt`: 测试通过的节点列表
- `mixed_tested.json`: 测试通过的节点(JSON格式)
- 按协议分类的节点文件(vmess.txt, vless.txt等)

## GitHub Actions 自动化

项目配置了GitHub Actions工作流，每天自动运行：

1. 从Telegram频道收集新节点
2. 测试节点有效性
3. 转换订阅格式
4. 提交更新到仓库

## 贡献指南

欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork 本项目
2. 创建您的分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

请确保您的代码符合PEP 8风格指南，并添加适当的测试。

## 致谢

- [subconverter](https://github.com/asdlokj1qpi233/subconverter) - 订阅格式转换工具
- [singtools](https://github.com/Kdwkakcs/singtools) - 基于sing-box的节点测试工具
- [V2rayCollector](https://github.com/mrvcoder/V2rayCollector) - 原始项目灵感来源

## 许可证

本项目采用 [MIT License](LICENSE) 开源。
