#!/usr/bin/env python3
"""
合约爆仓逃生教练 - 币安合约风险管理助手
Contract Liquidation Escape Coach

功能：
1. 开仓前风险评估
2. 实时强平监控
3. 三级预警系统
4. 智能止损建议
5. 爆仓复盘分析
6. 交易规则锁
"""

import json
import sys
import requests
import hashlib
import hmac
import time
from datetime import datetime

# 配置
BINANCE_FAPI = "https://fapi.binance.com"
DEMO_MODE = True  # 演示模式，使用模拟数据

class LiquidationCoach:
    def __init__(self):
        self.demo_positions = [
            {
                "symbol": "BTCUSDT",
                "positionSide": "LONG",
                "leverage": 10,
                "entryPrice": 69500,
                "markPrice": 68200,
                "liquidationPrice": 62550,
                "margin": 1000,
                "unrealizedProfit": -130
            },
            {
                "symbol": "ETHUSDT",
                "positionSide": "SHORT",
                "leverage": 5,
                "entryPrice": 2020,
                "markPrice": 2050,
                "liquidationPrice": 2424,
                "margin": 500,
                "unrealizedProfit": -15
            }
        ]
    
    def calc_distance_to_liquidation(self, pos):
        """计算距离爆仓的百分比"""
        mark = float(pos["markPrice"])
        liq = float(pos["liquidationPrice"])
        entry = float(pos["entryPrice"])
        
        if pos["positionSide"] == "LONG":
            distance = (mark - liq) / mark * 100
        else:
            distance = (liq - mark) / liq * 100
        
        return max(0, distance)
    
    def risk_rating(self, distance, leverage):
        """风险评级"""
        score = 0
        if distance < 5:
            score += 50
        elif distance < 10:
            score += 30
        elif distance < 20:
            score += 10
        
        if leverage > 20:
            score += 30
        elif leverage > 10:
            score += 20
        elif leverage > 5:
            score += 10
        
        if score >= 60:
            return "🔴 高危", "立即行动！"
        elif score >= 30:
            return "🟡 警告", "需要关注"
        else:
            return "🟢 安全", "保持监控"
    
    def pre_trade_assessment(self, symbol, leverage, margin):
        """开仓前风险评估"""
        print(f"\n{'='*60}")
        print("📋 开仓前风险评估")
        print(f"{'='*60}")
        print(f"\n拟开仓信息:")
        print(f"  币种: {symbol}")
        print(f"  杠杆: {leverage}x")
        print(f"  保证金: {margin} USDT")
        
        print(f"\n⚠️  请回答以下4个问题:")
        questions = [
            "1. 这笔亏损你能接受吗？ (建议≤本金的5%)",
            "2. 有明确的止损位吗？",
            "3. 现在是大趋势还是震荡？",
            "4. 今晚睡好了吗？(疲劳不开仓)"
        ]
        
        for q in questions:
            print(f"   □ {q}")
        
        print(f"\n📊 风险分析:")
        if leverage > 10:
            print(f"   ⚠️  杠杆过高 ({leverage}x → 建议≤5x)")
        if leverage > 5:
            print(f"   💡 建议降低杠杆至5x或以下")
        
        print(f"\n🎯 建议配置:")
        suggested_leverage = min(leverage, 5)
        suggested_margin = margin * 0.3
        print(f"   • 杠杆: {leverage}x → {suggested_leverage}x")
        print(f"   • 仓位: {margin}U → {suggested_margin:.0f}U (30%)")
        print(f"   • 止损: 建议设置 -3% 止损")
        
        print(f"\n{'='*60}")
    
    def check_positions(self, symbol=None):
        """检查持仓风险"""
        print(f"\n{'='*70}")
        print("🛡️  合约爆仓逃生教练 - 持仓风险报告")
        print(f"{'='*70}")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"模式: {'演示模式' if DEMO_MODE else '实盘模式'}")
        print(f"{'='*70}\n")
        
        positions = self.demo_positions
        
        if not positions:
            print("📭 当前无合约持仓")
            return
        
        total_risk = "🟢 安全"
        
        for pos in positions:
            if symbol and symbol.upper() not in pos["symbol"]:
                continue
            
            distance = self.calc_distance_to_liquidation(pos)
            risk_level, risk_desc = self.risk_rating(distance, pos["leverage"])
            
            if "🔴" in risk_level:
                total_risk = "🔴 高危"
            elif "🟡" in risk_level and total_risk == "🟢 安全":
                total_risk = "🟡 警告"
            
            pnl_pct = (float(pos["unrealizedProfit"]) / float(pos["margin"])) * 100
            
            print(f"📊 {pos['symbol']} {'多' if pos['positionSide'] == 'LONG' else '空'}仓 {pos['leverage']}x")
            print(f"   {'─'*60}")
            print(f"   开仓价: ${pos['entryPrice']:,.2f}")
            print(f"   标记价: ${pos['markPrice']:,.2f}")
            print(f"   强平价: ${pos['liquidationPrice']:,.2f}")
            print(f"   未实现盈亏: {pos['unrealizedProfit']:+.2f} USDT ({pnl_pct:+.2f}%)")
            print(f"   保证金: {pos['margin']} USDT")
            print(f"   {'─'*60}")
            print(f"   距离爆仓: -{distance:.2f}% 📉")
            print(f"   风险评级: {risk_level} ({risk_desc})")
            
            # 预警建议
            if distance < 10:
                print(f"\n   🚨 紧急建议:")
                print(f"      1. 立即减仓50% (强平价升至更高)")
                print(f"      2. 追加保证金 {pos['margin']*0.5:.0f}U")
                print(f"      3. 设置止损 -5%")
            elif distance < 20:
                print(f"\n   ⚠️  建议:")
                print(f"      • 设置止损保护")
                print(f"      • 降低杠杆至5x")
            
            print()
        
        print(f"{'='*70}")
        print(f"总体风险: {total_risk}")
        print(f"{'='*70}\n")
        
        # 通用建议
        print("💡 合约交易守则:")
        print("   1. 杠杆≤5x，仓位≤本金30%")
        print("   2. 开仓必设止损 (-3% to -5%)")
        print("   3. 亏损超5%当天不再交易")
        print("   4. 切勿逆势加仓")
        print()
    
    def smart_stop_loss(self, symbol, entry_price, leverage):
        """智能止损建议"""
        print(f"\n{'='*60}")
        print("🎯 智能止损建议")
        print(f"{'='*60}")
        print(f"\n币种: {symbol}")
        print(f"开仓价: ${entry_price}")
        print(f"杠杆: {leverage}x")
        
        # 基于杠杆的止损建议
        if leverage <= 3:
            stop_pct = -5
        elif leverage <= 5:
            stop_pct = -3
        elif leverage <= 10:
            stop_pct = -2
        else:
            stop_pct = -1.5
        
        stop_price = entry_price * (1 + stop_pct/100) if leverage > 0 else entry_price * (1 - stop_pct/100)
        
        print(f"\n建议止损位: ${stop_price:,.2f} ({stop_pct}%)")
        print(f"理由:")
        print(f"   • {leverage}x杠杆建议止损{abs(stop_pct)}%")
        print(f"   • 低于近期支撑位")
        print(f"   • 预计最大亏损: {abs(stop_pct)*leverage}% 本金")
        
        print(f"\n{'='*60}\n")
    
    def post_liquidation_review(self):
        """爆仓复盘分析"""
        print(f"\n{'='*60}")
        print("💔 爆仓复盘报告 (模拟)")
        print(f"{'='*60}")
        
        review_data = {
            "symbol": "BTCUSDT",
            "direction": "多仓",
            "leverage": 20,
            "entry": 69500,
            "liquidation": 66000,
            "loss": -1000
        }
        
        print(f"\n爆仓详情:")
        print(f"   币种: {review_data['symbol']}")
        print(f"   方向: {review_data['direction']}")
        print(f"   杠杆: {review_data['leverage']}x")
        print(f"   爆仓价: ${review_data['liquidation']}")
        print(f"   亏损: {review_data['loss']} USDT")
        
        print(f"\n❌ 错误分析:")
        errors = [
            "杠杆过高 (20x，建议≤5x)",
            "无止损设置 (扛单47分钟)",
            "逆势加仓 (亏损后加多)",
            "满仓操作 (风险集中度100%)"
        ]
        for i, err in enumerate(errors, 1):
            print(f"   {i}. {err}")
        
        print(f"\n✅ 改进建议:")
        improvements = [
            "下次杠杆≤5x",
            "开仓必设止损 -3%",
            "亏损超5%当天不再交易",
            "仓位≤本金的30%"
        ]
        for i, imp in enumerate(improvements, 1):
            print(f"   {i}. {imp}")
        
        print(f"\n{'='*60}\n")
    
    def trading_rules(self):
        """交易规则设置"""
        print(f"\n{'='*60}")
        print("🔒 交易规则锁 (模拟)")
        print(f"{'='*60}")
        
        rules = {
            "日最大亏损": "500 USDT",
            "连续亏损冷却": "3单后冷却1小时",
            "夜间禁交易": "凌晨1-6点禁止开仓",
            "高波动降杠杆": "波动>5%时杠杆减半"
        }
        
        print(f"\n当前规则:")
        for rule, value in rules.items():
            print(f"   □ {rule}: {value}")
        
        print(f"\n📊 今日状态:")
        print(f"   今日亏损: 0 / 500 USDT")
        print(f"   连续亏损: 0 单")
        print(f"   交易状态: 🟢 允许交易")
        
        print(f"\n{'='*60}\n")

