# Uniswap v3 无常损失分析


# Uniswap v3 无常损失分析

## 目标

1. 对 Uniswap v3 无常损失的定量分析；
2. 如何使用策略让 Uniswap v3 LP 获得更大的收益。

<!--more-->

## Uniswap 概览

基于恒定乘积的自动化做市商（AMM），去中心化交易所。

**v1 版本:**

- 2018年11月
- 解决了什么问题：传统交易所 order book 买卖双方不活跃导致的长时间挂单，交易效率低下
- 功能：ETH ←→ ERC20 token 兑换
- 带来的问题：
    - token1 与 token2 之间的兑换需要借助 ETH
        - USDT → ETH → USDC

**v2 版本:**

- 2020年5月
- 新功能
    - 自由组合交易对：token1 ←→ token2
        - token1-token2 交易池
    - LPers 提供流动性并赚取费用
    - 价格预言机（时间加权平均价格，TWAP）、闪电贷、最优化交易路径等
- 带来的问题
    - 资金利用率低：
        - 在 `x*y=k` 的情况下，做市的价格区间在 (0, +∞) 的分布，当用户交易时，交易的量相比我们的流动性来说是很小的
        - 假设 ETH/DAI 交易对的实时价格为 1500 DAI/ETH，交易对的流动性池中共有资金：4500 DAI 和 3 ETH，根据 `x⋅y=k`，可以算出池内的 k 值： `k=4500×3=13500`。假设 x 表示 DAI，y 表示 ETH，即初始阶段 x1=4500，y1=3，当价格下降到 1300 DAI/ETH 时： `x2⋅y2=13500, x2/y2=1300`，得出 `x2=4192.54, y2=3.22`，资金利用率为： `Δx/x1=6.84%`。同样的计算方式，当价格变为 2200 DAI/ETH 时，资金利用率约为 `21.45%`。也就是说，在大部分的时间内池子中的资金利用与低于 25%，这个问题对于稳定币池来说更加严重。
            
            
