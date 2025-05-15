# Slack通知配置指南

本文档介绍如何为"自动空格按键工具"配置GitHub Actions的Slack通知功能。

## 步骤

1. **创建Slack应用**

   - 访问 [Slack API](https://api.slack.com/apps) 页面
   - 点击"Create New App"
   - 选择"From scratch"
   - 输入应用名称（例如："自动空格按键工具通知"）
   - 选择您的工作区

2. **添加Incoming Webhooks功能**

   - 在左侧导航栏选择"Incoming Webhooks"
   - 将"Activate Incoming Webhooks"切换为开启状态
   - 点击"Add New Webhook to Workspace"
   - 选择要发送通知的频道
   - 点击"允许"

3. **复制Webhook URL**

   - 在Incoming Webhooks页面，找到新创建的Webhook
   - 复制Webhook URL

4. **添加GitHub仓库密钥**

   - 打开GitHub仓库
   - 点击"Settings" > "Secrets and variables" > "Actions"
   - 点击"New repository secret"
   - 名称填写：`SLACK_WEBHOOK_URL`
   - 值填写：步骤3中复制的Webhook URL
   - 点击"Add secret"

5. **测试通知**

   - 手动触发自动构建工作流
   - 构建完成后，检查指定的Slack频道是否收到通知

## 故障排除

如果您没有收到通知，请检查：

1. Webhook URL是否正确添加为仓库密钥
2. GitHub Actions工作流配置中是否正确引用了密钥
3. Slack应用是否有权限发送消息到指定频道

## 自定义通知

您可以通过编辑`.github/workflows/auto-build.yml`文件中的以下部分来自定义通知：

```yaml
env:
  SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK_URL }}
  SLACK_CHANNEL: builds  # 更改为您想要的频道名
  SLACK_COLOR: good      # 可以是"good"、"warning"、"danger"或十六进制颜色代码
  SLACK_TITLE: 自动空格按键工具构建完成  # 更改为您想要的标题
  SLACK_MESSAGE: '构建完成! 构建产物可在 GitHub Actions 页面获取。'  # 更改为您想要的消息
``` 