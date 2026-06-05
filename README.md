# 🚀 V2rayCollector - 智能节点爬取与测速工具

<div align="center">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/jagger235711/V2rayCollector/Collector.yml)
![GitHub License](https://img.shields.io/github/license/jagger235711/V2rayCollector)
![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![Stars](https://img.shields.io/github/stars/jagger235711/V2rayCollector)

一个全自动化的Telegram频道节点爬虫 + 订阅链接收集 + 节点去重 + 速度测试 + 订阅转换工具

[English](./README.en.md) | 简体中文

</div>

---

## 📋 项目简介

**V2rayCollector** 是一个强大的、全自动化的节点收集和管理工具，集成了爬虫、去重、测速和格式转换等功能。它能够：

- 🕷️ **自动爬取** Telegram频道中的V2ray节点配置
- 🔗 **汇总处理** 来自多个订阅链接的节点
- 🧹 **智能去重** 支持并发检测，排除无效和慢速链接
- ⚡ **高效测速** 使用singtools进行批量节点速度测试
- 🔄 **格式转换** 基于subconverter支持多种订阅格式
- ⏰ **自动更新** 通过GitHub Actions每天定时运行
- 📊 **结果分类** 按协议类型分类输出结果

### ✅ 支持的协议类型

| 协议 | 支持 | 说明 |
|------|------|------|
| **VLESS** | ✅ | 支持Reality等高级功能 |
| **VMESS** | ✅ | 支持AEAD加密 |
| **Trojan** | ✅ | TLS 1.3 & 完整加密 |
| **Hysteria2** | ✅ | 基于QUIC的新一代协议 |
| ~~Shadowsocks~~ | ❌ | 可用性低，已排除 |

---

## 🏗️ 项目架构

```
输入来源
├─ Telegram频道 (channels.csv)
└─ 订阅链接 (subList.csv)
    │
    ▼
[1] URL有效性检测 (deduplicate.py)
    - 并发检测 (10个线程)
    - 超时检测 (5秒)
    - 慢速检测 (>1秒)
    │
    ▼
[2] Telegram爬虫 (Scrapy + telegram_crawler.py)
    - 正则提取配置
    - 自动去重
    - 协议分类 (VLESS/VMESS/Trojan/Hysteria2)
    │
    ▼
[3] 订阅处理 (subconverter Docker)
    - 批量处理订阅链接
    - 并发请求 (5个并发)
    - 重试机制 (3次重试)
    - Base64编码
    │
    ▼
[4] 合并与去重
    - 混合所有来源节点
    - 清理空行和格式
    │
    ▼
[5] 节点测速 (singtools)
    - 并发测速
    - 输出JSON结果
    │
    ▼
输出结果 (results/)
├─ mixed.txt              # 原始混合节点
├─ mixed_tested.json      # 测速结果(JSON)
├─ mixed_tested.txt       # 测速后节点
├─ vmess.txt/vless.txt    # 按协议分类
└─ *.bak                  # 备份文件
```

---

## 📦 项目结构

```
V2rayCollector/
├── .github/
│   └── workflows/
│       └── Collector.yml              # ⭐ GitHub Actions自动化工作流
│
├── myproject/                         # Scrapy爬虫项目
│   ├── spiders/
│   │   └── telegram_crawler.py        # Telegram频道爬虫核心
│   ├── items.py                       # 数据模型定义
│   ├── pipelines.py                   # 数据处理管道
│   ├── settings.py                    # 爬虫配置
│   └── middlewares.py                 # 请求中间件
│
├── resource/                          # 配置资源文件
│   ├── channels.csv                   # Telegram频道列表
│   └── subList.csv                    # 订阅链接列表
│
├── results/                           # 输出结果目录
│   ├── mixed.txt                      # 混合节点列表
│   ├── mixed_tested.json              # 测速结果
│   ├── vmess.txt / vless.txt / ...    # 按协议分类
│   └── *.bak                          # 备份文件
│
├── tool/                              # 第三方工具
│   ├── speedTest_singtools/           # singtools测速工具
│   │   ├── singtools                  # 可执行文件
│   │   └── config.json                # 测速配置
│   └── (subconverter运行在Docker中)
│
├── deduplicate.py                     # 🔑 URL去重工具
├── main.py                            # 主程序入口
├── pyproject.toml                     # 项目配置
├── requirements.txt                   # Python依赖
├── scrapy.cfg                         # Scrapy配置
└── README.md                          # 项目文档
```

---

## 🚀 快速开始

### 环境要求

- **Python** 3.13+
- **Docker** (用于subconverter)
- **Git** (可选，用于版本控制)

### 安装步骤

#### 1️⃣ 克隆仓库
```bash
git clone https://github.com/jagger235711/V2rayCollector.git
cd V2rayCollector
```

#### 2️⃣ 安装依赖
使用 pip：
```bash
pip install -r requirements.txt
```

或使用 uv (更快)：
```bash
uv pip install -r requirements.txt
```

#### 3️⃣ 配置输入资源

编辑 `resource/channels.csv`，添加Telegram频道：
```csv
https://t.me/s/channel_name
https://t.me/another_channel
```

编辑 `resource/subList.csv`，添加订阅链接：
```csv
https://example.com/subscribe/user123
https://another.example.com/sub/abc
```

---

## 📖 使用方法

### 方式 1️⃣：本地运行

#### 步骤 1: 去重输入列表
```bash
python deduplicate.py resource/channels.csv resource/channels.csv
python deduplicate.py resource/subList.csv resource/subList.csv
```

#### 步骤 2: 运行Telegram爬虫
```bash
scrapy crawl telegram_crawler
```

#### 步骤 3: 启动subconverter容器
```bash
docker run -d --name subconverter \
  -v $(pwd)/results:/subconverter/results \
  -p 25500:25500 \
  asdlokj1qpi23/subconverter:latest
```

#### 步骤 4: 处理订阅链接
```bash
# 批量请求subconverter API处理订阅链接
# (具体脚本见GitHub Actions工作流)
```

#### 步骤 5: 执行测速
```bash
chmod +x tool/speedTest_singtools/singtools
tool/speedTest_singtools/singtools test \
  -i results/mixed.txt \
  -c tool/speedTest_singtools/config.json \
  -o results/mixed_tested.json
```

### 方式 2️⃣：GitHub Actions自动运行 (推荐)

项目已配置GitHub Actions工作流，自动执行以上所有步骤：

- **触发方式**：
  - ⏰ 每天 **06:00** 和 **18:00** (北京时间 UTC+8)
  - 🎯 或手动触发 workflow_dispatch

- **工作流执行内容**：
  1. 删除过期的Release和Workflows
  2. 清理旧结果目录
  3. 安装Python依赖 (使用pip缓存)
  4. 去重频道列表和订阅链接
  5. 运行Telegram爬虫
  6. 启动subconverter容器并批量处理订阅
  7. Base64解码转换
  8. 执行singtools测速
  9. 生成最终订阅
  10. 提交结果到仓库

---

## 📝 配置文件说明

### resource/channels.csv

Telegram频道配置文件，支持两种URL格式：

```csv
URL
https://t.me/s/channel_name
https://t.me/channel_name
```

每行一个频道URL。爬虫会自动转换为Web版本 (https://t.me/s/...) 用于爬取。

### resource/subList.csv

订阅链接配置文件，包含第三方订阅源：

```csv
URL
https://example.com/subscribe/user123
https://raw.githubusercontent.com/user/repo/main/subscribe
```

每行一个订阅链接。支持base64编码的订阅。

---

## 📤 输出结果说明

运行完成后，`results/` 目录下会生成以下文件：

### 核心输出文件

| 文件 | 说明 | 格式 |
|------|------|------|
| `mixed.txt` | 去重后的所有节点 | 纯文本，每行一个节点 |
| `mixed_tested.json` | 测速后的节点数据 | JSON格式，包含速度、延迟等信息 |
| `mixed_tested.txt` | 测速通过的节点 | 纯文本 |

### 协议分类文件

| 文件 | 说明 |
|------|------|
| `vmess.txt` | VMESS协议节点 |
| `vless.txt` | VLESS协议节点 |
| `trojan.txt` | Trojan协议节点 |
| `hysteria2.txt` | Hysteria2协议节点 |

### 备份文件

- `*.bak` - 去重前的备份文件，用于恢复

---

## 🔧 核心模块详解

### 1. `deduplicate.py` - URL有效性检测

**功能**：并发检测URL可用性，排除无效和慢速链接

**特点**：
- 🧵 并发处理 (10个线程)
- ⏱️ 5秒超时检测
- 🐌 慢速检测 (>1秒视为慢)
- 💾 自动备份 (.bak文件)
- 🔄 失败恢复机制

**使用**：
```bash
python deduplicate.py <input_file> <output_file>
```

**示例**：
```bash
python deduplicate.py resource/subList.csv resource/subList.csv
```

### 2. `telegram_crawler.py` - Telegram爬虫

**功能**：从Telegram公开频道爬取V2ray节点配置

**工作流程**：
1. 读取 `resource/channels.csv` 中的频道列表
2. 转换为Telegram Web版本URL
3. 解析HTML，提取消息中的节点配置
4. 使用正则表达式匹配各协议节点
5. 自动去重和分类

**支持的协议正则**：
```python
{
    'vmess': r'vmess://[^\s<>#]+',
    'vless': r'vless://(?:(?!=reality)[^\s<>#])+',
    'trojan': r'trojan://[^\s<>#]+',
    'hysteria2': r'hysteria2://[^\s<>#]+'
}
```

**配置**：
```python
CONCURRENT_REQUESTS = 16      # 并发请求数
DOWNLOAD_DELAY = 1           # 下载延迟
AUTOTHROTTLE_ENABLED = True  # 自动限速
```

### 3. `pipelines.py` - 数据处理管道

**功能**：将爬取的节点按协议类型分类保存

**处理流程**：
1. 创建 `results/` 目录
2. 为每种协议创建对应文件 (vmess.txt, vless.txt等)
3. 同时写入 `mixed.txt` (混合所有协议)
4. 自动关闭文件流

**输出格式**：
```
vmess://ey[...]Qxd==
vless://uuid@domain.com:443?...
trojan://password@domain.com:443?...
```

### 4. GitHub Actions工作流

**配置文件**：`.github/workflows/Collector.yml`

**关键步骤**：

```yaml
- name: Deduplicate URLs
  # 并发检测URL有效性
  python deduplicate.py resource/subList.csv

- name: Run Scrapy spider
  # 爬取Telegram频道
  scrapy crawl telegram_crawler

- name: Start subconverter and process URLs
  # 批量处理订阅链接 (5个并发，支持重试)
  docker run subconverter:latest

- name: Speedtest
  # 使用singtools测速
  singtools test -i results/mixed.txt -o results/mixed_tested.json

- name: Commit Changes
  # 提交结果到仓库
  git commit -m "✔️ $(date) Collected"
```

**并发处理细节**：
- 每批最多5个链接
- 最多同时处理5个批次
- 单个请求最多重试3次
- 超时时间: 5秒

---

## 📊 监控与日志

### 日志级别配置

在 `myproject/settings.py` 中配置：

```python
LOG_LEVEL = 'WARNING'          # 全局日志级别
SPIDER_MODULES = ["myproject.spiders"]
```

在 `telegram_crawler.py` 中配置：

```python
custom_settings = {
    'LOG_LEVEL': 'ERROR',
    'RETRY_TIMES': 3,
    'DOWNLOAD_TIMEOUT': 30,
}
```

### 常见日志信息

```
✅ URL is reachable (took 0.23s)          # URL有效
❌ URL returned 404                        # 无效URL
⚠️ URL is slow (took 1.5s)                # 慢速检测
🔧 批次 1 请求: http://localhost:25500... # 批处理
✅ 批次 1 完成 (尝试 1)                    # 批处理成功
```

---

## 🐛 常见问题 (FAQ)

### Q1: 爬虫无法访问Telegram频道？

**解决方案**：
- 确保频道是 **公开频道** (public channel)
- 检查频道URL格式是否正确
- Telegram可能有区域限制，请配置代理

### Q2: subconverter容器启动失败？

**解决方案**：
```bash
# 检查Docker是否运行
docker ps

# 查看容器日志
docker logs subconverter_container

# 手动清理并重启
docker stop subconverter_container
docker rm subconverter_container
docker pull asdlokj1qpi23/subconverter:latest
```

### Q3: 测速时没有生成结果？

**解决方案**：
- 检查 `mixed.txt` 是否为空
- 确认 `singtools` 文件有执行权限: `chmod +x tool/speedTest_singtools/singtools`
- 检查 `tool/speedTest_singtools/config.json` 配置是否正确

### Q4: GitHub Actions执行失败？

**解决方案**：
- 查看 Actions 日志找到具体错误
- 确保 secrets 配置正确 (GITHUB_TOKEN)
- 检查 resource/ 目录下的文件格式
- 确保仓库有写权限

### Q5: 如何加快爬虫速度？

**解决方案**：
在 `myproject/settings.py` 中修改：
```python
CONCURRENT_REQUESTS = 32        # 提高并发数
DOWNLOAD_DELAY = 0.5            # 降低延迟
AUTOTHROTTLE_TARGET_CONCURRENCY = 8  # 提高目标并发
```

---

## 🔐 隐私与安全

⚠️ **重要提示**：

1. 本项目仅用于 **学习和研究** 目的
2. 爬虫访问的频道均为 **公开频道**，尊重内容版权
3. 不存储任何个人信息或凭证
4. 建议运行时使用 **VPN或代理**，避免IP限制
5. 遵守当地法律法规

---

## 📈 性能参考

在标准GitHub Actions环境中的性能数据：

| 操作 | 耗时 | 数据量 |
|------|------|--------|
| URL去重 | ~1-2分钟 | 100-200个URLs |
| Telegram爬虫 | ~2-3分钟 | 10-20个频道 |
| 订阅处理 | ~3-5分钟 | 100-200个链接 |
| 节点测速 | ~10-15分钟 | 1000-2000个节点 |
| **总耗时** | **~15-30分钟** | - |

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 开发流程

1. **Fork** 本项目
2. **创建特性分支**：`git checkout -b feature/YourFeature`
3. **提交更改**：`git commit -m 'Add YourFeature'`
4. **推送分支**：`git push origin feature/YourFeature`
5. **创建 Pull Request**

### 代码规范

- 遵循 **PEP 8** 风格指南
- 添加适当的注释和docstring
- 提交前运行测试验证
- 更新README说明新功能

### 报告问题

在GitHub Issues中报告问题时，请提供：
- 详细的问题描述
- 复现步骤
- 相关日志输出
- 系统环境信息 (OS, Python版本等)

---

## 📚 相关项目与资源

### 依赖项目

- **[Scrapy](https://scrapy.org/)** - Python爬虫框架
- **[subconverter](https://github.com/asdlokj1qpi233/subconverter)** - 订阅格式转换工具
- **[singtools](https://github.com/Kdwkakcs/singtools)** - 基于sing-box的节点测试工具
- **[sing-box](https://github.com/SagerNet/sing-box)** - 通用代理平台

### 相关文档

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [V2ray协议规范](https://www.v2fly.org/)
- [Scrapy官方文档](https://docs.scrapy.org/)
- [GitHub Actions文档](https://docs.github.com/en/actions)

---

## 📄 许可证

本项目采用 **[MIT License](LICENSE)** 开源许可证。

```
MIT License

Copyright (c) 2024 V2rayCollector Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

详见 [LICENSE](LICENSE) 文件。

---

## ✨ 致谢

感谢以下项目和贡献者：

- **[asdlokj1qpi233/subconverter](https://github.com/asdlokj1qpi233/subconverter)** - 强大的订阅转换工具
- **[Kdwkakcs/singtools](https://github.com/Kdwkakcs/singtools)** - 高效的节点测速工具
- **[mrvcoder/V2rayCollector](https://github.com/mrvcoder/V2rayCollector)** - 原始项目灵感来源
- **所有贡献者和使用者**

---

<!-- ## 📞 联系方式

- 📧 Email: jagger235711@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/jagger235711/V2rayCollector/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/jagger235711/V2rayCollector/discussions) -->

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个Star！ ⭐**

Made with ❤️ by V2rayCollector Contributors

[⬆ 回到顶部](#-v2raycollector---智能节点爬取与测速工具)

</div>
