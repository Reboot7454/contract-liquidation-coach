# 🛡️ 合约爆仓逃生教练

> 币安合约用户的风险管理助手，帮助用户在爆仓前逃生。
> 
> **不是教你怎么赚钱，而是教你怎么不亏。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

---

## 🎯 核心价值

- 🚨 **开仓前风险评估** - 4问强制冷静期，科学配置建议
- 📊 **实时强平监控** - 显示距离爆仓%，预估剩余时间  
- 🔔 **三级预警系统** - 🟢安全🟡警告🔴危险分级提醒
- 🎯 **智能止损建议** - 基于ATR/支撑阻力/风险偏好
- 📈 **剧烈波动监控** - 1分钟内波动超2%自动语音提醒
- 🔊 **语音播报** - 高危时电脑语音警报（macOS）
- 📋 **爆仓复盘分析** - 错误诊断+改进建议
- 🔒 **交易规则锁** - 违规自动拦截（单日亏损上限等）

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/Reboot7454/contract-liquidation-coach.git ~/.openclaw/workspace/skills/contract-liquidation-coach

# 进入目录
cd ~/.openclaw/workspace/skills/contract-liquidation-coach
```

### 配置币安 API（可选，用于实盘监控）

```bash
# 设置环境变量
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

> 💡 **权限建议**: 只开 **读取 + 交易** 权限，**不要开提币**

---

## 📖 使用方法

### 基础检查（演示模式）
```bash
python3 scripts/coach.py check
```

### 检查 + 语音播报
```bash
python3 scripts/coach.py check --voice
```

### 全面监控（语音 + 波动检测）
```bash
python3 scripts/coach.py check --voice --volatility
```

### 检查指定币种
```bash
python3 scripts/coach.py check BTC --voice
```

### 其他命令
```bash
# 开仓前风险评估
python3 scripts/coach.py assess

# 智能止损建议
python3 scripts/coach.py stop 69500 10

# 爆仓复盘分析
python3 scripts/coach.py review

# 交易规则设置
python3 scripts/coach.py rules
```

---

## 🔊 语音提醒说明

| 风险等级 | 触发条件 | 语音内容 | 播报次数 |
|---------|---------|---------|---------|
| 🔴 高危 | 距离爆仓 < 5% | "警告！XX多仓距离爆仓仅剩X%！建议立即减仓或追加保证金！" | 3次 |
| 🟡 警告 | 距离爆仓 < 10% | "注意，XX空仓距离爆仓X%，请关注风险。" | 1次 |
| 📈 波动 | 1分钟波动 > 2% | "注意！BTC一分钟内上涨/下跌X%！请关注风险！" | 1次 |
| 🟢 安全 | 无风险 | "所有持仓风险正常，请继续保持监控。" | 1次 |

---

## ⏰ 定时监控配置

```bash
# 每2分钟检查一次（监控波动 + 爆仓风险）
*/2 * * * * cd ~/.openclaw/workspace/skills/contract-liquidation-coach && python3 scripts/coach.py check --voice --volatility
```

---

## 🏆 参赛信息

- **大赛**: 币安小龙虾大赛（币安AI Agent创意大赛）
- **作品名称**: 合约爆仓逃生教练
- **作者**: 陈冠希 / Reboot7454
- **核心理念**: 负责任金融，降低用户爆仓损失

---

## ⚠️ 风险提示

- 本工具仅提供风险管理建议，**不构成投资建议**
- 加密货币合约交易风险极高，可能导致本金全部损失
- 请根据自身风险承受能力谨慎交易
- 过往表现不代表未来收益

---

## 📄 免责声明

使用本工具即表示您理解并同意：
1. 本工具提供的建议仅供参考
2. 交易决策由用户自行负责
3. 开发者不对任何交易损失承担责任
4. 请遵守当地法律法规

---

## 🛠️ 技术栈

- Python 3.8+
- 币安合约 API (Binance Futures API)
- macOS `say` 命令（语音播报）
- OpenClaw Agent 框架

---

## 📜 版本历史

- **v1.1.0** (2026-03-12) - 新增实盘API支持、语音播报、剧烈波动监控
- **v1.0.0** (2026-03-11) - 初始版本，6大核心功能

---

## 📞 联系

- GitHub: [@Reboot7454](https://github.com/Reboot7454)
- Email: a408034351@gmail.com

---

**记住：活着，才有输出。** 🛡️
