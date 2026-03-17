# 从 0 搭建 OpenClaw Agent（Node 安装 + ChatGPT 配置 + 实战）

> 目标：30 分钟内搭出一个可用的 OpenClaw agent，能接消息、能调用工具、能持续工作。

## 1. OpenClaw 是什么？

OpenClaw 是一个多通道、多代理、可工具调用的 Agent 运行框架。  
你可以把它当成：**消息入口 + Agent 路由 + 工具执行 + 持续会话** 的一体化系统。

它能做的事包括：

- 接入 Telegram / Discord / Slack
- 将不同消息路由给不同 agent（如 `main`、`engineer`）
- 让 agent 调文件、命令、浏览器、定时任务等工具
- 用配置统一管理权限和行为

---

## 2. 准备环境

## 2.1 安装 Node.js（建议 LTS）

先确认 Node 版本：

```bash
node -v
npm -v
```

建议 `Node.js 20+`（越新越好，LTS 优先）。

如果你没有 Node，可用 nvm 安装（Linux/macOS 常见）：

```bash
# 安装 nvm（如果未安装）
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 重新加载 shell
source ~/.bashrc   # 或 source ~/.zshrc

# 安装并使用 LTS Node
nvm install --lts
nvm use --lts

# 检查
node -v
npm -v
```

---

## 2.2 用 npm 安装 OpenClaw

```bash
npm install -g openclaw
```

验证安装：

```bash
openclaw help
```

---

## 3. 初始化 OpenClaw

运行引导（按提示做）：

```bash
openclaw onboard
```

如果你的版本没有 `onboard`，就先看帮助：

```bash
openclaw help
```

---

## 4. 配置 ChatGPT（OpenAI / Codex）

OpenClaw 常见是通过 OpenAI Codex OAuth 或 OpenAI Key 来跑模型。  
你可以选择其中一种方式。

## 4.1 推荐：OAuth（如果你的环境支持）

在配置流程中选择 OpenAI/Codex 登录，完成授权后，默认 profile 会写入配置（类似）：

```json
{
  "auth": {
    "profiles": {
      "openai-codex:default": {
        "provider": "openai-codex",
        "mode": "oauth"
      }
    }
  }
}
```

## 4.2 备用：API Key（通用）

在系统环境变量配置你的 OpenAI Key（按你环境做）：

```bash
export OPENAI_API_KEY="sk-xxxx"
```

然后在 OpenClaw 配置里把模型指向 ChatGPT 系列模型（示例）：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai-codex/gpt-5.3-codex"
      }
    }
  }
}
```

> 注：具体可用模型名取决于你当前 OpenClaw 版本和 provider 适配。

---

## 5. 搭建一个可用 Agent（核心）

你至少需要这三块配置：

1. `agents.list`（定义 agent）
2. `channels`（接入消息渠道）
3. `bindings`（把消息路由给 agent）

下面给最小样例（Telegram）：

```json
{
  "agents": {
    "list": [
      { "id": "main" },
      {
        "id": "engineer",
        "name": "engineer",
        "workspace": "/home/ubuntu/.openclaw/workspace-engineer",
        "model": "openai-codex/gpt-5.3-codex"
      }
    ]
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "accounts": {
        "engineer": {
          "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
          "dmPolicy": "allowlist",
          "allowFrom": ["tg:YOUR_USER_ID"]
        }
      }
    }
  },
  "bindings": [
    {
      "agentId": "engineer",
      "match": {
        "channel": "telegram",
        "accountId": "engineer"
      }
    }
  ]
}
```

---

## 6. 启动与重启

查看状态：

```bash
openclaw gateway status
```

启动：

```bash
openclaw gateway start
```

修改配置后重启：

```bash
openclaw gateway restart
```

---

## 7. 验证是否搭建成功

按顺序排查：

1. `openclaw gateway status` 正常
2. ChatGPT 模型配置生效（有响应）
3. 渠道 token 正确
4. binding 命中你实际渠道/account
5. 给 bot 发“你好”，看到 agent 回应

---

## 8. 常见问题（高频）

### 8.1 收到消息但不回复
- 大概率是 `bindings` 没命中，或 `dmPolicy/allowFrom` 拦截了消息。

### 8.2 模型调用失败
- 优先检查：
  - OAuth 是否过期
  - API key 是否可用
  - model 名称是否存在

### 8.3 Slack/Discord 配置了没反应
- 常见是 `groupPolicy`、channel allowlist、mention 规则导致未触发。

---

## 9. 进阶建议

- 按职责拆 agent：`main`（总控）+ `engineer`（技术）+ 其他垂直 agent
- 每个 agent 独立 workspace
- 所有配置进 Git，保证可回滚
- 外发类工具（消息、交易、生产写操作）必须加确认机制

---

## 10. 总结

搭建 OpenClaw agent 的关键只有三步：

1. **装好运行时（Node + OpenClaw）**
2. **接好模型（ChatGPT/OpenAI）**
3. **打通路由（agent + channel + binding）**

这三层跑通后，你就有了一个可持续运营的 agent 基座。
