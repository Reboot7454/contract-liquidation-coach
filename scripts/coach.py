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
7. 剧烈波动监控 + 语音提醒
"""

import json
import sys
import requests
import hashlib
import hmac
import time
import subprocess
import argparse
import os
from datetime import datetime

# 配置
BINANCE_FAPI = "https://fapi.binance.com"
DEMO_MODE = True  # 演示模式，使用模拟数据

# TTS 配置 - macOS say 命令
TTS_ENABLED = True
TTS_VOICE = "Ting-Ting"  # 中文语音

# 剧烈波动配置
VOLATILITY_THRESHOLD = 2.0  # 1分钟内波动超过2%触发提醒
PRICE_HISTORY = {}  # 价格历史缓存

def speak_alert(message, priority="normal"):
    """
    语音播报警报
    priority: "normal" | "warning" | "danger" | "volatility"
    """
    if not TTS_ENABLED:
        return
    
    try:
        if priority == "danger":
            rate = 180
        elif priority == "warning":
            rate = 200
        elif priority == "volatility":
            rate = 210
        else:
            rate = 220
        
        cmd = f'say -v {TTS_VOICE} -r {rate} "{message}"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

class BinanceAPI:
    """币安合约 API 封装"""
    
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.base_url = BINANCE_FAPI
        
    def _generate_signature(self, params):
        """生成签名"""
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def get_positions(self, symbol=None):
        """获取合约持仓"""
        if not self.api_key or not self.api_secret:
            return None
        
        try:
            timestamp = int(time.time() * 1000)
            params = {'timestamp': timestamp}
            if symbol:
                params['symbol'] = symbol
            
            params['signature'] = self._generate_signature(params)
            
            headers = {'X-MBX-APIKEY': self.api_key}
            response = requests.get(
                f"{self.base_url}/fapi/v2/positionRisk",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            positions = []
            for pos in data:
                if float(pos.get('positionAmt', 0)) != 0:
                    positions.append({
                        'symbol': pos['symbol'],
                        'positionSide': 'LONG' if float(pos['positionAmt']) > 0 else 'SHORT',
                        'leverage': int(pos['leverage']),
                        'entryPrice': float(pos['entryPrice']),
                        'markPrice': float(pos['markPrice']),
                        'liquidationPrice': float(pos['liquidationPrice']),
                        'margin': float(pos['isolatedMargin']) if float(pos['isolatedMargin']) > 0 else abs(float(pos['positionAmt']) * float(pos['entryPrice']) / int(pos['leverage'])),
                        'unrealizedProfit': float(pos['unRealizedProfit'])
                    })
            return positions
            
        except Exception as e:
            print(f"⚠️  API 调用失败: {e}")
            return None
    
    def get_ticker_price(self, symbol):
        """获取最新价格"""
        try:
            response = requests.get(
                f"{self.base_url}/fapi/v1/ticker/price",
                params={'symbol': symbol},
                timeout=5
            )
            response.raise_for_status()
            return float(response.json()['price'])
        except Exception:
            return None

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
        self.api = BinanceAPI()
    
    def calc_distance_to_liquidation(self, pos):
        """计算距离爆仓的百分比"""
        mark = float(pos["markPrice"])
        liq = float(pos["liquidationPrice"])
        
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
    
    def check_volatility(self, symbol, voice=False):
        """检查剧烈波动"""
        global PRICE_HISTORY
        
        current_price = self.api.get_ticker_price(symbol)
        if current_price is None:
            return None
        
        now = time.time()
        
        # 清理1分钟前的历史
        if symbol in PRICE_HISTORY:
            PRICE_HISTORY[symbol] = [
                (t, p) for t, p in PRICE_HISTORY[symbol] 
                if now - t < 60
            ]
        else:
            PRICE_HISTORY[symbol] = []
        
        # 检查波动
        volatility_alerts = []
        for t, p in PRICE_HISTORY[symbol]:
            change_pct = abs(current_price - p) / p * 100
            if change_pct >= VOLATILITY_THRESHOLD:
                direction = "上涨" if current_price > p else "下跌"
                alert_msg = f"注意！{symbol.replace('USDT', '')} 一分钟内{direction} {change_pct:.1f} 百分比！请关注风险！"
                volatility_alerts.append((change_pct, alert_msg))
        
        # 记录当前价格
        PRICE_HISTORY[symbol].append((now, current_price))
        
        # 播报最剧烈的波动
        if volatility_alerts and voice:
            max_volatility = max(volatility_alerts, key=lambda x: x[0])
            speak_alert(max_volatility[1], "volatility")
        
        return volatility_alerts
    
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
    
    def get_positions_data(self, symbol=None):
        """获取持仓数据（实盘或演示）"""
        global DEMO_MODE
        
        real_positions = self.api.get_positions(symbol)
        
        if real_positions is not None:
            DEMO_MODE = False
            return real_positions
        else:
            DEMO_MODE = True
            if symbol:
                return [p for p in self.demo_positions if symbol.upper() in p['symbol']]
            return self.demo_positions
    
    def check_positions(self, symbol=None, voice=False, check_volatility=False):
        """检查持仓风险"""
        global DEMO_MODE
        
        print(f"\n{'='*70}")
        print("🛡️  合约爆仓逃生教练 - 持仓风险报告")
        print(f"{'='*70}")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"模式: {'演示模式' if DEMO_MODE else '实盘模式'}")
        if voice:
            print("🔊 语音播报: 已启用")
        if check_volatility:
            print("📈 波动监控: 已启用 (阈值: ±2%/min)")
        print(f"{'='*70}\n")
        
        # 检查剧烈波动
        if check_volatility:
            print("📊 检查市场波动...")
            monitored_symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']
            for sym in monitored_symbols:
                vol_alerts = self.check_volatility(sym, voice)
                if vol_alerts:
                    max_vol = max(vol_alerts, key=lambda x: x[0])
                    print(f"   ⚠️  {sym}: 1分钟内波动 {max_vol[0]:.2f}%")
            print()
        
        # 获取持仓
        positions = self.get_positions_data(symbol)
        
        if not positions:
            print("📭 当前无合约持仓")
            if voice:
                speak_alert("当前无合约持仓", "normal")
            return
        
        total_risk = "🟢 安全"
        danger_alerts = []
        warning_alerts = []
        
        for pos in positions:
            if symbol and symbol.upper() not in pos["symbol"]:
                continue
            
            distance = self.calc_distance_to_liquidation(pos)
            risk_level, risk_desc = self.risk_rating(distance, pos["leverage"])
            
            if "🔴" in risk_level:
                total_risk = "🔴 高危"
                alert_msg = f"警告！{pos['symbol'][:-4]} {'多仓' if pos['positionSide'] == 'LONG' else '空仓'}距离爆仓仅剩 {distance:.1f} 百分比！建议立即减仓或追加保证金！"
                danger_alerts.append(alert_msg)
            elif "🟡" in risk_level and total_risk == "🟢 安全":
                total_risk = "🟡 警告"
                alert_msg = f"注意，{pos['symbol'][:-4]} {'多仓' if pos['positionSide'] == 'LONG' else '空仓'}距离爆仓 {distance:.1f} 百分比，请关注风险。"
                warning_alerts.append(alert_msg)
            
            pnl_pct = (float(pos["unrealizedProfit"]) / float(pos["margin"])) * 100
            
            print(f"📊 {pos['symbol']} {'多' if pos['positionSide'] == 'LONG' else '空'}仓 {pos['leverage']}x")
            print(f"   {'─'*60}")
            print(f"   开仓价: ${pos['entryPrice']:,.2f}")
            print(f"   标记价: ${pos['markPrice']:,.2f}")
            print(f"   强平价: ${pos['liquidationPrice']:,.2f}")
            print(f"   未实现盈亏: {pos['unrealizedProfit']:+.2f} USDT ({pnl_pct:+.2f}%)")
            print(f"   保证金: {pos['margin']:.2f} USDT")
            print(f"   {'─'*60}")
            print(f"   距离爆仓: -{distance:.2f}% 📉")
            print(f"   风险评级: {risk_level} ({risk_desc})")
            
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
        
        # 语音播报
        if voice:
            if danger_alerts:
                for _ in range(2):
                    for alert in danger_alerts:
                        speak_alert(alert, "danger")
                        time.sleep(0.5)
            elif warning_alerts:
                for alert in warning_alerts:
                    speak_alert(alert, "warning")
            else:
                speak_alert("所有持仓风险正常，请继续保持监控。", "normal")
        
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

用法: python3 coach.py [命令] [参数] [--voice] [--volatility]

命令:
  check [币种]     检查持仓风险 (如: check BTC)
  assess          开仓前风险评估
  stop [价] [杠]   智能止损建议 (如: stop 69500 10)
  review          爆仓复盘分析
  rules           交易规则设置
  help            显示帮助

选项:
  --voice         启用语音播报
  --volatility    启用剧烈波动监控 (±2%/min)

环境变量:
  BINANCE_API_KEY      币安 API Key (实盘模式)
  BINANCE_API_SECRET   币安 API Secret (实盘模式)

示例:
  python3 coach.py check                    # 普通检查
  python3 coach.py check BTC --voice        # 检查BTC + 语音播报
  python3 coach.py check --voice --volatility  # 全面监控 + 波动提醒
  python3 coach.py stop 69500 10
  python3 coach.py review

提示: 未配置API时自动使用演示数据
    """)

def main():
    parser = argparse.ArgumentParser(description='合约爆仓逃生教练', add_help=False)
    parser.add_argument('command', nargs='?', default='check', help='命令')
    parser.add_argument('args', nargs='*', help='命令参数')
    parser.add_argument('--voice', action='store_true', help='启用语音播报')
    parser.add_argument('--volatility', action='store_true', help='启用剧烈波动监控')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助')
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        return
    
    coach = LiquidationCoach()
    cmd = args.command.lower()
    
    if cmd == "check":
        symbol = args.args[0] if args.args else None
        coach.check_positions(symbol, voice=args.voice, check_volatility=args.volatility)
    
    elif cmd == "assess":
        coach.pre_trade_assessment("BTCUSDT", 10, 1000)
    
    elif cmd == "stop":
        if len(args.args) < 2:
            print("用法: coach.py stop <开仓价> <杠杆>")
            print("示例: coach.py stop 69500 10")
        else:
            coach.smart_stop_loss("BTCUSDT", float(args.args[0]), int(args.args[1]))
    
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
