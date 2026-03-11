#!/bin/bash
# 合约爆仓逃生教练 - 一键安装脚本

echo "🛡️  合约爆仓逃生教练 - 安装脚本"
echo "======================================"
echo ""

# 检查OpenClaw目录
OPENCLAW_DIR="$HOME/.openclaw/workspace/skills"
if [ ! -d "$OPENCLAW_DIR" ]; then
    echo "❌ 错误: 未找到OpenClaw目录"
    echo "   请确认OpenClaw已正确安装"
    echo "   预期路径: $OPENCLAW_DIR"
    exit 1
fi

# 检查当前目录
if [ ! -f "SKILL.md" ]; then
    echo "❌ 错误: 请在Skill根目录运行此脚本"
    echo "   预期文件: SKILL.md"
    exit 1
fi

# 安装路径
INSTALL_DIR="$OPENCLAW_DIR/contract-liquidation-coach"

echo "📦 安装信息:"
echo "   源目录: $(pwd)"
echo "   目标目录: $INSTALL_DIR"
echo ""

# 如果已存在，询问是否覆盖
if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  检测到已安装版本"
    read -p "   是否覆盖? (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "   安装已取消"
        exit 0
    fi
    rm -rf "$INSTALL_DIR"
fi

# 复制文件
echo "📁 正在复制文件..."
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"

# 检查是否成功
if [ ! -f "$INSTALL_DIR/scripts/coach.py" ]; then
    echo "❌ 安装失败"
    exit 1
fi

# 测试运行
echo "🧪 测试安装..."
python3 "$INSTALL_DIR/scripts/coach.py" help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ 测试通过"
else
    echo "   ⚠️  测试失败，但文件已复制"
fi

echo ""
echo "✅ 安装完成!"
echo ""
echo "🚀 快速开始:"
echo "   cd $INSTALL_DIR"
echo "   python3 scripts/coach.py check"
echo ""
echo "📖 查看帮助:"
echo "   python3 scripts/coach.py help"
echo ""
echo "📄 完整文档:"
echo "   cat $INSTALL_DIR/README.md"
echo ""
