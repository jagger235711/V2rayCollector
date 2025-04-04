# V2rayCollector


## 项目简介
V2rayCollector 是一个从 Telegram 频道抓取 节点 配置、从订阅链接汇总 节点 的项目。

### 支持的类型

|      节点类型      | 是否支持 |
| :----------------: | :------: |
|       VLESS        |   支持   |
|       VMESS        |   支持   |
|  SS (Shadowsocks)  |   支持   |
| SSR (ShadowsocksR) |   支持   |
|       Trojan       |   支持   |
|     hysteria2      |   支持   |

## 项目结构
项目主要包含以下几个部分：
- .github/workflows: 包含 GitHub Actions 工作流配置文件。
- collector: 包含辅助函数的 Go 包。
- tool: 包含项目使用的工具，如 subconverter 和 speedTest_singtools。
- results: 包含项目运行后生成的结果文件。
- channels.csv 和 subList.csv: 包含频道列表和订阅链接的 CSV 文件。
- main.go: 项目的主程序文件,用于实现从公开频道中获取节点。
- go.mod 和 go.sum: Go 模块的依赖管理文件。
- README.md: 项目的说明文档。



## 贡献
欢迎任何形式的贡献！你可以通过以下方式贡献：

提交 Issue 反馈 bug 或者建议。
提交 Pull Request 改进代码。

## 感谢

- [subconverter](https://github.com/asdlokj1qpi233/subconverter "用于转换各种代理订阅格式的工具")
- [singtools](https://github.com/Kdwkakcs/singtools "基于sing - box的节点测试工具")
- [V2rayCollector](https://github.com/mrvcoder/V2rayCollector "从Telegram频道抓取v2ray配置的项目")