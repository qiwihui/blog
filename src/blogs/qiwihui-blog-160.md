# Across 代币发布提案 v2


# Across 代币发布提案 v2

这是一个修订后的提案，它建立在[最初的 Across 代币发布提案](https://forum.across.to/t/across-token-launch-proposal/195)的基础上，增加了社区反馈和实施细节。

Across 代币的推出将发展和团结 Across 社区，激励流动性提供者，提高 Across 的知名度，并进一步实现成为最快和最便宜的 L2 桥的使命。 该提案概述了代币发布计划，大致可分为两部分：

1. 初始分配（Initial Distribution）── 多样化的空投和国库代币交换
2. 奖励锁定激励计划（Reward Locking Incentive Program） ── 一种新颖的奖励计划，用于激励支持 Across 协议的行为

## 第一部分、初始分配

将铸造 **1,000,000,000 (\$ACX)** Across 代币 。 700,000,000 \$ACX 将保留在 Across DAO 国库中，一部分将保留用于激励奖励。 300,000,000 \$ACX 将作为初始供应，并按以下方式分配：

**\$ACX 空投** ── 总共 **100,000,000 \$ACX** 将奖励给以下团体：

1. 10%：拥有“联合创始人（Co-founder）”或“早期招募（Early Recruit）”的社区 Discord 成员
2. 10%：拥有“DAO 贡献者（DAO Contributor）”或“高级 DAO 贡献者（Senior DAO Contributor）”的社区 Discord 成员
3. 20%：代币将作为额外奖励保留给 Across 社区的重要早期贡献者，其中可能包括 DAO 贡献者、高级 DAO 贡献者和开发者支持团队。代币发布后，社区将有机会提交关于如何分配的提案，\$ACX 持有者将通过快照进行投票。
4. 10%：在 2022 年 3 月 11 日之前桥接资产的早期 Across 协议用户。这些代币将根据完成的转账量按比例分配给钱包。将调整这些数字以过滤掉可能来自空投农民的小额转账。
5. 50%：在代币发布之前将 ETH、USDC、WBTC 和 DAI 汇集到 Across 协议中的流动性提供者。对 LP 的奖励数量按规模按比例分配，并且自协议开始以来，每个区块都会发出固定数量的代币。

* \*权重和确切细节都可能发生变化，并取决于代币发布前收集的数据。*

**\$UMA 的代币交换 ── 100,000,000 \$ACX** 将与 Risk Labs Treasury 交换价值 5,000,000 美元的 \$UMA。 这实现了两个目标 ── 它赋予 UMA 中的 Across 社区所有权和治理权，这对桥的安全性至关重要，并且它还提供投票奖励作为 Across DAO 国库的收入来源。 Risk Labs 推出了 Across，并将在可预见的未来继续支持协议和社区。 向 Risk Labs 提供 \$ACX 将进一步激励 Risk Labs 团队。 Risk Labs 可能会考虑使用这些代币来建立和扩展一个专门的开发团队，以帮助提供 \$ACX 的流动性，并参与治理。 无论用途如何，这些代币只会用于协议的利益。

**战略合作伙伴和中继者资本 ── 100,000,000 \$ACX** 将转移到 Risk Labs Treasury，以筹集资金并从 DeFi 行业的主要参与者那里获得贷款。 跨链桥领域的竞争对手正在与大型机构合作，并获得大量资源来推动其发展。 Risk Labs 可以使用这些代币来帮助 Across 协议做同样的事情。 一个关键的资源限制是中继者网络，其中大量资金由 Risk Labs 的国库提供。 与资本充足的大型加密货币玩家合作有助于缓解这一瓶颈并加速增长。 为实现这一目标，Risk Labs 可能会使用这些 \$ACX 代币来筹集成功代币（[success token](https://umaproject.org/products/success-tokens)）资金，在通过区间代币（[range tokens](https://umaproject.org/products/range-tokens)）借款时用作抵押，以及用于奖励以促进中继者网络的去中心化。

## 第二部分、Across 奖励锁定激励计划

700,000,000 \$ACX 储备的很大一部分将通过此激励计划发放，社区成员可以通过执行以下任何操作来赚取 \$ACX：

1. 质押来自桥接池的 Across LP 份额 ── WETH 和 USDC 池将是第一个受到激励的 Across 池
2. 从指定的 \$ACX/ETH 池中质押 \$ACX LP 份额
3. 通过 Across 推荐计划（Across Referral Program）推荐用户

**流动性提供者（LP）** ── 奖励锁定是传统流动性挖矿的增强版本，它阻止耕种（farm）和抛售活动，同时奖励协议的忠实贡献者。流动性提供者 (LP) 有一个他们获得奖励的个性化利率。 LP 保持未提取（和未售出）累积奖励的时间越长，LP 获得额外奖励的速度就越快。

每个受激励的流动性池将有一个基本的发放率，每个 LP 将有一个针对每个池的独特收益增值率（multiplier）。 LP 将按比例获得基准发放量乘以 LP 的独特收益增值率的份额。 LP 的收益增值率从第 0 天的 1 开始，当奖励未提取 100 天时可以线性增长到最大值 3。下表说明了这个简单的过程。例如，持有 60 天未领取的奖励的 LP 的收益增值率为 2.2。一旦 LP 领取任何奖励，收益增值率立即重置为 1，LP 将需要重赚取该乘数。

|持有天数 | 收益增值率|
|--- | ---|
0 | 1.0
25  |1.5
50 | 2.0
75 | 2.5
100 | 3.0

最初的奖励锁定计划预计将运行 6 个月，届时将及时审查是否有任何更改。 该计划将从以下基本发放率开始：

- Across ETH LP 份额每天约 100,000 \$ACX
- Across USDC LP 份额每天约 100,000 \$ACX
- 指定 \$ACX/$ETH LP 份额每天约 20,000 \$ACX

这相当于大约 4MM 到 10MM \$ACX，具体取决于 LP 的行为。 \$ACX 持有者可以随时提议并投票添加新资产或更改这些参数。

**Across 推荐计划** ── 推荐计划将 Across 社区转变为销售队伍。要参与推荐计划，Across 支持者可以输入他们的钱包地址以生成唯一的推荐链接。单击该链接并在 Across 上完成桥接转移的用户会将 \$ACX 奖励分配给推荐人。鼓励支持者与朋友分享他们的链接，并在 Twitter 等社交媒体上宣传 Across。这也可以用于与其他项目的集成。跨链聚合器或 DEX 可以创建推荐链接以将 Across 连接到他们的 dApp。单击该链接并完跨链转移后，奖励将分配给该项目。该钱包所有的未来转账将继续向推荐人发放奖励，除非钱包用户点击不同的推荐链接或推荐人领取了他们的奖励。

与 LP 的奖励锁定类似，推荐人可以通过保持奖励未认领并达到特定数量的推荐或确保一定数量的数量来提高他们赚取推荐费的比率。推荐费是在 \$ACX 中授予推荐人的跨链 LP 费用的百分比。如果没有领取奖励并且完成了一定数量的推荐或交易量，那么推荐费就会上涨。推荐人分为五层：

- 铜（Copper）：40% 的推荐费。
- 青铜（Bronze）：50% 推荐费。铜推荐人在 3 次推荐或跨链交易量超过 5 万美元后晋升为青铜
- 白银（Silver）：60% 的推荐费。青铜推荐人在 5 次推荐或跨链交易量超过 10 万美元后晋升为白银
- 黄金（Gold）：70% 的推荐费。白银推荐人在 10 次推荐或超过 25 万美元的跨链交易量后升级为黄金。
- 白金（Platinum）：80% 的推荐费。黄金推荐人在 20 次推荐或超过 50 万美元的跨链交易量后升级为白金。

推荐奖励每周分配一次，推荐人每周只能增加一个等级。一旦推荐人领取奖励，推荐人的等级立即重置回铜，并且所有推荐链接都失效。这意味着推荐人需要让用户再次点击他们的推荐链接才能继续赚取推荐费，并且推荐人需要重新获得他们的等级，这需要至少 5 周的时间才能达到白金级别。

**奖励锁定 = DeFi 的游戏化**

奖励锁定的好处是显而易见的。保持奖励锁定不鼓励耕种和抛售活动，但更重要的是，它使 LP 和推荐人与协议更加紧密。如果您被鼓励参与该协议，您自然会想了解更多有关它的信息，并且您会被激励加入社区并进一步履行其使命。

鉴于您可以为每个流动性池赚取的各种独特收益增值率，以及您作为推荐人可以获得的不同层级，为协议做出贡献的每个钱包都将发展出一个个性化的身份。类似于角色扮演游戏中的角色，各种统计数据可以转化为经验值，使钱包可以升级并获得协议中的状态。

奖励锁定可以通过精心涉及的用户界面和用户体验进一步游戏化，使其看起来像一个真正的游戏。它可以像 RPG 一样构建，用户可以在达到某些里程碑时获得特殊的 NFT 或物品。社区成员可以构建这个和/或使用这些统计数据的实际游戏并相互进行战斗。同样，排行榜可以识别所有忠诚的 Across 用户的成就。这一切都会使用户非常不愿意领取他们的奖励并降低身份。

**质押 \$ACX** ── 随着协议的成熟，社区可以考虑为 \$ACX 设置质押机制，该机制可以授予进一步的治理权，并分享整个协议的收入。治理可以决定激励奖励的方向，以确定哪些代币和哪些 L2 应该获得更多流动性。这种类似投票锁定的机制可以为 \$ACX 和 Across 协议增加更多价值。

## 结论

除了建立社区和激励项目目标外，Across 代币的发布旨在为拥有 \$ACX 创造价值和意义。 目标是让 \$ACX 代币持有者在启动后立即通过他们的代币与协议进行交互。 事实上，通过概述在空投之前将获得奖励的行为，这个协议现在正在鼓励整个 LP 活动。 Across 奖励锁定激励计划将吸引社区成员并使用 \$ACX 作为货币来游戏化和激励对协议的贡献。 \$ACX 代币将代表 Across 协议在经济和治理方面的真正所有权。

非常欢迎对此提案提出反馈意见。 可以而且应该讨论机制和数字，以便社区在此代币发布之前感到舒适。


[View on GitHub](https://github.com/qiwihui/blog/issues/160)