![Untitled](https://user-images.githubusercontent.com/3297411/190839344-efc05df3-293a-422e-bc22-b26311154b12.png)
            

**v3版本:**

- 2021年5月
- 考虑风险
    1. 价格影响（Price impact）：
        - 是指一笔交易对价格的影响程度，取决于池子深度。 更高的价格影响意味着：流动性提供者提供的流动性不足，向交易者提供更差的比率（滑点高）。
    2. 存货风险（Inventory risk）：
        - LP 的主要目标是随着时间的推移增加其总库存价值
        - 在价格变化过程中，相对于首选价值存储的资产而言，LP 拥有的资产数量更少，比如对于 ETH-DAI，用户更倾向于 ETH（ETH价格升高），相对于 ETH而言，LP 拥有越多的 DAI，存货风险越高；
        - 比如 100% ETH 和 50%-50% ETH-DAI 的对比，ETH价格上涨，更多人将 DAI 换成 ETH，相对应LP手中 ETH就少了，风险加大。
    3. 无常损失
        - 提供流动性时发生的资金暂时损失/非永久性损失；
        - 只要代币相对价格恢复到其初始状态，该损失就消失了；
- 新功能
    - 集中流动性 →  提升资金利用率
        
        
![Untitled 1](https://user-images.githubusercontent.com/3297411/190839359-483c9ed2-e79f-4be9-b489-0af0d86c62b6.png)

        
    - 多层级手续费率（0.05%，0.3%，1%），升级的预言机，区间订单（range order）等。
- 带来的问题：
    - 相对于v2而言
        - 无常损失（Impermanent Loss）仍然存在，而且更大；
        - LP 的权衡
            - 价格区间越大，所获得的费用收益就越低，(0, +∞)时和 v2一致。
            - 但如果选择一个更小的价格区间，就会有更高的无常损失。

## 无常损失分析

### Uniswap v2

**例子：**

假设 ETH/DAI 交易对的实时价格为 1500 DAI/ETH，交易对的流动性池中共有资金：4500 DAI 和 3 ETH，根据 `x⋅y=k`，可以算出池内的 k 值： `k=4500×3=13500`。假设 x 表示 DAI，y 表示 ETH，即初始阶段 x1=4500，y1=3。

当价格下降到 1300 DAI/ETH 时： `x2⋅y2=13500, x2/y2=1300`，得出 `x2=4192.54, y2=3.22` 。

如果用户选择HODL，则 `x2'=4500，y2'=3`，我们分别计算两种情况下的资产价值（DAI）：

LP: 4192.54 + 3.22 * 1300 = 8378.54

HODL: 4500 + 3 * 1300 = 8400

资产减少：8400 - 8378.54 = 21.46 → 无常损失

无常损失率：21.46 / 8400 = 0.26%

当价格变为 2200 DAI/ETH时，x2=5449.77, y2=2.48，资产减少 194.23，损失率为 1.75%。

**模型分析：**

根据恒定乘积公式 $xy=k$，令 $k=L^2$，其中 L 表示流动性，则有 $xy=L^2$，再根据价格 $S=x/y$，可以得到 $x=L/\sqrt{S}$，$y=L\sqrt{S}$。

考虑 LP 在流动性池 X-Y 中添加流动性 $L$，池的初始价格为 $S_0$，所以 LP 需要向流动性池中提供 $x_0=L/\sqrt{S_0}$的 X 代币和 $y_0=L\sqrt{S_0}$ 的 Y 代币。

当池的价格变为 $S_1$时，LP 的资产价值为

$$
V_{v2,pos}(L, S_1)=S_1 \cdot x_1+y_1=\frac{L}{\sqrt{S_1}}S_1+L\sqrt{S_1}=2L\sqrt{S_1}
$$

其中 $x_1$和 $y_1$是LP在池中的资产。

LP 初始时的资产如果一直拿手里，则价值为

$$
V_{v2,hold}(L,S_0,S_1)=S_1 \cdot x_0 + y_0=\frac{L}{\sqrt{S_0}}S_1+L\sqrt{S_0}
$$

所以，无常损失为：

$$
\begin{aligned}
\mathrm{IL}_{\mathrm{v} 2}\left(S_0, S_1\right) &=\frac{V_{\mathrm{v} 2, \text { pos }}-V_{\mathrm{v} 2, \text { hold }}}{V_{\mathrm{v} 2, \text { hold }}} \\
&=\frac{2 L \sqrt{S_1}-\left(\frac{L}{\sqrt{S_0}} S_1+L \sqrt{S_0}\right)}{\frac{L}{\sqrt{S_0}} S_1+L \sqrt{S_0}} \\
&=\left(\frac{2 \cdot \sqrt{\frac{S_1}{S_0}}}{1+\frac{S_1}{S_0}}-1\right)
\end{aligned}
$$

令 $r=S_1/S_0$，则有：

$$
\mathrm{IL}_{v2} = \frac{2 \cdot \sqrt{r}}{1+r}-1
$$

用之前的例子计算，r=1300/1500=0.87时，IL=0.0026=0.26%，r=2200/1500=1.47时，IL=0.018=1.8%，与上述计算相符合。

**图像：**

![Untitled 2](https://user-images.githubusercontent.com/3297411/190839374-f568b419-7536-44d0-b988-13dd4982972a.png)

[https://www.desmos.com/calculator/aza5py3g95](https://www.desmos.com/calculator/aza5py3g95)

可以看到，当 $S_0=S_1$时无常损失为0，其他时候无常损失都为负数。列一个表：

| 价格变化 | 无常损失 |
| --- | --- |
| 0.25x | 20.0% |
| 0.5x | 5.7% |
| 0.75x | 1.0% |
| 1 | 0 |
| 1.25x | 0.6% |
| 1.5x | 2.0% |
| 1.75x | 3.8% |
| 2x | 5.7% |
| 3x | 13.4% |
| 4x | 20.0% |
| 5x | 25.5% |

### Uniswap v3

用同样的过程，我们分析 Uniswap v3的无常损失。假设 LP 向价格区间 $[P_a,P_b]$提供流动性  $L$，初始价格为 $P_0(\in[P_a,P_b])$，之后价格变为 $P_1(\in[P_a,P_b])$。

首先我们从Uniswap v3 的白皮书中可以知道，集中流动性的资产储备曲线（橙色）的公式为：

$$
\left(x+\frac{L}{\sqrt{p_b}}\right)\left(y+L \sqrt{p_a}\right)=L^2
$$

（推导：曲线相当于v2的曲线向左向下平移动）

![Untitled 1](https://user-images.githubusercontent.com/3297411/190839406-4880142e-70e3-4073-973f-1f9d8830449c.png)

对于虚拟曲线: $x_{virtual} \cdot y_{virtual} = L^2$，可以得到：

$$
\begin{aligned}&y=y_{\text {virtual }}-L \sqrt{p_a}=L\left(\sqrt{P}-\sqrt{p_a}\right) \\&x=x_{\text {virtual }}-\frac{L}{\sqrt{p_b}}=L\left(\frac{1}{\sqrt{P}}-\frac{1}{\sqrt{p_b}}\right)\end{aligned}
$$

初始时资产价值为：

$$
\begin{aligned}V_{v3}(P_0) &=y_0+x_0 \cdot P_0 \\&=L\left(\sqrt{P_0}-\sqrt{p_a}\right)+L\left(\sqrt{P_0}-\frac{P_0}{\sqrt{p_b}}\right) \\&=2 L \sqrt{P_0}-L\left(\sqrt{p_a}+\frac{P_0}{\sqrt{p_b}}\right)\end{aligned}
$$

同样，则在价格 $P_1$时流动池中的资产价值为（令 $r=P_1/P_0$）：

$$
\begin{aligned}V_{v3,pos}(P_1) &=2 L \sqrt{P_1}-L\left(\sqrt{p_a}+\frac{P_1}{\sqrt{p_b}}\right) \\ &=2 L \sqrt{rP_0}-L\left(\sqrt{p_a}+\frac{rP_0}{\sqrt{p_b}}\right)\end{aligned}
$$

在价格为 $P_1$ 时的，选择 HODL 的资产价值为：

$$
\begin{aligned}
V_{\text {v3,hold}}(P_1) &=y_0+x_0 P_1 \\
&=L\left(\sqrt{P_0}-\sqrt{p_a}\right)+P_1 \cdot L\left(\frac{1}{\sqrt{P_0}}-\frac{1}{\sqrt{p_b}}\right) \\&=L\left(\sqrt{P_0}-\sqrt{p_a}\right)+L \cdot rP _0\left(\frac{1}{\sqrt{P_0}}-\frac{1}{\sqrt{p_b}}\right) \\
&=L \sqrt{P_0}(1+r)-L\left(\sqrt{p_a}+\frac{rP_0 }{\sqrt{p_b}}\right)
\end{aligned}
$$

所以无常损失为（不失一般性，取 $P_0$为 $P$）：

$$
\begin{aligned}\mathrm{IL}_{a, b}(r) &=\frac{V_{pos}-V_{\text {hold }}}{V_{\text {hold }}} \\&=\frac{2 L \sqrt{rP}-L \sqrt{P}(1+r)}{L \sqrt{P}(1+r)-L\left(\sqrt{p_a}+\frac{rP}{\sqrt{p_b}}\right)} \\&=\frac{2 \sqrt{r}-1-r}{1+r-\sqrt{\frac{p_a}{P}}-r \sqrt{\frac{P}{p_b}}} \\&=\operatorname{IL}(r) \cdot\left(\frac{1}{1-\frac{\sqrt{\frac{p_a}{P}}+r \sqrt{\frac{P}{p_b}}}{1+r}}\right)\end{aligned}
$$

（ $P_1$ 在价格区间 $[0,P_b]$，$[P_a,+\infty]$时的无常损失也同样可以计算。）

我们可以通过价格区间 $[P_a, P_b]$ 的变化看到：

1. 在 $P_a=P_b=P$时， IL = 0；
2. 当 $r=1$ 时， IL = 0；
3. 与 v2 的联系：

$$
p_a=0, p_b \rightarrow \infty, \mathrm{IL}_{v3}=\frac{2 \cdot \sqrt{r} -1-r}{1+r}=\mathrm{IL}_{v2}
$$

趋近于 $\mathrm{IL}_{v2}$。

**画图**

![Untitled 3](https://user-images.githubusercontent.com/3297411/190839418-ebe47fa1-2446-431d-bceb-1e01ddd454a4.png)

[https://www.desmos.com/calculator/ha322rtufc](https://www.desmos.com/calculator/ha322rtufc)

同样我们可以看到：当价格区间越小时，无常损失越大：

（这是一个动图）

![Untitled](https://user-images.githubusercontent.com/3297411/190839425-25812665-4d4c-4b3a-bb0e-38378036b31d.gif)

数值**比较**

我们比较在不同的价格区间下 Uniswap v3的无常损失：

<img width="757" alt="Screen_Shot_2022-08-31_at_09 56 06" src="https://user-images.githubusercontent.com/3297411/190839436-dc4969bd-51d7-4a30-a86e-9d50930fdc85.png">

具体数据（）：

| 价格区间% | -20% | Initial | +20% |
| --- | --- | --- | --- |
| [0%,Inf]( Uniswap v2 ) | -0.56% | 0 | -0.46% |
| [0%, 200%] | -0.86% | 0 | -0.70% |
| [25%, 175%] | -1.5% | 0 | -1.22% |
| [50%, 150%] | -2.34% | 0 | -1.91% |
| [75%, 125%] | -4.75% | 0 | -3.8% |

提问：既然无常损失总是为负，为什么还是会有人愿意做 LP？

我们的计算忽略了两个问题：

1. 手续费（fee）：不同的池子提供不同的手续费，需要在原来的计算上加上手续费。
2. 集中流动性增加了池的深度：
    - 例如：ETH-USDC-0.3%池的流动性
                
		![Untitled 4](https://user-images.githubusercontent.com/3297411/190839469-259db8d9-b51e-47c9-8444-06399598866e.png)

    - 一些流行的 token 对的深度比中心化交易所（Binance, Coinbase）更高。[link](https://uniswap.org/blog/uniswap-v3-dominance)
        - large-cap: ETH/dollar
        - mid-cap - cross-chain pairs
            
			![Untitled 5](https://user-images.githubusercontent.com/3297411/190839462-ae80daf8-398c-4dac-bc90-482a62fd3388.png)

            
        - 稳定币与稳定币对: USDC/USDT

### **从资产价值的角度**

比较以下五种资产持有策略

1. 100% 持有 ETH
2. 100% 持有 USDC
3. 50% 持有 ETH，50% 持有 USDC
4. 使用 50%ETH 与 50%USDC 参与做市 - Uniswap v2
5. 使用 50%ETH 与 50%USDC 参与做市 - Uniswap v3

比较这五种策略的资产价值。（使用 [https://defi-lab.xyz/uniswapv3simulator](https://defi-lab.xyz/uniswapv3simulator)）

无手续费时：

<img width="838" alt="Untitled 6" src="https://user-images.githubusercontent.com/3297411/190839480-ae2dbd81-24c7-4692-8ec5-c682b28937ea.png">

包含手续费时：

![Untitled 7](https://user-images.githubusercontent.com/3297411/190839487-0004de8e-9500-42e6-95dd-3cf5dca0e737.png)

Uniswap V3 既是投资者收益的放大器，也是风险的放大器。在享受更高投资收益的同时，也必然要承担当价格脱离安全范围时更多的无常损失。

## 如何通过策略降低损失，或者说增加收益？

### 策略0：在不主动调整的情况下选择比v2表现更好的池子

在不主动调整情况下，全范围（full range）的 Uniswap v3 头寸和价格限定的稳定币头寸的手续费回报平均比 Uniswap v2 好约 54%。其中

- 100 基点手续费的全范围 v3 头寸比 v2 平均**好** ~80%。
- 1 基点，范围限定的 v3 稳定币对，v2 ，平均**好** ~160%.
- 30 基点，全范围 v3 头寸， v2 平均**好** ~16%.
- 5 基点，全范围 v3 头寸，v2  平均**差** ~68%.

通常建议 LPers 选择 v3。[link](https://uniswap.org/blog/fee-returns)

选择哪个池？

![Untitled 8](https://user-images.githubusercontent.com/3297411/190839496-8d41b11a-d26a-479c-8441-c481f3aa26e9.png)

v3 表现更好的是 100 基点费率或 1 基点费率的稳定币对。

100 bps 的 token 对通常流动性较差，部署时间较晚且波动性较大。 对于 1-bp 费用等级，代币对价格波动较小，但 Uniswap v3 的交易量远高于 v2。 1-bp 池上的集中流动性实现了超过 v2 的高回报。

### 策略一：主动的被动策略

如果初始投入是 50%ETH 和50%USDC，当价格变化时，池中剩余的资产比例可能变成 80%ETH 和 20%USDC，这时你需要手动调整库存来防止出现一种资产在一侧耗尽，可以持续提供两边的库存。

根据价格变动周期性地再平衡（rebalance）两种资产之间的比例。

利用范围订单（range order）被动执行的，在现在价格的预测方向放置一个窄的订单，这样就避免了swap费用和价格影响。如果主动使用 swap 达到 50/50，会有 0.3%的费用。

**如何操作：**

对于 Uniswap 上为某个矿池，例如 ETH/USDC，它有两个主要参数：

- B（基本阈值）
- R（再平衡阈值）

该策略始终保持两个有效的范围订单：

- 基本定单：以当前价格 X 为中心，范围 [X-B, X+B]。 如果 B 较低，它将从交易费用中获得更高的收益。
- 再平衡订单：刚好高于或低于当前价格。在 [X-R, X] 或 [X, X+R] 范围内，具体取决于在基本订单下达后它持有的更多的代币是哪一种。 此订单有助于策略重新平衡并接近 50/50 以降低库存风险。

每24小时，进行再平衡，根据价格和token数量提交订单。如果策略表现优秀，则时间区间可以被减少。再平衡并不能保证完全50/50。

**举例：**

![Untitled 9](https://user-images.githubusercontent.com/3297411/190839504-426e6004-c3f3-4101-8a08-c507915c9d20.png)

比如，ETH目前价格 150USDC，B=50，R=20，策略拥有资金 1ETH 和160USDC。则在 [100, 200] 放置一个基础订单，使用 1ETH 和 150 USDC。剩余的 10 USDC 用来在 [130,150] 放置一个在平衡订单，用来购买ETH以达到50/50。

![Untitled 10](https://user-images.githubusercontent.com/3297411/190839510-80e1e8bd-3204-4566-a11c-b4c268246038.png)

如果价格提升到 180， 再平衡之后，基础订单为 [130, 230]，若此时策略有 1.2 ETH 和 90USDC，则策略会使用 0.5EHT 和 90USDC 放入基础订单中，剩余 0.7ETH 会用于在 [180, 200] 之间的再平衡订单。

实际操作：

[https://dune.com/queries/78325/155734?Number of days=200](https://dune.com/queries/78325/155734?Number%20of%20days=200)

**效果**

蓝色曲线

![Untitled 11](https://user-images.githubusercontent.com/3297411/190839522-c5c425e6-a397-4809-a96e-3a36c20ee8b5.png)

实际效果：

[https://dune.com/mxwtnb/Alpha-Vaults-Performance?Number+of+days=200&Number+of+days_t4072e=500](https://dune.com/mxwtnb/Alpha-Vaults-Performance?Number+of+days=200&Number+of+days_t4072e=500)

### 策略二：预期价格范围策略（expected price range strategies）

从历史数据中预测未来10分钟的价格走势，得到一个价格范围区间，在这个价格范围区间中提供流动性。直到当前价格超出价格范围，重复上述过程，重新预测价格范围并添加流动性。这个价格范围称为“预期价格范围”。同时我们可以在当前价格没有完全超出预期价格范围时调整价格区间，称这个价格范围为“移动策略范围（move strategy ranges）”，这个范围指示了什么时候需要移动。

<img width="479" alt="Untitled 12" src="https://user-images.githubusercontent.com/3297411/190839530-f02eb060-6daf-4545-8166-35ecf2e34270.png">

**如何设置**

2018年3月~2020年4月的十分钟数据得出价格移动分布在 [-3%, 3%] 之间。可以设置百分比作为价格波动区间。

<img width="501" alt="Untitled 13" src="https://user-images.githubusercontent.com/3297411/190839533-07b08d89-e42d-471c-84c3-85444226f677.png">

**进一步策略**：在预期价格范围内不采用一致的流动性，而是采用多个连续的流动性多头，每个多头存入不同数量的资产。

三种策略：

- 均匀策略：在价格区间内均匀分布，Uniswap v3 默认；
- 比例策略：在价格区间内分成子价格区间，权重对应价格可能的变化概率放置；
- 最优策略：使用决策理论（比如马尔可夫决策过程），计算一个模型来估算“最佳”范围来提供流动性，使用 LP 的“风险规避”程度作为参数。

**比例策略：**

- Ba: 预期价格范围
- Bt: 移动策略范围

蓝线为概率分布，使用小的价格区间实现

<img width="509" alt="Untitled 14" src="https://user-images.githubusercontent.com/3297411/190839543-c3e52671-e05b-4f1b-8e8a-dfeed7f886d1.png">

**结论：**

- 对于厌恶风险的投资者，均匀策略最优，对于其他所有人来说是次优的；
- 比例策略对于大部分厌恶风险的投资者来说的接近最优的；
- 对于最厌恶风险的投资者而言，均匀策略可获利。

![Untitled 15](https://user-images.githubusercontent.com/3297411/190839545-ec74a8e6-e5bb-4ed2-8712-630db12c2226.png)

比例策略对于风险偏向 LP 提供者是最优的（ $\alpha$大 ），而均匀分配对于风险规避LP提供者是最优的（ $\alpha$ 小）。

这意味着，在 Uniswap v3 中被动管理的头寸可能不足以以资本效率和平衡风险赚取费用，积极的流动性提供策略既是机遇也是挑战。

### 其他主动的流动性管理

其他主动策略 dapp

- [xToken project](https://xtoken.market/app/invest)
- [Gelato Network](https://www.gelato.network/)
- [Visor Finance team](https://www.visor.finance/)
- Charm.fi’s [Alpha Vaults](https://alpha.charm.fi/)
- [Mellow Protocol](https://mellow.finance/vault)

![Untitled 16](https://user-images.githubusercontent.com/3297411/190839551-e149cbf3-10fb-46c1-9a58-5507499ac6ea.png)

## 参考

- [How to avoid Impermanent Loss](https://newsletter.banklesshq.com/p/how-to-avoid-impermanent-loss)
- [Going Bankless with Uniswap](https://newsletter.banklesshq.com/p/10-going-bankless-with-uniswap-caleb)
- [How to make money with Uniswap V3](https://newsletter.banklesshq.com/p/how-to-make-money-with-uniswap-v3)
- [A Guide to Uniswap on Optimism](https://newsletter.banklesshq.com/p/a-guide-to-uniswap-on-optimism)
- ****Uniswap Liquidity Provision: Is the Yield Worth the Risk?：****[https://medium.com/gammaswap-labs/uniswap-liquidity-provision-is-the-yield-worth-the-risk-c45a4a850700](https://medium.com/gammaswap-labs/uniswap-liquidity-provision-is-the-yield-worth-the-risk-c45a4a850700)
- [https://betterprogramming.pub/uniswap-v2-in-depth-98075c826254](https://betterprogramming.pub/uniswap-v2-in-depth-98075c826254)
- [https://liaoph.com/uniswap-v3-1/](https://liaoph.com/uniswap-v3-1/)
- [https://www.theblockbeats.info/news/24654](https://www.theblockbeats.info/news/24654)
- [https://medium.com/charmfinance/introducing-alpha-vaults-an-lp-strategy-for-uniswap-v3-ebf500b67796](https://medium.com/charmfinance/introducing-alpha-vaults-an-lp-strategy-for-uniswap-v3-ebf500b67796)
- [https://medium.com/@DeFiScientist/rebalancing-vs-passive-strategies-for-uniswap-v3-liquidity-pools-754f033bdabc](https://medium.com/@DeFiScientist/rebalancing-vs-passive-strategies-for-uniswap-v3-liquidity-pools-754f033bdabc)
- [https://uniswap.org/blog/fee-returns](https://uniswap.org/blog/fee-returns)
- [https://uniswapv3.flipsidecrypto.com/](https://uniswapv3.flipsidecrypto.com/)
- [https://newsletter.banklesshq.com/p/how-to-automate-uniswap-v3-liquidity](https://newsletter.banklesshq.com/p/how-to-automate-uniswap-v3-liquidity)
- [https://kydo.substack.com/p/palm-protocol-owned-active-liquidity](https://kydo.substack.com/p/palm-protocol-owned-active-liquidity)

[View on GitHub](https://github.com/qiwihui/blog/issues/165)


