#!/bin/bash
# 生成演示截图脚本

echo "📸 正在生成演示截图..."
echo ""

cd ~/.openclaw/workspace/skills/contract-liquidation-coach/scripts

# 截图1: 持仓风险检查
echo "截图1: 持仓风险检查 (coach.py check)"
python3 coach.py check > ../screenshots/demo1_check.txt 2>&1
echo "✅ 已保存到 screenshots/demo1_check.txt"

# 截图2: 开仓前评估
echo "截图2: 开仓前风险评估 (coach.py assess)"
python3 coach.py assess > ../screenshots/demo2_assess.txt 2>&1
echo "✅ 已保存到 screenshots/demo2_assess.txt"

# 截图3: 智能止损
echo "截图3: 智能止损建议 (coach.py stop)"
python3 coach.py stop 69500 10 > ../screenshots/demo3_stop.txt 2>&1
echo "✅ 已保存到 screenshots/demo3_stop.txt"

# 截图4: 爆仓复盘
echo "截图4: 爆仓复盘分析 (coach.py review)"
python3 coach.py review > ../screenshots/demo4_review.txt 2>&1
echo "✅ 已保存到 screenshots/demo4_review.txt"

# 截图5: 帮助信息
echo "截图5: 帮助信息 (coach.py help)"
python3 coach.py help > ../screenshots/demo5_help.txt 2>&1
echo "✅ 已保存到 screenshots/demo5_help.txt"

echo ""
echo "🎉 所有演示截图已生成!"
echo ""
echo "📁 截图文件位置:"
echo "   screenshots/demo1_check.txt   - 持仓风险检查"
echo "   screenshots/demo2_assess.txt  - 开仓前评估"
echo "   screenshots/demo3_stop.txt    - 智能止损建议"
echo "   screenshots/demo4_review.txt  - 爆仓复盘分析"
echo "   screenshots/demo5_help.txt    - 帮助信息"
echo ""
echo "💡 使用说明:"
echo "   1. 打开对应的.txt文件"
echo "   2. 复制内容或截图"
echo "   3. 用于参赛帖子配图"
