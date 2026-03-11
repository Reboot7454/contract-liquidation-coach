# 🛡️ 合约爆仓逃生教练

币安合约用户的风险管理助手，帮助你在爆仓前逃生。

## 📦 安装

### 方法1: 一键安装 (推荐)
```bash
# 复制Skill到OpenClaw目录
cp -r contract-liquidation-coach ~/.openclaw/workspace/skills/

# 验证安装
python3 ~/.openclaw/workspace/skills/contract-liquidation-coach/scripts/coach.py help
```

### 方法2: 手动安装
1. 下载本文件夹
2. 复制到 `~/.openclaw/workspace/skills/contract-liquidation-coach/`
3. 确保目录结构如下：
```
contract-liquidation-coach/
├── SKILL.md
├── README.md
└── scripts/
    └── coach.py
```

## 🚀 快速开始

### 基本用法
```bash
# 查看所有持仓风险
python3 scripts/coach.py check

# 查看指定币种风险
python3 scripts/coach.py check BTC

# 开仓前风险评估
python3 scripts/coach.py assess

# 智能止损建议
python3 scripts/coach.py stop 69500 10

# 爆仓复盘分析
python3 scripts/coach.py review

# 交易规则设置
python3 scripts/coach.py rules
```

## 📖 功能详解

### 1️⃣ 开仓前风险评估
```bash
python3 scripts/coach.py assess
```
功能：
- 4道强制冷静期问题
- 杠杆/仓位优化建议
- 风险评级

### 2️⃣ 实时强平监控
```bash
python3 scripts/coach.py check
```
功能：
- 显示距离爆仓百分比
- 三级风险评级 (🟢🟡🔴)
- 紧急逃生建议

### 3️⃣ 智能止损建议
```bash
python3 scripts/coach.py stop <开仓价> <杠杆>
# 示例
python3 scripts/coach.py stop 69500 10
```
功能：
- 基于杠杆倍数计算最优止损
- 预计最大亏损金额

### 4️⃣ 爆仓复盘分析
```bash
python3 scripts/coach.py review
```
功能：
- 错误分析
- 改进建议
- 避免重复犯错

### 5️⃣ 交易规则锁
```bash
python3 scripts/coach.py rules
```
功能：
- 日亏损上限设置
- 连续亏损冷却
- 夜间禁交易

## 📊 示例输出

### 持仓风险检查
```
======================================================================
🛡️  合约爆仓逃生教练 - 持仓风险报告
======================================================================
时间: 2026-03-11 18:00:00
模式: 演示模式
======================================================================

📊 BTCUSDT 多仓 10x
   ────────────────────────────────────────────────────────────
   开仓价: $69,500.00
   标记价: $68,200.00
   强平价: $62,550.00
   未实现盈亏: -130.00 USDT (-13.00%)
   保证金: 1000 USDT
   ────────────────────────────────────────────────────────────
   距离爆仓: -8.24% 📉
   风险评级: 🟡 警告 (需要关注)

   ⚠️  建议:
      • 设置止损保护
      • 降低杠杆至5x

======================================================================
总体风险: 🟡 警告
======================================================================

💡 合约交易守则:
   1. 杠杆≤5x，仓位≤本金30%
   2. 开仓必设止损 (-3% to -5%)
   3. 亏损超5%当天不再交易
   4. 切勿逆势加仓
```

## ⚠️ 风险提示

**重要声明**：
- 本工具仅供学习交流，不构成投资建议
- 加密货币合约交易风险极高，可能导致本金全部损失
- 请根据自身风险承受能力谨慎交易
- 过往表现不代表未来收益

**使用本工具即表示您理解并同意**：
1. 本工具提供的建议仅供参考
2. 交易决策由用户自行负责
3. 开发者不对任何交易损失承担责任
4. 请遵守当地法律法规

## 🔧 配置说明

### 使用真实币安API (可选)
编辑脚本顶部配置：
```python
DEMO_MODE = False  # 关闭演示模式
BINANCE_API_KEY = "your-api-key"
BINANCE_API_SECRET = "your-api-secret"
```

### 自定义交易规则
编辑 `coach.py` 中的 `trading_rules` 方法：
```python
rules = {
    "日最大亏损": "500 USDT",      # 修改这里
    "连续亏损冷却": "3单后冷却1小时",
    "夜间禁交易": "凌晨1-6点禁止开仓",
    "高波动降杠杆": "波动>5%时杠杆减半"
}
```

## 📄 文件结构

```
contract-liquidation-coach/
├── SKILL.md              # Skill描述文件
├── README.md             # 使用说明
└── scripts/
    └── coach.py          # 主脚本
```

## 🏆 参赛信息

- **比赛**: 币安小龙虾大赛 (Binance Lobster Hackathon)
- **作品名称**: 合约爆仓逃生教练
- **作者**: 陈冠希
- **时间**: 2026-03-11

## 🤝 贡献

欢迎提交Issue和PR！

## 📜 许可证

MIT License

## 💬 联系

如有问题，欢迎在币安广场或X联系。

---

**记住：不是不让你玩合约，是让你活着玩下去。** 🛡️
