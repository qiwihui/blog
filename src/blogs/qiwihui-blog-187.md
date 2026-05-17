# alt.fun 平台机制全面分析报告

> Issue: #187  
> State: open  
> Source: [https://github.com/qiwihui/blog/issues/187](https://github.com/qiwihui/blog/issues/187)


> **平台地址**：[https://alt.fun](https://alt.fun)  
> **文档**：[https://docs.alt.fun](https://docs.alt.fun)  
> **核心合约（Zap）**：[0xb318e2ab...aa8758feb](https://hyperevmscan.io/address/0xb318e2ab995d805cb0c5b97c39edda0aa8758feb#code)  
> **链**：HyperEVM Mainnet  
> **报告日期**：2026-05-16

---

## 一、平台概述

**alt.fun** 是部署在 HyperEVM 上的代币发射平台（Token Launchpad）。与 Pump.fun 等传统平台的根本区别在于：**每个代币的 Bonding Curve 储备资产不是 SOL/ETH/HYPE，而是 BounceTech 的杠杆代币（Leveraged Token，LT）** —— 一种封装了 Hyperliquid 永续合约头寸的 ERC-20 代币。

这使得代币价格由两个因素共同驱动：

1. **用户的买卖交易活动**（传统 Bonding Curve 机制）
2. **底层永续合约标的资产的价格走势**（放大 2x / 3x / 5x）

**结果**：代币在无任何人交易的情况下，也会因底层资产价格变动而涨跌。

### 整体技术栈

```
用户 (USDC)
    │
    ▼
alt.fun Zap 合约 (HyperEVM)
    │
    ├─── BounceTech（铸造 / 赎回 LT）
    │         │
    │         └─── Hyperliquid Perps（实际永续合约仓位）
    │
    └─── 毕业后 ───▶ HyperSwap V2（代币 / LT 交易对）
```

---

## 二、代币创建机制

### 2.1 创建者可选参数

| 参数 | 可选项 |
|------|--------|
| 底层资产 | HYPE、BTC、ETH、SOL、PAXG |
| 方向 | Long（做多）/ Short（做空）|
| 杠杆倍数 | 2x、3x、5x |

### 2.2 协议固定参数

| 参数 | 数值 |
|------|------|
| 代币总供应量 | 10 亿枚（1,000,000,000） |
| 进入 Bonding Curve | 75%（7.5 亿枚） |
| 留给毕业后 LP | 25%（2.5 亿枚） |
| 最低初始买入（创建者） | $20 USDC |
| 最低单笔买入 | $20 USDC |
| 最低单笔卖出 | $12 USDC |
| 合约地址特征 | 末尾 5 个零（`...00000`） |

### 2.3 创建者权益
- 绑定创建者地址，永久享有所有交易 **0.25% 创建者费用**（含毕业后）
- 可更换费用接收地址
- 代币元数据（名称、图片、描述）创建后不可修改

---

## 三、Bonding Curve 核心机制

### 3.1 与传统 Pump.fun 的本质区别

```
传统 Pump.fun：
  储备资产 = SOL（价值静态）
  代币价格 ← 仅由用户买卖驱动

alt.fun：
  储备资产 = Leveraged Token（LT，价值随标的资产动态变化）
  代币价格 ← 用户买卖 + 底层资产涨跌 × 杠杆倍数
```

### 3.2 买入流程

```
用户输入 USDC
    │
    ▼
Zap 合约调用 BounceTech 铸造 LT
    │
    ▼
LT 进入 Bonding Curve 储备
    │
    ▼
用户按曲线当前价格获得代币
```

### 3.3 卖出流程

```
用户输入代币
    │
    ▼
代币归还 Bonding Curve
    │
    ▼
从储备取出等价 LT
    │
    ▼
BounceTech 将 LT 赎回为 USDC（收 0.3% 赎回费）
    │
    ▼
用户收到 USDC
```

### 3.4 曲线价值的双向变动

曲线 USD 价值 = 储备中所有 LT 的当前 USD 市值

| 事件 | 曲线 USD 价值 | 代币价格 |
|------|-------------|---------|
| 用户买入 | ↑ 增加 | ↑ 上涨 |
| 用户卖出 | ↓ 减少 | ↓ 下跌 |
| LT 升值（标的资产顺向运动） | ↑ 增加 | ↑ 上涨 |
| LT 贬值（标的资产逆向运动） | ↓ 减少 | ↓ 下跌 |

### 3.5 典型示例

> **代币**：HYPE 3x Long  
> **初始买入**：$100（创建者）  
> **24 小时内**：HYPE 价格上涨 10%，**零交易**  
> **结果**：HYPE 3x Long LT 升值约 30%，创建者持仓变为 ~**$130**  
> **纯靠底层资产上涨实现，无需任何新买盘**

---

## 四、杠杆代币（LT）的特性

LT 由 **BounceTech** 发行，通过**自动再平衡**维持目标杠杆倍数（如 3x），并封装为标准 ERC-20。

### 4.1 优势
- **无清算风险**：即使杠杆漂移也不会被强制平仓
- **单边趋势中收益放大**：HYPE 涨 10% → 3x LT 涨 ~30%
- **可在 AMM 上直接交易**：毕业后作为配对资产继续流通

### 4.2 波动率损耗（Volatility Decay）

在**震荡横盘**市场中，LT 自动再平衡会将波动率转化为价值损耗：

```
示例（3x Long，初始 $100）：
  Day 1：标的涨 10% → LT 价值 $130
  Day 2：标的跌 9.09%（回到原价）→ LT 价值 $130 × (1 - 3×9.09%) ≈ $95.5
  净效果：标的回原点，LT 损失 4.5%
```

- **杠杆越高，损耗越大**：5x LT 在震荡市中损耗远大于 2x
- **对 alt.fun 的影响**：横盘行情下，即使无净卖出，曲线 USD 价值也会因 LT 损耗持续缩水，毕业门槛越来越难以达到

---

## 五、毕业机制（Graduation）

### 5.1 触发条件（满足其一即触发）

1. **Bonding Curve 上的代币被全部购买完毕**
2. **Bonding Curve 中 LT 的 USD 价值达到 $9,000**

### 5.2 毕业执行
- 75% 的代币 + 对应 LT → 迁移至 **HyperSwap V2** 创建流动性池
- 配对资产：**Token / LT**（而非 Token / USDC）
- 流动性通过 **LPLock.sol** 锁定（防止创建者撤池）

### 5.3 毕业后特性
- 代币成为标准 ERC-20，在 HyperSwap 上自由交易
- **杠杆属性延续**：持有代币 = 间接暴露于底层资产的杠杆走势
- 创建者费用 0.25% 继续在毕业后交易中计提

### 5.4 毕业阈值的双向性（关键风险点）

**$9K 门槛会后退**：

```
示例：
  曲线价值达到 $8,500（接近毕业）
  底层资产突然逆向暴跌 20%（对 3x Long 而言 LT 跌 60%）
  曲线价值瞬间跌至 $3,400
  离毕业门槛倒退了 $5,600
```

这是 alt.fun 与所有其他 Launchpad 最大的不同之处：**即将毕业的代币可能因行情逆转而永久无法毕业**。

---

## 六、费用结构

### 6.1 平台直接费用

| 操作 | 总费率 | 协议收取 | 创建者收取 |
|------|--------|---------|-----------|
| 买入（曲线） | 0.75% | 0.50% | 0.25% |
| 卖出（曲线） | 0.75% | 0.50% | 0.25% |
| 买入（毕业后） | HyperSwap 设定 | — | 0.25% 继续 |
| 卖出（毕业后） | HyperSwap 设定 | — | 0.25% 继续 |
| 合约最大费率上限 | **2%（200 BPS）** | 硬编码 | 硬编码 |

### 6.2 外部费用（用户间接承担）

| 类型 | 费率 | 收取方 | 触发时机 |
|------|------|--------|---------|
| LT 赎回费 | **0.3%**（名义价值）| BounceTech | 每次卖出兑换 USDC 时 |
| Hyperliquid 交易费 | 由 LT 内部承担 | Hyperliquid | LT 持有期间持续 |
| HyperSwap Swap 费 | HyperSwap V2 设定 | HyperSwap | 毕业后每笔交易 |

### 6.3 卖出实际总费用估算（曲线期间）

```
平台 Sell 费：0.75%
BounceTech 赎回费：0.30%
合计约：1.05%（不含 Hyperliquid 内部费）
```

---

## 七、合约架构分析

**主入口合约**：`Zap.sol`（UUPS 可升级代理）  
地址：`0xb318e2ab995d805cb0c5b97c39edda0aa8758feb`

### 7.1 合约文件结构

| 合约文件 | 核心职责 |
|----------|---------|
| **Zap.sol** | 用户入口；USDC↔LT 路由；buy/sell 封装 |
| **Bonding.sol** | Bonding Curve 逻辑；每个代币的储备状态 |
| **Router.sol** | 曲线 vs AMM 的路由判断 |
| **Factory.sol** | 用 Clones 最小代理批量部署 Token 合约 |
| **Token.sol** | 每个发射代币的 ERC-20（含 Permit）|
| **Pair.sol** | 毕业后 AMM Pair 合约 |
| **FeeVault.sol** | 费用归集与分发 |
| **LPLock.sol** | 毕业后流动性锁定 |

### 7.2 关键接口

```solidity
// Zap.sol 主要函数
function createToken(...)                 // 创建新代币
function createTokenWithPermit(...)       // 无需预先 approve 创建
function buy(address token, uint usdcIn, uint minOut, address referrer)
function sell(address token, uint tokenIn, uint minOut)
function buyWithPermit(...)               // EIP-2612 无 gas approve 买入
function sellWithPermit(...)              // EIP-2612 无 gas approve 卖出

// 管理函数
function setBonding(address)              // 更新 Bonding 合约
function setFeeVault(address)             // 更新费用接收地址
function setFees(uint buy, uint sell, uint creator)  // 调整费率
```

### 7.3 安全机制

| 机制 | 作用 |
|------|------|
| **ReentrancyGuard** | 防止重入攻击 |
| **SafeERC20** | 安全的 ERC-20 转账（防 approve race） |
| **UUPS Proxy** | 可升级合约（Owner 权限）|
| **Ownable2Step** | 两步所有权转移，防意外移交 |
| **Clones** | 最小代理部署 Token，节省 gas |
| **Permit 支持** | EIP-2612，用户可免 approve 交易 |

---

## 八、风险评估

### 8.1 🔴 高风险：组合性（Composability）风险

平台强依赖三个外部协议：

```
BounceTech 故障 → LT 无法铸造/赎回 → 所有代币无法买卖
Hyperliquid 故障 → LT 价值归零 → 所有曲线储备归零
HyperSwap 故障 → 毕业后代币无法交易
```

任意一环出现漏洞、宕机或流动性危机，都将影响平台上所有代币。

### 8.2 🔴 高风险：大额卖出非原子性

大额卖出（LT 赎回超出 BounceTech 单笔限制）会导致**交易 revert**，用户须手动操作：
1. 先在 AMM 上将代币换为 LT
2. 再去 BounceTech 将 LT 赎回为 USDC

**散户风险**：普通用户可能不知道这个机制，反复尝试大额卖出都会失败，造成时间和 gas 损失。

### 8.3 🟡 中风险：波动率损耗 + 毕业倒退

- 震荡横盘行情下，LT 持续损耗 → 曲线价值缩水 → 毕业遥遥无期
- 高杠杆（5x）代币在 20% 逆向行情下 LT 价值几乎归零

### 8.4 🟡 中风险：合约可升级性

Zap 合约采用 UUPS 代理，Owner 可升级逻辑合约，理论上可修改：
- 费率（上限 2%，但下限无保护）
- Bonding 合约地址（可指向恶意合约）
- FeeVault 地址（可劫持费用流）

用户需完全信任团队，且合约无 Timelock 保护。

### 8.5 🟡 中风险：创建者激励错配

- 创建者永久享有 0.25% 费用
- 创建者有动机：制造高换手率（拉高交易量），在高点 dump，留下接盘者
- 最低 $20 创建门槛极低，垃圾代币泛滥成本几乎为零

### 8.6 🟢 低风险：默认 10% 滑点

平台默认 10% 滑点容忍度较高，用户可能在不知情下以较差价格成交。

### 8.7 审计状态

**审计机构**：[Phage Security](https://phagesecurity.com)（审计员：Pyro、BengalCatBalu、Kvarr）  
**审计日期**：2026-05-14  
**审计代码版本**：Commit `474837d`；修复版本：Commit `f7f953b`  
**总体评价**：*"The codebase is in good shape for mainnet."*（代码库状态良好，可部署主网）

#### 发现汇总

| 严重程度 | 数量 | 已修复 | 已确认（未修复）|
|---------|------|--------|--------------|
| 🔴 Critical | 0 | — | — |
| 🟠 High | 0 | — | — |
| 🟡 Medium | 2 | 1 | 1 |
| 🔵 Low | 8 | 4 | 4 |
| **合计** | **10** | **5** | **5** |

#### Medium 级发现

| ID | 标题 | 状态 |
|----|------|------|
| M-01 | **Strict deadline enforcement prevents legitimate bonding curve participation**（截止时间强制执行过严，阻止合法参与）| ✅ 已确认（团队接受风险）|
| M-02 | **Cross-graduation accounting discrepancy causes fund misallocation**（跨毕业线会计差异导致资金分配错误）| ✅ 已修复 |

**M-02 详情**：当一笔买入交易横跨毕业阈值时（买入中途触发毕业），超出 $9K 门槛的部分 USDC 仍全部被铸造为 LT 并留在曲线内，而非正确地将多余资金分配至 LP。已修复。

#### Low 级发现

| ID | 标题 | 状态 |
|----|------|------|
| L-01 | Seller receives less USDC than expected due to undisclosed BounceTech fee（卖出实得 USDC 少于预期，因 BounceTech 赎回费未在预估中体现）| ✅ 已确认 |
| L-02 | Buyer fee is not collected for the closing buy（毕业最后一笔买入未收取买方手续费）| ✅ 已修复 |
| L-03 | `createToken` and `buyWithPermit` can be front-run（创建代币和 Permit 买入可被前跑）| ✅ 已确认 |
| L-04 | Tokens can get stuck in `LPLock`（代币可能永久锁死在 LPLock 合约中）| ✅ 已修复 |
| L-05 | Missing minimum amount check for USDC swaps（USDC 兑换缺少最小金额校验）| ✅ 已修复 |
| L-06 | Referral fee is not emitted in events（推荐费事件未正确发出）| ✅ 已确认 |
| L-07 | Protocol fees are collected post-graduation（毕业后仍收取协议费）| ✅ 已确认（团队设计如此）|
| L-08 | Vanity address probe causes out-of-gas（靓号地址探测导致 gas 耗尽）| ✅ 已修复 |

#### 关键风险解读

- **L-01（未修复）**：卖出时 BounceTech 赎回费（0.3%）不含在平台的报价预估中，用户实际到手 USDC 会少于界面显示值，存在透明度问题。
- **L-03（未修复）**：`createToken` 和使用 Permit 买入均可被 MEV 机器人前跑，但影响有限，属于结构性无法完全避免的问题。
- **L-07（已确认）**：毕业后协议仍从 HyperSwap 交易中抽取 0.5% 费用（创建者 0.25% 继续）——团队确认这是有意为之的设计。
- **M-02（已修复）**：跨毕业触发时资金计算错误已修复，避免了流动性迁移时的资金损失。

---

## 九、与竞品横向对比

| 特性 | **alt.fun** | **Pump.fun** | **HypurrFun** |
|------|------------|-------------|--------------|
| 所在链 | HyperEVM | Solana | HyperEVM |
| 储备资产 | 杠杆代币（LT）| SOL | HYPE |
| 价格驱动力 | 交易 + 杠杆行情 | 仅交易 | 仅交易 |
| 毕业门槛 | $9K USD（**动态**）| ~$69K SOL | 固定 |
| 可选杠杆 | 2x / 3x / 5x | 无 | 无 |
| 多空方向 | Long / Short | 无 | 无 |
| 毕业后配对资产 | LT（保留杠杆）| SOL | HYPE |
| 无买盘也能涨 | **是** | 否 | 否 |
| 波动率损耗风险 | **有** | 无 | 无 |
| 毕业阈值可后退 | **是** | 否 | 否 |
| 合约可升级 | 是（UUPS）| 否 | 未知 |
| 平台费率 | 0.75% | 1% | 未知 |

---

## 十、核心创新总结

alt.fun 将**杠杆衍生品**与**社区代币发射**深度融合，形成了几个独特的创新点：

### 10.1 "无买盘即可涨"的冷启动解法
传统 Launchpad 的痛点是新代币需要大量买盘才能推高价格。alt.fun 通过 LT 储备，让代币在底层资产顺势运动时自然升值，有效降低了冷启动难度。

### 10.2 方向性押注 × Meme 文化结合
首次允许发射 **Short 类型代币**（如 "BTC 3x Short Meme"），让看空者也能通过 Meme 社区参与做空叙事，创造了全新的玩法。

### 10.3 杠杆延续性
毕业后代币的配对资产仍是 LT 而非稳定币，持有者在 AMM 中交易时仍保留对底层资产的杠杆敞口，形成了独特的"永续杠杆 Meme"资产类别。

### 10.4 本质定义

> **alt.fun 的每个代币本质上是：Meme 社区投机 + 杠杆 ETF 的混合体。**  
> 它同时满足了 Meme 玩家（叙事驱动）和交易员（杠杆方向押注）的需求，但也叠加了两者的风险。

---

## 十一、参考资料

| 资源 | 链接 |
|------|------|
| 官网 | https://alt.fun |
| 文档 | https://docs.alt.fun |
| 合约（Zap） | https://hyperevmscan.io/address/0xb318e2ab995d805cb0c5b97c39edda0aa8758feb#code |
| BounceTech | https://bouncetech.io |
| Hyperliquid | https://hyperliquid.xyz |
| HyperSwap | https://hyperswap.exchange |

---

*报告生成时间：2026-05-16*  
*数据来源：alt.fun 官网、docs.alt.fun、HyperEVMScan 链上合约*

