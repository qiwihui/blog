# rsETH 攻击事件完整时间线

> Issue: #195  
> State: open  
> Source: [https://github.com/qiwihui/blog/issues/195](https://github.com/qiwihui/blog/issues/195)



> **事件规模**：$2.92 亿无抵押 rsETH 被凭空铸造，Aave 产生约 $1.24 亿–$2.30 亿坏账，波及 KelpDAO、LayerZero、Aave、DeFi United 四方。
>
> **攻击日期**：2026 年 4 月 18 日 17:35 UTC
> **归因**：朝鲜 Lazarus Group（TraderTraitor 子组织）
> **攻击向量**：RPC 节点投毒 + DDoS，针对 LayerZero 1-of-1 DVN 配置
>
> *文档整理日期：2026 年 5 月 16 日*

---

## 目录

1. [事件概览](#一事件概览)
2. [LayerZero V2 机制与 DVN 角色](#二layerzero-v2-机制与-dvn-角色)
3. [根本漏洞分析](#三根本漏洞分析1-of-1-dvn-默认配置)
4. [攻击前隐患](#四攻击前隐患2024-01--2026-04-17)
5. [链上数据与关键地址](#五链上数据与关键地址)
6. [小时级攻击时间线](#六小时级攻击时间线2026-04-18-utc)
7. [危机首日](#七危机首日2026-04-19)
8. [官方报告与互相指责](#八官方报告与互相指责2026-04-20)
9. [资金追踪与洗钱](#九资金追踪与洗钱2026-04-21--04-22)
10. [DeFi United 联盟与方案细化](#十defi-united-联盟与方案细化2026-04-23--04-28)
11. [法律与治理博弈](#十一法律与治理博弈2026-05-01--05-12)
12. [协议重启与基础设施迁移](#十二协议重启与基础设施迁移2026-05-13--05-16)
13. [攻击技术拆解](#十三攻击技术拆解rpc-投毒)
14. [市场与生态影响汇总](#十四市场与生态影响汇总)
15. [关键人物声明](#十五关键人物声明)
16. [行业意义](#十六行业意义)
17. [参考来源](#十七参考来源)

---

## 一、事件概览

### TL;DR

2026 年 4 月 18 日 17:35 UTC，攻击者通过攻陷 LayerZero 去中心化验证网络（DVN）所依赖的 RPC 节点，伪造跨链消息，从 KelpDAO 的 rsETH OFT Adapter 桥铸造 **116,500 枚无抵押 rsETH**（约 $2.92 亿）。随后将 rsETH 抵押到 Aave V3/V4，借出约 **$2.36 亿 WETH**，引发 Aave 大规模 TVL 流失与潜在坏账危机。事件由 Aave 主导的 **DeFi United** 联盟通过募集 $3.2 亿+ 资金完成救援，并于 5 月 13-15 日重启 rsETH 市场。LayerZero 于 5 月 8-9 日公开道歉，宣布废除 1-of-1 DVN 默认配置；KelpDAO 宣布迁移至 Chainlink CCIP。

### 各方角色

| 角色 | 说明 |
|------|------|
| **rsETH / KelpDAO** | 以太坊流动性再质押协议，rsETH 是其 LRT（液态再质押代币） |
| **LayerZero** | 跨链消息传递协议；KelpDAO 使用其 V2 OFT 桥从 Unichain 跨链到以太坊主网 |
| **Aave** | 去中心化借贷协议；rsETH 被列为抵押品，攻击者用伪造 rsETH 借出大量 WETH |
| **DeFi United** | 由 Aave 主导、多协议联合发起的行业救援联盟 |
| **Lazarus Group** | 朝鲜黑客组织，被 LayerZero 与 Chainalysis 共同归因为本次攻击者 |

### 损失规模

- **被盗 rsETH**：116,500 枚（占 rsETH 流通量 ~18%）
- **市值**：约 $2.92 亿（攻击时刻价格）
- **Aave 借出资产**：约 82,650 WETH + 821 wstETH（合计约 $2.36 亿）
- **Aave 潜在坏账**：$1.237 亿–$2.301 亿（取决于损失分摊方式）
- **DeFi 行业 TVL 48 小时跌幅**：$99.5B → $86.3B（-$13.2B，仅次于 LUNA 崩盘）

---

## 二、LayerZero V2 机制与 DVN 角色

> 理解 DVN 是理解本次攻击的核心前提。

### 2.1 LayerZero V1 vs V2 的演进

#### V1：Oracle + Relayer 模型

- **Oracle**：验证源链区块头（仅确认区块有效性，不确认交易内容）
- **Relayer**：提交交易证明并在目标链执行消息
- **问题**：单一 Relayer 成为瓶颈和单点故障；Relayer 宕机则消息无法投递

#### V2：DVN + Executor 模型

- **DVN（Decentralized Verifier Network）**：取代 Oracle，验证**区块头 + 交易内容（payloadHash）**
- **Executor**：取代 Relayer，**无许可**消息执行
- **核心优势**：
  1. **模块化**：每个应用自由选择验证者组合
  2. **并行化**：多个 DVN 并行验证，无串行瓶颈
  3. **执行解耦**：验证与执行完全独立；已验证消息可被任意 Executor 重试
  4. **容错**：多 DVN 配置下可容忍 f 个 DVN 被攻陷

### 2.2 V2 四大核心组件

#### (1) Endpoint（EndpointV2）

- 部署在每条链上的**不可升级**入口合约
- 以太坊主网地址：`0x1a44076050125825900e736c501f859c50fE728c`
- 管理每个 OApp（Omnichain Application）的 **Security Stack** 配置
- 维护数据包状态机：**Sent → Verified → Received**
- 为出站数据包分配唯一 nonce

#### (2) MessageLib（ULN — Ultra Light Node）

- 按 OApp 安全配置独立运行的库合约
- 当前实现：`SendULN302.sol`（源链）与 `ReceiveULN302.sol`（目标链）

**源链流程：**
1. 接收来自 OApp 的消息
2. 编码数据包，计算 `payloadHash`
3. 向所有配置的 DVN 与 Executor 派发任务
4. 收取每个验证者的费用

**目标链流程：**
1. 接收 DVN 提交的验证任务
2. 检查所有 required DVN 是否已签名 `payloadHash`
3. 检查 optional DVN 是否达到阈值
4. 将已验证数据包状态提交至 Endpoint
5. 允许 Executor 通过 `lzReceive()` 投递消息

#### (3) DVN — Decentralized Verifier Network ⭐

**什么是 DVN？**

DVN 是**链下独立运行**的验证实体（或网络），负责验证跨链消息的真实性与完整性。每个 DVN 对 LayerZero 消息的 `payloadHash`（唯一数字指纹）进行签名，证明该消息确实从源链发出。

**DVN 的核心职责：**

1. **读取源链数据**：通过自有 RPC 节点 / 轻客户端 / 全节点读取数据包
2. **独立验证**：使用独立基础设施验证 payload 完整性
3. **等待确认**：根据配置的区块确认数（如以太坊 5 个块）后才能签名
4. **提交签名**：在目标链调用 `ULN.verify(_packetHeader, _payloadHash, _confirmations)`

**DVN 验证流程：**

```
1. 幂等性检查：
   ULN._verified(_dvn, _headerHash, _payloadHash, _requiredConfirmation)
   → 检查是否已验证过此数据包（防止双签）

2. 提交验证：
   ULN.verify(_packetHeader, _payloadHash, _confirmations)
   → 提交对 payloadHash 的签名

3. 协议提交：
   所有 required DVN 签名后，MessageLib 将 (nonce, payloadHash)
   提交至目标 Endpoint，状态变为 Verified
```

**DVN 激励机制：**

- DVN 按消息计费（由 OApp 通过 Endpoint 支付）
- V2 引入 **EigenLayer CryptoEconomic DVN Framework**：DVN 可质押 ETH/LST 作为信用担保；签名错误消息会被 slash（罚没）

#### (4) Executor

- **无许可**投递已验证消息至目标 OApp
- 调用 `OApp.lzReceive()` 执行消息 payload
- 与验证层完全解耦：任何人都可执行已验证消息

**数据包三态：**
- **Sent**：源 Endpoint 分配 nonce
- **Verified**：所有 required DVN 已签名，已提交至目标 Endpoint
- **Received**：消息已成功执行，OApp 已接收 payload

### 2.3 DVN 配置模型（X-of-Y）

每个 OApp 配置自己的 **Security Stack**：

```typescript
{
  requiredDVNCount: N,         // 必须签名的 DVN 数量
  optionalDVNCount: M,         // 可选 DVN 候选数量
  optionalDVNThreshold: K,     // 可选 DVN 需达到的签名阈值
  requiredDVNs: [...],         // required DVN 地址列表
  optionalDVNs: [...]          // optional DVN 地址列表
}
```

| 配置 | 容错（f）| 攻击难度 | 风险等级 |
|------|---------|---------|---------|
| **1-of-1** | f = 0 | 攻陷 1 个 DVN | **🔴 致命**（KelpDAO 用此配置） |
| **2-of-3** | f = 1 | 同时攻陷 2 个独立 DVN | 🟡 中 |
| **3-of-5** | f = 2 | 同时攻陷 3 个独立 DVN | 🟢 低 |
| **5-of-5** | 不容错但难破解 | 同时攻陷 5 个独立 DVN | 🟢 极低 |

**KelpDAO 事件后 LayerZero 新默认值**：
- **5-of-5**（推荐）
- **3-of-3**（仅有 3 个 DVN 的链的最低要求）
- **LayerZero Labs DVN 不再服务于任何 1-of-1 配置**

### 2.4 OFT（Omnichain Fungible Token）与 OFT Adapter

**OFT** 是 LayerZero 的代币标准，允许 ERC-20 在多条链上以**单一全局资产**存在，而非包装代币。

**两种实现：**

1. **Native OFT**（原生）
   - 每条链都有原生 mint/burn 能力
   - 跨链 = Chain A burn → Chain B mint

2. **OFT Adapter**（适配器，**KelpDAO 采用**）
   - 在已有 ERC-20 的原生链上锁定（lock）原始代币
   - 在其他链上铸造 OFT 代表锁定的资产
   - 返回原生链时：burn OFT → unlock 原始 ERC-20

**KelpDAO 的 OFT 流程（攻击点所在）：**

```
正常流程：
  1. 用户在 Unichain 调用 OFT.send()
  2. Unichain 上 OFT 被 burn
  3. LayerZero 消息发送至 Ethereum 的 OFT Adapter
  4. 安全栈 DVN 验证消息
  5. Executor 投递至 OFT Adapter
  6. Adapter 从 escrow 释放原 rsETH 给目标地址

4月18日攻击：
  1. 攻击者伪造"在 Unichain 上 burn 了 116,500 rsETH"的消息
  2. 1-of-1 DVN（已被 RPC 投毒）签名通过
  3. Ethereum 上 Adapter 释放 116,500 rsETH
  4. 实际上 Unichain 从未发生过 burn —— 跨链桥失衡，资不抵债
```

### 2.5 完整消息流图

```
┌─ SOURCE CHAIN (Unichain) ────────────────────────────────────┐
│  1. OApp 调用 Endpoint.send()                                  │
│  2. Endpoint 分配 nonce N                                      │
│  3. MessageLib 编码 packet，计算 payloadHash                   │
│  4. 派发任务至 DVN 与 Executor                                 │
│  状态：SENT                                                    │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─ DESTINATION CHAIN (Ethereum) - 验证阶段 ─────────────────────┐
│  5. DVN 独立查询源链（自有 RPC / 轻客户端）⚠️ 攻击点         │
│  6. 验证 packet header + payload                              │
│  7. 等待 N 个区块确认                                          │
│  8. DVN.signAndCall(ULN.verify(...))                          │
│  9. MessageLib 检查 required + optional 阈值                   │
│ 10. 提交 (nonce, payloadHash) 至 Endpoint                     │
│  状态：VERIFIED                                                │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌─ DESTINATION CHAIN - 执行阶段 ────────────────────────────────┐
│ 11. Executor 检测到 Verified 数据包                            │
│ 12. 调用 OApp.lzReceive(...)                                  │
│ 13. OFTAdapter 释放/铸造代币                                   │
│  状态：RECEIVED                                                │
└───────────────────────────────────────────────────────────────┘
```

### 2.6 为什么 1-of-1 在 KelpDAO 案例中是致命的

- **没有第二意见**：单 DVN 签名通过即视为合法，无任何复核
- **攻击面集中**：所有 RPC 节点 / API key / 签名者都属于同一组织
- **f = 0**：不容忍任何故障或妥协
- **本次攻击成立的全部条件**：
  1. 仅需攻陷 LayerZero Labs 一个 DVN
  2. 仅需投毒其使用的两个 RPC 节点
  3. 加上对未被攻陷节点的 DDoS

若是 2-of-3 或 3-of-5 配置，攻击者必须**同时**攻陷多个独立组织运营的独立基础设施，难度成数量级上升。

---

## 三、根本漏洞分析：1-of-1 DVN 默认配置

| 维度 | 详情 |
|------|------|
| **漏洞类型** | 安全栈配置缺陷（非智能合约漏洞、非密码学漏洞） |
| **漏洞来源** | LayerZero quickstart 文档默认值 + GitHub 模板默认 1-of-1 |
| **行业普遍性** | Blockaid 审计显示 **40% 的 LayerZero 活跃协议**仍在使用 1/1 单验证者配置 |
| **KelpDAO 责任** | 沿用 LayerZero 推荐的默认配置，未升级到多 DVN |
| **LayerZero 责任** | 默认值激进、文档误导、Labs DVN 接受 1-of-1 部署 |

---

## 四、攻击前隐患（2024-01 — 2026-04-17）

| 时间 | 事件 |
|------|------|
| **2024-01** | KelpDAO 推出 rsETH，使用 LayerZero V2 OFT；DVN 配置为 **1-of-1（仅 LayerZero Labs DVN）**。据 KelpDAO 后续披露，该配置**由 LayerZero 官方文档默认推荐并审核批准** |
| **2024–2026** | LayerZero GitHub quickstart 与默认配置文件持续以 1-of-1 DVN 出货 |
| 攻击前数月 | 无任何重大公开警告、治理帖或安全公司专门标记此配置风险 |
| **2026-04-18 ~07:35 UTC** | 攻击者从 **Tornado Cash 1 ETH 池**获取启动资金，预先注资 6 个攻击钱包（典型 Lazarus 手法） |

---

## 五、链上数据与关键地址

### 5.1 关键合约地址

| 角色 | 地址 | 链 |
|------|------|----|
| **KelpDAO rsETH OFT Adapter**（攻击释放点） | `0x85d456B2DfF1fd8245387C0BfB64Dfb700e98Ef3` | Ethereum |
| **LayerZero Endpoint V2** | `0x1a44076050125825900e736c501f859c50fE728c` | Ethereum |
| **被攻陷的 LayerZero Labs DVN** | `0x589dedbd617e0cbcb916a9223f4d1300c294236b` | Ethereum |

### 5.2 攻击者地址

| 类型 | 地址 |
|------|------|
| **攻击者主 EOA**（116,500 rsETH 接收地址） | `0x8B1b6c9A6DB1304000412dd21Ae6A70a82d60D3b` |
| **其他追踪地址（部分）** | `0x1F4C1c2e...b0db3adeF`、`0x5d3919f1...90c257ccc` |
| **ZachXBT 标记钱包总数** | 6 个（全部地址未在公开报道中完整列出，主要通过 Telegram 私享） |

### 5.3 链上事件锚点

| 数据 | 值 |
|------|---|
| **攻击区块高度（Ethereum）** | 24,908,285 |
| **攻击时间戳** | 2026-04-18 17:35 UTC |
| **被铸 rsETH 数量** | 116,500 |
| **Aave Ethereum 抵押** | 89,567 rsETH |
| **Aave Ethereum 借出** | 52,834 WETH |
| **Aave Arbitrum 抵押** | 36,167 rsETH（部分通过桥转入） |
| **Aave Arbitrum 借出** | 29,782 WETH + 821 wstETH |
| **总借出价值** | ~$1.9086 亿（WETH 部分）+ wstETH，合计约 $2.36 亿 |
| **THORChain 转出量（4月21日）** | 75,701 ETH（~$1.7541 亿）|
| **Arbitrum 安全委员会冻结量** | 30,765.67 ETH |
| **美国法院争议金额** | ~$7,100 万（冻结 ETH 子集） |

### 5.4 已公开 / 未公开 数据明细

**✅ 已公开**：
- 攻击时间、规模、区块高度
- 主攻击者 EOA：`0x8B1b6c9A...`
- 涉及合约地址（OFT Adapter、Endpoint V2、被攻陷 DVN）
- KelpDAO pause、Aave 冻结的大致时间（分钟级）
- 聚合资金流向（Aave 抵押/借出 / THORChain swap 总量）
- 归因 Lazarus Group / TraderTraitor

**❌ 未公开**（截至 2026-05-16）：
- 初始 mint 交易具体 hash
- 全部 6 个攻击者钱包地址
- Aave 抵押/借出每笔交易 hash
- 两次回滚的二次铸造尝试 hash
- KelpDAO pause 多签交易 hash
- Aave Guardian 冻结操作 hash
- THORChain swap 具体 swap ID
- Tornado Cash 出金交易 hash

> **说明**：本文档仅引用已被链上分析公司（Chainalysis、Arkham、Blockaid、Hypernative 等）或主流加密媒体公开披露的数据，未公开数据明确标注，避免编造哈希。

---

## 六、小时级攻击时间线（2026-04-18 UTC）

### 攻击执行阶段

| UTC 时间 | 事件 |
|----------|------|
| **~17:20 (10:20 AM PT)** | 攻击者对 LayerZero DVN 未被攻陷的备用 RPC 节点发起 **DDoS 攻击**（持续约 80 分钟） |
| 同期 | 已被攻陷的**两个独立 op-geth RPC 节点**（不同集群）替换二进制文件，对 DVN 提供伪造数据，对其他系统返回正常数据；节点被编程为攻击窗口结束后**自毁** |
| **17:35** | DVN 故障转移至被投毒的 RPC 节点 → 攻击者在以太坊主网（block 24,908,285）铸造 **116,500 rsETH** |
| **17:35–18:20** | 攻击者向 Aave V3 存入 89,567 rsETH，跨 Ethereum + Arbitrum 借出约 $1.9 亿 WETH + wstETH |
| **~17:55** | **ZachXBT** 在公开 Telegram 频道发出首个预警，标记 6 个攻击者钱包地址（漏出后 ~20 分钟） |

### 应急响应阶段

| UTC 时间 | 事件 |
|----------|------|
| **18:21**（事发后 46 分钟） | **KelpDAO 紧急暂停多签**调用 `pauseAll`，冻结协议核心合约 |
| **18:26** | 攻击者尝试**第二次铸造 ~40,000 rsETH（~$9,500 万）** → **回滚** |
| **18:28** | 攻击者尝试**第三次铸造 ~40,000 rsETH** → **回滚** + 钱包被拉黑 |
| **18:52**（事发后 ~77 分钟） | **Aave Guardian** 跨 5 条链冻结 rsETH/wrsETH 市场，LTV 设为 0 |
| **当晚** | SlowMist（余弦）率先披露技术细节，指明 1-of-1 DVN 是根因 |

### 4月19日 02:28 UTC

Aave Guardian 进一步冻结 WETH 市场——但此时 Ethereum Core 池 WETH 流动性已从 $6.89 亿被借光至仅剩 $150 万。

---

## 七、危机首日（2026-04-19）

| 事件 | 影响 |
|------|------|
| **Aave TVL 24 小时内从 $26.4B 跌至 ~$20B** | -$6.6B（-25%） |
| **DeFi 总 TVL 48 小时内从 $99.5B 跌至 $86.3B** | LUNA 崩盘以来最严重双日跌幅 |
| **AAVE 代币** | -16% 至 -18%，跌至 2024 年 8 月以来最低 |
| **ZRO 代币** | -20% 至 -24%，跌至 ~$1.50 中段 |
| **Aave 暂停 AAVE 代币回购** | 保留 DAO 财库应对潜在坏账 |
| **ZachXBT 持续追踪** | 公开攻击者地址与混币跳点 |

---

## 八、官方报告与互相指责（2026-04-20）

### LayerZero 首份声明

LayerZero 发布 *KelpDAO Incident Statement*：

> "事件**完全孤立于 KelpDAO 的配置选择**……协议**完全按预期运行**。该攻击为**高度精密的国家级行为者所为，极可能为朝鲜 Lazarus Group，具体为 TraderTraitor 子分支**。"

同时发布技术 post-mortem，公开 RPC 投毒攻击机制。

### Aave 官方事件报告

发布于 [Aave Governance](https://governance.aave.com/t/rseth-incident-report-april-20-2026/24580)：

| 场景 | rsETH 折价 | Aave 坏账 |
|------|----------|----------|
| 损失均摊（场景 1） | 15.12% | **$1.237 亿** |
| 集中在 L2（场景 2） | Arbitrum 单独短缺 26.67% | **$2.301 亿**（其中 Arbitrum $8,840 万） |

### KelpDAO 反击

> "1-of-1 DVN 配置正是 **LayerZero 自己的默认设置和 quickstart 文档所推荐**的。rsETH 于 2024 年 1 月上线时，该配置经过 **LayerZero 团队批准**。"
> — KelpDAO 联合创始人 Amitej Gajjala

**Stani Kulechov（Aave 创始人）**个人承诺捐赠 **5,000 ETH（约 $1,170 万）**。

---

## 九、资金追踪与洗钱（2026-04-21 — 04-22）

| 日期 | 事件 |
|------|------|
| **4月21日** | Arkham Intelligence 追踪到攻击者将 **75,701 ETH（~$1.7541 亿）**转入新建钱包；大部分通过 **THORChain** 跨链 swap 为 BTC |
| 同期 | THORChain 因本次事件获得约 **$91 万**手续费 |
| 同期 | 攻击者还使用 **Umbra（隐私协议）**进一步混淆部分资金 |
| **4月22日** | OFAC 关注度上升；攻击者钱包与 OFAC Lazarus SDN 列表关联地址被打标 |

---

## 十、DeFi United 联盟与方案细化（2026-04-23 — 04-28）

### 4月23日 — Aave 正式宣布 DeFi United

由 **Aave Labs 主导**，多协议联合：Aave DAO、Lido、Ether.fi、LayerZero、Mantle、Compound、KelpDAO。

### 4月25日 — Arbitrum Constitutional AIP

Aave Labs 联合 KelpDAO、LayerZero、EtherFi、Compound 在 Arbitrum 提交宪法级 AIP，请求释放 **Arbitrum 安全委员会冻结的 30,765.67 ETH** 用于恢复计划。Temperature check 持续至 5 月 7 日。

### 4月27日 — 资金到位

DeFi United 锁定约 **$1.6-1.61 亿 ETH** 承诺。

### 4月28日 — 技术恢复方案

- 两周内向以太坊主网 LayerZero OFT 适配器**逐步注入 117,132 枚 rsETH**（精确匹配被盗数量）
- 资金来源：**Aave Recovery Guardian + Kelp Recovery Safe**
- 入金地址：`defiunited.eth`

### 承诺明细

| 出资方 | 金额 | 结构 |
|--------|------|------|
| **Mantle** | 30,000 ETH | 3 年期信贷便利，利率 = Lido 质押年化 + 1% |
| **Aave DAO** | 25,000 ETH | 财库直接出资 |
| **Stani Kulechov 个人** | 5,000 ETH | 个人捐赠 |
| **Ether.fi** | 5,000 ETH | 直接出资 |
| **LayerZero** | 5,000 ETH | 直接出资 |
| **Lido DAO** | 最多 2,500 stETH | 备用承诺 |
| **合计（首期）** | **$1.6-1.61 亿** | |
| **最终总募集** | **$3.2 亿+** | 超过最大坏账缺口 |

---

## 十一、法律与治理博弈（2026-05-01 — 05-12）

### 5月1日

Arbitrum DAO 正式对释放冻结 30,765 ETH 发起治理投票。

### 5月5日

KelpDAO 提交额外文件证明 LayerZero **2024 年曾正式批准其 1-of-1 DVN 配置**——升级公关攻势。

### 5月6日 — 美国曼哈顿联邦法院听证

**两组索赔人**就被冻结的 **$7,100 万 ETH** 争夺权利：
1. **DeFi United 联盟**（恢复 rsETH 抵押）
2. **朝鲜绑架受害者律师团**——依据 2015 年针对平壤的判决，主张对 Lazarus 关联资产的优先索赔权

### 5月8-9日 — LayerZero 公开道歉

LayerZero 发布完整道歉声明：

> "**我们在过去三周的沟通工作做得很糟糕**……我们犯了一个错误，**允许我们的 DVN 在高价值交易中作为 1/1 DVN 运行**。"

**结构性改革**：
- 终止支持 **1-of-1 DVN 配置**
- 默认配置升级为 **5-of-5**（部分仅有 3 DVN 的链最低 3-of-3）
- 与 Aave 系统性合作审计

### 5月8-9日（同期）

**Arbitrum DAO 通过**释放冻结 ETH 的议案——即便面临美国法院的扣押申请。

### 5月12日

Arbitrum 安全委员会对 **$7,100 万**攻击者资产实施**协议层锁定**，等待法律裁决。KelpDAO + Aave 公布协调重启方案。

---

## 十二、协议重启与基础设施迁移（2026-05-13 — 05-16）

### 5月13日 — 重启启动

Aave 将**第一批 25,000 rsETH** 转入以太坊主网 LayerZero OFT 适配器。117,132 rsETH 将在两周内分批注入。

### 5月14-15日 — rsETH 赎回重新开放

- **KelpDAO rsETH 提现功能上线**——自 4 月 18 日以来首次（暂停 28 天）
- **Aave 在 5 条链上解冻 rsETH 市场**：Ethereum Core、Arbitrum、Base、Linea、Mantle
- 汇率调整以反映暂停期累积的质押收益

### 5月15-16日 — LayerZero 客户大逃离

- **KelpDAO** 正式宣布迁移至 **Chainlink CCIP**
- **Solv Protocol** 跟进确认离开 LayerZero
- 业内估算 **近 $20 亿协议资产正在向 Chainlink CCIP 迁移**
- KelpDAO 成为**首个大规模离开 LayerZero 的主流协议**

---

## 十三、攻击技术拆解（RPC 投毒）

### 步骤分解

1. **侦察阶段**：攻击者获取 LayerZero Labs DVN 使用的 RPC 节点列表（疑似通过供应链或凭证窃取）
2. **持续渗透**：攻陷两个位于**完全不同集群**的 op-geth 节点（无直接连接）
3. **二进制替换**：植入自定义 payload
   - 对 DVN 返回伪造数据
   - 对其他客户端返回真实数据（避免被察觉）
4. **触发**：对未被攻陷的备用 RPC 发起 DDoS（10:20–11:40 AM PT），迫使 DVN 故障转移至被投毒节点
5. **执行**：在 DVN 上验证伪造的 Unichain → Ethereum 跨链消息，铸造 rsETH
6. **自毁**：被攻陷节点执行预置自毁脚本，擦除二进制、日志、配置——取证极为困难

### 归因证据链

| 证据 | 来源 |
|------|------|
| 攻击钱包资金来自 Tornado Cash | Chainalysis 链上分析 |
| 攻击节点二进制特征 | LayerZero 内部取证 |
| 资金通过 THORChain → BTC 的洗钱路径 | Arkham Intelligence |
| 与历史 Lazarus 操作的 TTPs 匹配 | LayerZero、Chainalysis 共同结论 |

---

## 十四、市场与生态影响汇总

### 代币价格反应

| 代币 | 即时影响 | 月度影响 |
|------|---------|---------|
| **ZRO** | -20% 至 -24%，跌至 ~$1.50 中段 | 当月跌约 24%，因协议迁移恐慌持续承压 |
| **AAVE** | -16% 至 -18% | 跌至自 2024 年 8 月以来最低 |
| **rsETH** | 暂停前折价 15.12%（理论情景） | 重启后逐步回归锚定 |

### TVL 变动

| 协议 | 变动 |
|------|------|
| **Aave** | $26.4B → ~$20B（-25%，48 小时内） |
| **DeFi 总 TVL** | $99.5B → $86.3B（-13%，48 小时内） |
| **KelpDAO** | 暂停 28 天（4月18日 — 5月15日） |
| **LayerZero 生态** | ~$20 亿资产向 Chainlink CCIP 迁移 |

### 治理与文档动作

- **Aave**：ARFC（4月20日）→ AIP（财政援助提案）→ Arbitrum Constitutional AIP（4月25日）
- **Arbitrum DAO**：5月1日发起投票，5月8-9日通过
- **LayerZero**：终止 1/1 DVN 支持，默认升级 5/5

---

## 十五、关键人物声明

### Bryan Pellegrino (LayerZero CEO)
- **4月20日**：发布初始声明否认 LayerZero 责任
- **5月8日**：公开道歉："我们在过去三周的沟通工作做得很糟糕。"

### Stani Kulechov (Aave 创始人)
- 个人承诺 5,000 ETH（~$1,170 万）
- 主导 DeFi United 联盟
- 业内评价为本次危机中**最强的协调领导者**

### Amitej Gajjala (KelpDAO 联合创始人)
- 强调 LayerZero 应承担默认配置责任
- 宣布迁移至 Chainlink CCIP

### ZachXBT
- 漏出后约 20 分钟内识别首批洗钱跳点
- 公开 6 个攻击者钱包地址

---

## 十六、行业意义

### 短期影响
- 跨链桥安全性的最严重事件之一（与 Ronin $6.2 亿、Wormhole $3.2 亿、Harmony $1 亿 同级）
- 单一中心化基础设施依赖（默认 1/1 DVN）的危险性被血淋淋揭示
- DeFi 集体救援机制（DeFi United）首次大规模成功运转

### 长期影响
- **跨链消息验证范式转变**：从"信任默认值"转向"多验证者强制要求"
- **Chainlink CCIP vs LayerZero** 的市场份额重新洗牌
- 推动 OFAC、美国法院介入 DeFi 资产冻结的法律先例
- 重提对 Lazarus Group 在加密领域威胁的全球警觉
- LayerZero EigenLayer CryptoEconomic DVN Framework 加速落地

---

## 十七、参考来源

### 攻击事件报道

- [The Block — 攻击首报](https://www.theblock.co/post/397988/kelp-daos-rseth-bridge-apparently-exploited-for-roughly-292-million-in-layerzero-based-attack)
- [CoinDesk — Kelp DAO 被攻击](https://www.coindesk.com/tech/2026/04/19/2026-s-biggest-crypto-exploit-kelp-dao-hit-for-usd292-million-with-wrapped-ether-stranded-across-20-chains)
- [CoinDesk — Aave TVL 暴跌](https://www.coindesk.com/tech/2026/04/19/aave-records-usd6-billion-tvl-drop-as-kelp-hack-exposes-structural-risk-at-defi-lender/)
- [CoinDesk — Kelp 反击 LayerZero](https://www.coindesk.com/tech/2026/04/20/kelp-dao-claims-layerzero-s-default-settings-are-what-actually-caused-the-usd290-million-disaster)
- [CoinDesk — Arbitrum 通过释放议案](https://www.coindesk.com/markets/2026/05/08/arbitrum-delegates-back-usd71-million-eth-recovery-plan-despite-u-s-seizure-fight)
- [The Defiant — DeFi United 详细方案](https://thedefiant.io/news/defi/defi-united-outlines-technical-path-to-make-kelp-s-rseth-whole)
- [The Block — DeFi United 技术方案](https://www.theblock.co/post/399118/defi-united-detailed-plan)
- [The Block — LayerZero 道歉](https://www.theblock.co/post/400629/layerzero-issues-public-apology-for-kelp-dao-exploit-response-admits-fault-in-single-verifier-setup)
- [Bleeping Computer — Lazarus 归因](https://www.bleepingcomputer.com/news/security/kelpdao-suffers-290-million-heist-tied-to-lazarus-hackers/)
- [Bloomberg — 朝鲜绑架案受害者索赔](https://en.bloombergbit.io/feed/news/111710)

### 链上分析与技术拆解

- [Chainalysis 深度技术拆解](https://www.chainalysis.com/blog/kelpdao-bridge-exploit-april-2026/)
- [Blockaid — DVN 配置审计](https://www.blockaid.io/blog/how-a-single-layerzero-dvn-compromise-drained-292m-from-kelpdao)
- [Hypernative — 观察层漏洞分析](https://www.hypernative.io/blog/the-kelpdao-observation-layer-exploit-291m-released-on-a-message-that-never-existed)
- [Arkham — 黑客资金追踪](https://info.arkm.com/research/kelpdao-hacker-moving-funds-attacker-transfers-175-41m-to-new-addresses)
- [Chainstack — RPC 投毒攻击分析](https://chainstack.com/rpc-poisoning-attacks-crypto-kelp-dao-exploit/amp/)
- [Unchained — THORChain 资金路径](https://unchainedcrypto.com/kelp-dao-exploiter-moves-175-million-in-stolen-eth-into-new-wallets-routing-funds-through-thorchain/)
- [BeeInCrypto — Arbitrum 冻结](https://beincrypto.com/arbitrum-freezes-eth-kelpdao-exploit/)
- [DeFi Prime — 综合分析](https://defiprime.com/kelpdao-rseth-exploit)
- [Messari — 综合报告](https://messari.io/report/the-rseth-exploit)
- [KuCoin — 技术机制解析](https://www.kucoin.com/blog/my-kelpdao-rseth-exploit-how-292m-layerzero-bridge-attack-created-177m-bad-debt-on-aave)

### 官方声明与治理

- [LayerZero 事件声明](https://layerzero.network/blog/kelpdao-incident-statement)
- [LayerZero 道歉与更新](https://layerzero.network/blog/an-overdue-apology)
- [Aave Governance — 事件报告](https://governance.aave.com/t/rseth-incident-report-april-20-2026/24580)
- [Aave Governance — 事件追踪](https://governance.aave.com/t/rseth-incident-2026-04-18/24481)
- [CryptoTimes — 重启与提现重开](https://www.cryptotimes.io/2026/05/15/kelp-dao-rseth-withdrawals-go-live-as-aave-unpauses-markets/)
- [CryptoTimes — 恢复方案](https://www.cryptotimes.io/2026/05/13/kelp-dao-aave-set-to-resume-rseth-operations-after-292m-exploit-recovery/)
- [News.Bitcoin — DeFi United $1.6 亿筹资](https://news.bitcoin.com/defi-united-secures-160m-as-industry-moves-to-cover-aave-bad-debt-crisis/)
- [News.Bitcoin — ZachXBT 预警](https://news.bitcoin.com/zachxbt-flags-280m-kelpdao-exploit-hitting-ethereum-defi-lending-markets/)
- [EGW News — LayerZero 用户外流](https://egw.news/crypto/news/34682/mass-exodus-from-layerzero-kelpdao-and-solv-protoc-yumh0TAIl/)

### LayerZero 协议文档

- [LayerZero Docs — DVN 概述](https://docs.layerzero.network/v2/workers/off-chain/dvn-overview)
- [LayerZero Docs — V2 概览](https://docs.layerzero.network/v2/concepts/v2-overview)
- [LayerZero Docs — OFT 标准](https://docs.layerzero.network/v2/home/token-standards/oft-standard)
- [LayerZero Docs — OFT Adapter](https://docs.layerzero.network/v2/developers/evm/oft/adapter)
- [LayerZero Docs — DVN/Executor 配置](https://docs.layerzero.network/v2/developers/evm/configuration/dvn-executor-config)
- [LayerZero Docs — Message Packet](https://docs.layerzero.network/v2/home/protocol/packet)
- [LayerZero Medium — V2 深度解析](https://medium.com/layerzero-official/layerzero-v2-deep-dive-869f93e09850)
- [LayerZero Medium — DVN 解释](https://medium.com/layerzero-official/layerzero-v2-explaining-dvns-02e08cce4e80)
- [LayerZero Medium — EigenLayer CryptoEconomic DVN Framework](https://medium.com/layerzero-official/layerzero-x-eigenlayer-the-cryptoeconomic-dvn-framework-68af27ca2040)

---

**文档版本**：v1.0
**最后更新**：2026-05-16
**整理者说明**：本文档基于截至 2026-05-16 公开报道整理。部分链上交易哈希尚未在公开渠道披露，已在第五章明确标注。事件后续发展（如美国法院最终判决、攻击者资金最终去向）请关注 Aave Governance、KelpDAO 官方频道与 Chainalysis 持续报告。
