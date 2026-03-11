# GitHub 上传指南

## 方法1: 手动创建仓库 (推荐)

### 步骤1: 在GitHub创建仓库
1. 打开 https://github.com/new
2. 仓库名: `contract-liquidation-coach`
3. 描述: `币安合约爆仓逃生教练 - 币安小龙虾大赛参赛作品`
4. 选择 **Public**
5. 不要勾选 "Initialize this repository with a README"
6. 点击 **Create repository**

### 步骤2: 推送代码
```bash
cd ~/.openclaw/workspace/skills/contract-liquidation-coach
git remote add origin https://github.com/你的用户名/contract-liquidation-coach.git
git branch -M main
git push -u origin main
```

---

## 方法2: 使用GitHub CLI (需要登录)

```bash
# 登录GitHub
gh auth login

# 创建仓库并推送
cd ~/.openclaw/workspace/skills/contract-liquidation-coach
gh repo create contract-liquidation-coach --public --source=. --push
```

---

## 方法3: 直接下载ZIP分享

如果不想用GitHub，可以打包成ZIP：

```bash
cd ~/.openclaw/workspace/skills/contract-liquidation-coach
zip -r contract-liquidation-coach.zip .
```

然后直接上传ZIP文件到比赛表单。

---

## 📋 仓库创建后的参赛链接

创建完成后，你的仓库链接将是：
```
https://github.com/你的用户名/contract-liquidation-coach
```

把这个链接填入币安参赛表单的"作品链接"一栏。

---

## 🔗 快速复制命令

```bash
# 设置Git用户名
git config --global user.name "陈冠希"
git config --global user.email "your-email@example.com"

# 添加远程仓库 (替换YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/contract-liquidation-coach.git

# 推送
git push -u origin main
```

**注意**: 推送时会要求输入GitHub用户名和密码（或Personal Access Token）