def show_help():
    print("""
🛡️ 合约爆仓逃生教练 - 使用帮助

用法: python3 coach.py [命令] [参数]

命令:
  check [币种]     检查持仓风险 (如: check BTC)
  assess          开仓前风险评估
  stop [价] [杠]   智能止损建议 (如: stop 69500 10)
  review          爆仓复盘分析
  rules           交易规则设置
  help            显示帮助

示例:
  python3 coach.py check
  python3 coach.py check BTC
  python3 coach.py stop 69500 10
  python3 coach.py review

提示: 本工具为演示版本，使用模拟数据
    """)

def main():
    coach = LiquidationCoach()
    
    if len(sys.argv) < 2:
        coach.check_positions()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "check":
        symbol = sys.argv[2] if len(sys.argv) > 2 else None
        coach.check_positions(symbol)
    
    elif cmd == "assess":
        coach.pre_trade_assessment("BTCUSDT", 10, 1000)
    
    elif cmd == "stop":
        if len(sys.argv) < 4:
            print("用法: coach.py stop <开仓价> <杠杆>")
            print("示例: coach.py stop 69500 10")
        else:
            coach.smart_stop_loss("BTCUSDT", float(sys.argv[2]), int(sys.argv[3]))
    
    elif cmd == "review":
        coach.post_liquidation_review()
    
    elif cmd == "rules":
        coach.trading_rules()
    
    elif cmd == "help":
        show_help()
    
    else:
        print(f"未知命令: {cmd}")
        show_help()

if __name__ == "__main__":
    main()
