---
title: "Across 跨链桥合约解析"
description: "Across 跨链桥合约解析"
tags: 
- 区块链
top: 158
date: 18/03/2022, 18:00:34
author: qiwihui
update: 17/09/2022, 11:59:27
categories: 
---

## 什么是 Across

以太坊跨链协议 [Across](https://across.to/) 是一种新颖的跨链方法，它结合了乐观预言机（Optimistic Oracle）、绑定中继者和单边流动性池，可以提供从 Rollup 链到以太坊主网的去中心化即时交易。目前，Across 协议通过集成以太坊二层扩容方案Optimism、Arbitrum和Boba Network支持双向桥接，即可将资产从L1发送至L2，亦可从L2发送至L1。

<!--more-->

### 存款跨链流程

![process](https://user-images.githubusercontent.com/3297411/158982132-cd917c98-e156-45d4-b50b-0256f222db32.png)

来源于：[https://docs.across.to/bridge/how-does-across-work-1/architecture-process-walkthrough](https://docs.across.to/bridge/how-does-across-work-1/architecture-process-walkthrough)

Across 协议中，存款跨链有几种可能的流程，最重要的是，存款人在任何这些情况下都不会损失资金。在每一种情况下，在 L2 上存入的任何代币都会通过 Optimism 或 Arbitrum 的原生桥转移到 L1 上的流动池，用以偿还给流动性提供者。

从上面的流程中，我们可以看到 Across 协议流程包括以下几种：

- 即时中继，无争议；
- 即时中继，有争议；
- 慢速中继，无争议；
- 慢速中继，有争议；
- 慢速中继，加速为即时中继。

Across 协议中主要包括几类角色：

- 存款者（Depositor）：需要将资产从二层链转移到L1的用户；
- 中继者（Relayer）：负责将L1层资产转移给用户，以及L2层资产跨链的节点；
- 流动性提供者（LP）：为流动性池提供资产；
- 争议者（Disputor）：对中继过程有争议的人，可以向 Optimistic Oracle 提交争议；

## 项目总览

Across 的合约源码地址为 https://github.com/across-protocol/contracts-v1，目前 Across Protocol 正在进行 v2 版本合约的开发，我们这一篇文章主要分析 v1 版本的合约源码。首先我们下载源码：

```bash
git clone https://github.com/across-protocol/contracts-v1
cd contracts-v1
```

合约源码的主要的目录结构为：

```bash
contract-v1
├── contracts // Across protocol 的合约源码
├── deploy // 部署脚本
├── hardhat.config.js // hardhat 配置
├── helpers // 辅助函数
├── networks // 合约在不同链上的部署地址
└── package.json // 依赖包
```

在这篇解析中，我们主要关注 `contracts` 和 `deploy` 目录下的文件。

### 合约总览

合约目录 `contracts` 的目录结构为：

```bash
contracts/
├── common
│   ├── implementation
│   └── interfaces
├── external
│   ├── README.md
│   ├── avm
│   ├── chainbridge
│   ├── ovm
│   └── polygon
├── insured-bridge
│   ├── BridgeAdmin.sol
│   ├── BridgeDepositBox.sol
│   ├── BridgePool.sol
│   ├── RateModelStore.sol
│   ├── avm
│   ├── interfaces
│   ├── ovm
│   └── test
└── oracle
    ├── implementation
    └── interfaces
```

其中，各个目录包含的内容为：

- `common`：一些通用功能的库方法等，包括：
    - [AncillaryData.sol](https://github.com/across-protocol/contracts-v1/blob/master/contracts/common/implementation/AncillaryData.sol)：用来编码和解码 DVM价格请求的数据的库；
    - [FixedPoint.sol](https://github.com/across-protocol/contracts-v1/blob/master/contracts/common/implementation/FixedPoint.sol)：定点数运算；
    - [Lockable.sol](https://github.com/across-protocol/contracts-v1/blob/master/contracts/common/implementation/Lockable.sol)：防止重入攻击的一些函数修改器；
    - [MultiCaller.sol](https://github.com/across-protocol/contracts-v1/blob/master/contracts/common/implementation/MultiCaller.sol) ：可以在当个调用中调用合约的多个方法；
    - [Testable.sol](https://github.com/across-protocol/contracts-v1/blob/master/contracts/common/implementation/Testable.sol)：测试时修改时间；
    - [Timer.sol](https://github.com/across-protocol/contracts-v1/blob/master/contracts/common/implementation/Timer.sol)：获取时间方法；
- `external`：外部合约，主要用于实现在管理员合约中对不同 L2 的消息发送；
- `insured-bridge` 合约主要功能，我们会在接下来的章节章节中重点分析；
- `oracle`：主要是 Optimistic Oracle 提供功能的方法接口，在这篇文章中我们不对 Optimistic Oracle 的原理实现进行介绍，主要会介绍 Across 协议会在何处使用 Optimistic Oracle。

接下来我们会重点分析 `insured-bridge` 中的合约的功能，这是 Across 主要功能的合约所在。

在 `insured-bridge` 目录中：

- `BridgeAdmin.sol` ：管理合约，负责管理和生成生成 L2 上的 DepositBox 合约和 L1 上的 BridgePool 合约；
- `BridgeDepositBox.sol` ：L2 层上负责存款的抽象合约，Arbitrum，Optimism 和 Boba 网络的合约都是继承自这个合约；
- `BridgePool.sol` ：桥接池合约，管理 L1 层资金池。

## BridgeAdmin

这个合约是管理员合约，部署在L1层，并有权限管理 L1 层上的流动性池和 L2 上的存款箱（DepositBoxes）。可以注意的是，这个合约的管理帐号是一个多钱钱包，避免了一些安全问题。

首先我们看到合约中的几个状态变量：

```solidity
contract BridgeAdmin is BridgeAdminInterface, Ownable, Lockable {

    address public override finder;

    mapping(uint256 => DepositUtilityContracts) private _depositContracts;

    mapping(address => L1TokenRelationships) private _whitelistedTokens;

    // Set upon construction and can be reset by Owner.
    uint32 public override optimisticOracleLiveness;
    uint64 public override proposerBondPct;
    bytes32 public override identifier;

    constructor(
        address _finder,
        uint32 _optimisticOracleLiveness,
        uint64 _proposerBondPct,
        bytes32 _identifier
    ) {
        finder = _finder;
        require(address(_getCollateralWhitelist()) != address(0), "Invalid finder");
        _setOptimisticOracleLiveness(_optimisticOracleLiveness);
        _setProposerBondPct(_proposerBondPct);
        _setIdentifier(_identifier);
    }

...
```

其中：

- `finder` 用来记录查询最新 OptimisticOracle 和 UMA 生态中其他合约的合约地址；
- `_depositContracts` 该合约可以将消息中继到任意数量的 L2 存款箱，每个 L2 网络一个，每个都由唯一的网络 ID 标识。 要中继消息，需要存储存款箱合约地址和信使（messenger）合约地址。 每个 L2 的信使实现不同，因为 L1 --> L2 消息传递是非标准的；
- `_whitelistedTokens` 记录了 L1 代币地址与对应 L2 代币地址以及桥接池的映射；
- `optimisticOracleLiveness` 中继存款的争议时长；
- `proposerBondPct` Optimistic Oracle 中 proposer 的绑定费率

管理员可以设置以上这些变量的内容，以及可以设置每秒的 LP 费率，转移桥接池的管理员权限等。

同时，管理员还可以通过信使设置 L2 层合约的参数，包括；

- `setCrossDomainAdmin` ：设置 L2 存款合约的管理员地址；
- `setMinimumBridgingDelay` ：设置 L2 存款合约的最小桥接延迟；
- `setEnableDepositsAndRelays`：开启或者暂停代币 L2 存款，这个方法会同时暂停 L1 层桥接池；
- `whitelistToken`：关联 L2 代币地址，这样这个代币就可以开始存款和中继；

对于消息发送，管理员合约通过调用不同的信使的 `relayMessage` 方法来完成，将 msg.value == l1CallValue 发送给信使，然后它可以以任何方式使用它来执行跨域消息。

```solidity
    function _relayMessage(
        address messengerContract,
        uint256 l1CallValue,
        address target,
        address user,
        uint256 l2Gas,
        uint256 l2GasPrice,
        uint256 maxSubmissionCost,
        bytes memory message
    ) private {
        require(l1CallValue == msg.value, "Wrong number of ETH sent");
        MessengerInterface(messengerContract).relayMessage{ value: l1CallValue }(
            target,
            user,
            l1CallValue,
            l2Gas,
            l2GasPrice,
            maxSubmissionCost,
            message
        );
    }
```

不同L2的消息方法分别在对应链的 `CrossDomainEnabled.sol` 合约中，比如：

- Arbitrum: `contracts/insured-bridge/avm/Arbitrum_CrossDomainEnabled.sol`；
- Optimism，Boba: `contracts/insured-bridge/ovm/OVM_CrossDomainEnabled.sol`；

## BridgeDepositBox

接下来我们看到 `BridgeDepositBox.sol`，抽象合约 `BridgeDepositBox` 合约中主要有两个功能。

### `bridgeTokens`

第一个是 `bridgeTokens` 方法，用于将 L2 层代币通过原生代币桥转移到 L1 上，这个方法需要在不同的 L2 层合约上实现，目前支持的 L2 层包括 Arbitrum，Optimism 和 Boba，分别对应的文件为：

- Arbitrum: `contracts/insured-bridge/avm/AVM_BridgeDepositBox.sol`
- Optimism: `contracts/insured-bridge/ovm/OVM_BridgeDepositBox.sol`
- Boba: `contracts/insured-bridge/ovm/OVM_OETH_BridgeDepositBox.sol`

以 Arbitrum 链上的 `bridgeToken` 为例：

```solidity
    // BridgeDepositBox.sol 文件中
    function canBridge(address l2Token) public view returns (bool) {
        return isWhitelistToken(l2Token) && _hasEnoughTimeElapsedToBridge(l2Token);
    }

		// AVM_BridgeDepositBox.sol文件中
    function bridgeTokens(address l2Token, uint32 l1Gas) public override nonReentrant() {
        uint256 bridgeDepositBoxBalance = TokenLike(l2Token).balanceOf(address(this));
        require(bridgeDepositBoxBalance > 0, "can't bridge zero tokens");
        require(canBridge(l2Token), "non-whitelisted token or last bridge too recent");

        whitelistedTokens[l2Token].lastBridgeTime = uint64(getCurrentTime());

        StandardBridgeLike(l2GatewayRouter).outboundTransfer(
            whitelistedTokens[l2Token].l1Token, // _l1Token. Address of the L1 token to bridge over.
            whitelistedTokens[l2Token].l1BridgePool, // _to. Withdraw, over the bridge, to the l1 withdraw contract.
            bridgeDepositBoxBalance, // _amount. Send the full balance of the deposit box to bridge.
            "" // _data. We don't need to send any data for the bridging action.
        );

        emit TokensBridged(l2Token, bridgeDepositBoxBalance, l1Gas, msg.sender);
    }
```

`bridgeTokens` 上有一个装饰器 `canBridge` 包含两个判断， `isWhitelistToken` 用于判断对应 L2 层代币是否已经在 L1 层上添加了桥接池， `_hasEnoughTimeElapsedToBridge` 用来减少频繁跨连导致的费用消耗问题，因此设置了最小的跨链接时间。

`bridgeTokens` 主要就是调用了 L2 层原生的跨链方法，比如 `outboundTransfer`。

### `deposit`

第二个是 `deposit` 方法用于将 L2 层资产转移到以太坊 L1 层上，对应与前端页面 Deposit 操作。对应代码为：

```bash
    function bridgeTokens(address l2Token, uint32 l2Gas) public virtual;

    function deposit(
        address l1Recipient,
        address l2Token,
        uint256 amount,
        uint64 slowRelayFeePct,
        uint64 instantRelayFeePct,
        uint64 quoteTimestamp
    ) public payable onlyIfDepositsEnabled(l2Token) nonReentrant() {
        require(isWhitelistToken(l2Token), "deposit token not whitelisted");

        require(slowRelayFeePct <= 0.25e18, "slowRelayFeePct must be <= 25%");
        require(instantRelayFeePct <= 0.25e18, "instantRelayFeePct must be <= 25%");

        require(
            getCurrentTime() >= quoteTimestamp - 10 minutes && getCurrentTime() <= quoteTimestamp + 10 minutes,
            "deposit mined after deadline"
        );
        
        if (whitelistedTokens[l2Token].l1Token == l1Weth && msg.value > 0) {
            require(msg.value == amount, "msg.value must match amount");
            WETH9Like(address(l2Token)).deposit{ value: msg.value }();
        }
        else IERC20(l2Token).safeTransferFrom(msg.sender, address(this), amount);

        emit FundsDeposited(
            chainId,
            numberOfDeposits, // depositId: the current number of deposits acts as a deposit ID (nonce).
            l1Recipient,
            msg.sender,
            whitelistedTokens[l2Token].l1Token,
            l2Token,
            amount,
            slowRelayFeePct,
            instantRelayFeePct,
            quoteTimestamp
        );

        numberOfDeposits += 1;
    }
```

其中，合约区分了 ETH 和 ERC20 代币的存入方式。

存入资产后，合约产生了一个事件 `FundsDeposited`，用于中继者程序捕获并进行资产跨链，事件信息包含合约部署的 L2 链ID，存款ID `numberOfDeposits`，L1层接收者，存款者，L1和L2层代币地址，数量和费率，以及时间戳。

## BridgePool

`BridgePool` 合约部署在 Layer 1 上，提供了给中继者完成 Layer2 上存款订单的函数。主要包含以下功能：

1.  流动性提供者添加和删除流动性的方法 `addLiquidity`， `removeLiquidity`；
2. 慢速中继： `relayDeposit`
3. 即时中继： `relayAndSpeedUp`， `speedUpRelay`
4. 争议： `disputeRelay`
5. 解决中继： `settleRelay`

### 构造器

在合约初始时，合约设置了对应的桥管理员地址，L1代币地址，每秒的 LP 费率，以及标识是否为 WETH 池。同时，通过 `syncUmaEcosystemParams` 和 `syncWithBridgeAdminParams` 两个方法同步了 Optimistic Oracle 地址信息，Store 的地址信息，以及对应的 `ProposerBondPct` ， `OptimisticOracleLiveness` 等参数。

```solidity
    function syncUmaEcosystemParams() public nonReentrant() {
        FinderInterface finder = FinderInterface(bridgeAdmin.finder());
        optimisticOracle = SkinnyOptimisticOracleInterface(
            finder.getImplementationAddress(OracleInterfaces.SkinnyOptimisticOracle)
        );

        store = StoreInterface(finder.getImplementationAddress(OracleInterfaces.Store));
        l1TokenFinalFee = store.computeFinalFee(address(l1Token)).rawValue;
    }

		function syncWithBridgeAdminParams() public nonReentrant() {
        proposerBondPct = bridgeAdmin.proposerBondPct();
        optimisticOracleLiveness = bridgeAdmin.optimisticOracleLiveness();
        identifier = bridgeAdmin.identifier();
    }

		constructor(
        string memory _lpTokenName,
        string memory _lpTokenSymbol,
        address _bridgeAdmin,
        address _l1Token,
        uint64 _lpFeeRatePerSecond,
        bool _isWethPool,
        address _timer
    ) Testable(_timer) ERC20(_lpTokenName, _lpTokenSymbol) {
        require(bytes(_lpTokenName).length != 0 && bytes(_lpTokenSymbol).length != 0, "Bad LP token name or symbol");
        bridgeAdmin = BridgeAdminInterface(_bridgeAdmin);
        l1Token = IERC20(_l1Token);
        lastLpFeeUpdate = uint32(getCurrentTime());
        lpFeeRatePerSecond = _lpFeeRatePerSecond;
        isWethPool = _isWethPool;

        syncUmaEcosystemParams(); // Fetch OptimisticOracle and Store addresses and L1Token finalFee.
        syncWithBridgeAdminParams(); // Fetch ProposerBondPct OptimisticOracleLiveness, Identifier from the BridgeAdmin.

        emit LpFeeRateSet(lpFeeRatePerSecond);
    }
```

### 添加和删除流动性

我们首先看到添加和删除流动性，添加流动性即流动性提供者向连接池中提供 L1 代币，并获取相应数量的 LP 代币作为证明，LP 代币数量根据现行汇率计算。

```solidity
    function addLiquidity(uint256 l1TokenAmount) public payable nonReentrant() {
				// 如果是 weth 池，调用发送 msg.value，msg.value 与 l1TokenAmount 相同
				// 否则，msg.value 必需为 0
        require((isWethPool && msg.value == l1TokenAmount) || msg.value == 0, "Bad add liquidity Eth value");

			  // 由于 `_exchangeRateCurrent()` 读取合约的余额并使用它更新合约状态，
				// 因此我们必需在转入任何代币之前调用
        uint256 lpTokensToMint = (l1TokenAmount * 1e18) / _exchangeRateCurrent();
        _mint(msg.sender, lpTokensToMint);
        liquidReserves += l1TokenAmount;

        if (msg.value > 0 && isWethPool) WETH9Like(address(l1Token)).deposit{ value: msg.value }();
        else l1Token.safeTransferFrom(msg.sender, address(this), l1TokenAmount);

        emit LiquidityAdded(l1TokenAmount, lpTokensToMint, msg.sender);
    }
```

由于合约支持 WETH 作为流动性池，因此添加流动性区分了 WETH 和其他 ERC20 代币的添加方法。

此处的难点在于 LP 代币和 L1 代币之间的汇率换算 `_exchangeRateCurrent` 的实现，我们从合约中提取出了 `_exchangeRateCurrent` 所使用的函数，包括 `_updateAccumulatedLpFees` 和 `_sync` ：

```solidity
	
		function _getAccumulatedFees() internal view returns (uint256) {
        uint256 possibleUnpaidFees =
            (undistributedLpFees * lpFeeRatePerSecond * (getCurrentTime() - lastLpFeeUpdate)) / (1e18);
        return possibleUnpaidFees < undistributedLpFees ? possibleUnpaidFees : undistributedLpFees;
    }

    function _updateAccumulatedLpFees() internal {
        uint256 unallocatedAccumulatedFees = _getAccumulatedFees();

        undistributedLpFees = undistributedLpFees - unallocatedAccumulatedFees;

        lastLpFeeUpdate = uint32(getCurrentTime());
    }

		function _sync() internal {
        uint256 l1TokenBalance = l1Token.balanceOf(address(this)) - bonds;
        if (l1TokenBalance > liquidReserves) {
            
            utilizedReserves -= int256(l1TokenBalance - liquidReserves);
            liquidReserves = l1TokenBalance;
        }
    }
    
		function _exchangeRateCurrent() internal returns (uint256) {
        if (totalSupply() == 0) return 1e18; // initial rate is 1 pre any mint action.

        _updateAccumulatedLpFees();
        _sync();

        int256 numerator = int256(liquidReserves) + utilizedReserves - int256(undistributedLpFees);
        return (uint256(numerator) * 1e18) / totalSupply();
    }
```

换算汇率等于当前合约中代币的储备与总 LP 供应量的比值，计算步骤如下：

1. 更新自上次方法调用以来的累积LP费用 `_updateAccumulatedLpFees`
    1. 计算可能未付的费用 `possibleUnpaidFees` ，等于未分配的 Lp 费用 `undistributedLpFees` * 每秒 LP 费率 *（当前时间-上次更新时间），目前 WETH 桥接池中每秒LP费率为 0.0000015。
    2. 计算累积费用 `unallocatedAccumulatedFees` ，如果 `possibleUnpaidFees` 小于未分配的 Lp 费用，则所有未分配的 LP 费用都将用于累积费用；
    3. 当前未分配 LP 费用 = 原先未分配 LP 费用 - 累积费用；
2. 计算由于代币桥接产生的余额变化
    1. 当前合约中的代币储备=当前合约中的代币数量 - 被绑定在中继过程中的代币数量；
    2. 如果当前合约中的代币储备大于流动储备 `liquidReserves`，则被使用的储备  `utilizedReserves` = 原先被使用的储备 -（当前合约中的代币储备 - 流动储备）；
    3. 当前流动性储备 = 当前合约中的代币储备；
3. 计算汇率：
    1. 经过更新之后，汇率计算的分子：流动储备 + 被使用的储备 - 未被分配 LP 费用；
    2. 分子与LP 代币总供应量的比值即为换算汇率。

利用换算汇率，可以计算得到添加 `l1TokenAmount` 数量的代币时所能得到的 LP 代币的数量。

对于移除流动性，过程与添加流动性相反，这里不再赘述。

```solidity
    function removeLiquidity(uint256 lpTokenAmount, bool sendEth) public nonReentrant() {
        // 如果是 WETH 池，则只能通过发送 ETH 来取出流动性
        require(!sendEth || isWethPool, "Cant send eth");
        uint256 l1TokensToReturn = (lpTokenAmount * _exchangeRateCurrent()) / 1e18;

        // 检查是否有足够的流储备来支持取款金额
        require(liquidReserves >= (pendingReserves + l1TokensToReturn), "Utilization too high to remove");

        _burn(msg.sender, lpTokenAmount);
        liquidReserves -= l1TokensToReturn;

        if (sendEth) _unwrapWETHTo(payable(msg.sender), l1TokensToReturn);
        else l1Token.safeTransfer(msg.sender, l1TokensToReturn);

        emit LiquidityRemoved(l1TokensToReturn, lpTokenAmount, msg.sender);
    }
```

### 慢速中继

慢速中继，以及之后要讨论的即时中继，都会用到 `DepositData` 和 `RelayData` 这两个数据，前者表示存框交易的数据，后者表示中继交易的信息。

```solidity
		// 来自 L2 存款交易的数据。
    struct DepositData {
        uint256 chainId;
        uint64 depositId;
        address payable l1Recipient;
        address l2Sender;
        uint256 amount;
        uint64 slowRelayFeePct;
        uint64 instantRelayFeePct;
        uint32 quoteTimestamp;
    }

		// 每个 L2 存款在任何时候都可以进行一次中继尝试。 中继尝试的特征在于其 RelayData。
    struct RelayData {
        RelayState relayState;
        address slowRelayer;
        uint32 relayId;
        uint64 realizedLpFeePct;
        uint32 priceRequestTime;
        uint256 proposerBond;
        uint256 finalFee;
    }
```

下面我们看到 `relayDeposit` 方法，这个方法由中继者调用，执行从 L2 到 L1 的慢速中继。对于每一个存款而言，只能有一个待处理的中继，这个待处理的中继不包括有争议的中继。

```solidity
    function relayDeposit(DepositData memory depositData, uint64 realizedLpFeePct)
        public
        onlyIfRelaysEnabld()
        nonReentrant()
    {
				// realizedLPFeePct 不超过 50%，慢速和即时中继费用不超过25%，费用合计不超过100%
        require(
            depositData.slowRelayFeePct <= 0.25e18 &&
                depositData.instantRelayFeePct <= 0.25e18 &&
                realizedLpFeePct <= 0.5e18,
            "Invalid fees"
        );

        // 查看是否已经有待处理的中继
        bytes32 depositHash = _getDepositHash(depositData);

				// 对于有争议的中继，relays 中对应的 hash 会被删除，这个条件可以通过
        require(relays[depositHash] == bytes32(0), "Pending relay exists");

				// 如果存款没有正在执行的中继，则关联调用者的中继尝试
        uint32 priceRequestTime = uint32(getCurrentTime());

        uint256 proposerBond = _getProposerBond(depositData.amount);

        // 保存新中继尝试参数的哈希值。
        // 注意：这个中继的活跃时间（liveness）可以在 BridgeAdmin 中更改，这意味着每个中继都有一个潜在的可变活跃时间。
				// 这不应该提供任何被利用机会，特别是因为 BridgeAdmin 状态（包括 liveness 值）被许可给跨域所有者。
				RelayData memory relayData =
            RelayData({
                relayState: RelayState.Pending,
                slowRelayer: msg.sender,
                relayId: numberOfRelays++, // 注意：在将 relayId 设置为其当前值的同时增加 numberOfRelays。
                realizedLpFeePct: realizedLpFeePct,
                priceRequestTime: priceRequestTime,
                proposerBond: proposerBond,
                finalFee: l1TokenFinalFee
            });
        relays[depositHash] = _getRelayDataHash(relayData);

        bytes32 relayHash = _getRelayHash(depositData, relayData);

				// 健全性检查池是否有足够的余额来支付中继金额 + 提议者奖励。 OptimisticOracle 价格请求经过挑战期后，将在结算时支付奖励金额。
        // 注意：liquidReserves 应该总是 <= balance - bonds。
        require(liquidReserves - pendingReserves >= depositData.amount, "Insufficient pool balance");

				// 计算总提议保证金并从调用者那里拉取，以便 OptimisticOracle 可以从这里拉取它。
        uint256 totalBond = proposerBond + l1TokenFinalFee;
        pendingReserves += depositData.amount; // 在正在处理的准备中预订此中继使用的最大流动性。
        bonds += totalBond;

        l1Token.safeTransferFrom(msg.sender, address(this), totalBond);
        emit DepositRelayed(depositHash, depositData, relayData, relayHash);
    }
```

可以看到，存款哈希与 `depositData` 有关，中继哈希与 `depositData` 和 `relayData` 都有关。最后我们可以看到， `relayDeposit` 还未实际付款给用户的 L1 地址，需要等待中继者处理，或者通过加速处理中继。

### 加速中继

`speedUpRelay` 方法立即将存款金额减去费用后转发给 `l1Recipient`，即时中继者在待处理的中继挑战期后获得奖励。

```solidity
    // 我们假设调用者已经执行了链外检查，以确保他们尝试中继的存款数据是有效的。
		// 如果存款数据无效，则即时中继者在无效存款数据发生争议后无权收回其资金。
		// 此外，没有人能够重新提交无效存款数据的中继，因为他们知道这将再次引起争议。
		// 另一方面，如果存款数据是有效的，那么即使它被错误地争议，即时中继者最终也会得到补偿，
		// 因为会激励其他人重新提交中继，以获得慢中继者的奖励。
		// 一旦有效中继最终确定，即时中继将得到补偿。因此，调用者在验证中继数据方面与争议者具有相同的责任。
		function speedUpRelay(DepositData memory depositData, RelayData memory relayData) public nonReentrant() {
        bytes32 depositHash = _getDepositHash(depositData);
        _validateRelayDataHash(depositHash, relayData);
        bytes32 instantRelayHash = _getInstantRelayHash(depositHash, relayData);
        require(
            // 只能在没有与之关联的现有即时中继的情况下加速待处理的中继。
            getCurrentTime() < relayData.priceRequestTime + optimisticOracleLiveness &&
                relayData.relayState == RelayState.Pending &&
                instantRelays[instantRelayHash] == address(0),
            "Relay cannot be sped up"
        );
        instantRelays[instantRelayHash] = msg.sender;

        // 从调用者那里提取中继金额减去费用并发送存款到 l1Recipient。
				// 支付的总费用是 LP 费用、中继费用和即时中继费用的总和。
        uint256 feesTotal =
            _getAmountFromPct(
                relayData.realizedLpFeePct + depositData.slowRelayFeePct + depositData.instantRelayFeePct,
                depositData.amount
            );
        // 如果 L1 代币是 WETH，那么：a) 从即时中继者提取 WETH b) 解包 WETH 为 ETH c) 将 ETH 发送给接收者。
        uint256 recipientAmount = depositData.amount - feesTotal;
        if (isWethPool) {
            l1Token.safeTransferFrom(msg.sender, address(this), recipientAmount);
            _unwrapWETHTo(depositData.l1Recipient, recipientAmount);
            // 否则，这是一个普通的 ERC20 代币。 发送给收件人。
        } else l1Token.safeTransferFrom(msg.sender, depositData.l1Recipient, recipientAmount);

        emit RelaySpedUp(depositHash, msg.sender, relayData);
    }
```

### 即时中继

`relayAndSpeedUp` 执行即时中继。这个方法的函数内容与 `relayDeposit` 和 `speedUpRelay` 方法是一致的，这里就不具体注释了，可以参考前文中的注释。这个函数的代码几乎是直接将 `relayDeposit` 和 `speedUpRelay` 的代码进行了合并，代码冗余。

```solidity
    // 由 Relayer 调用以执行从 L2 到 L1 的慢 + 快中继，完成相应的存款订单。
    // 存款只能有一个待处理的中继。此方法实际上是串联的 relayDeposit 和 speedUpRelay 方法。
		// 这可以重构为只调用每个方法，但是结合传输和哈希计算可以节省一些 gas。
		function relayAndSpeedUp(DepositData memory depositData, uint64 realizedLpFeePct)
        public
        onlyIfRelaysEnabld()
        nonReentrant()
    {
        uint32 priceRequestTime = uint32(getCurrentTime());

        require(
            depositData.slowRelayFeePct <= 0.25e18 &&
                depositData.instantRelayFeePct <= 0.25e18 &&
                realizedLpFeePct <= 0.5e18,
            "Invalid fees"
        );

        bytes32 depositHash = _getDepositHash(depositData);

        require(relays[depositHash] == bytes32(0), "Pending relay exists");

        uint256 proposerBond = _getProposerBond(depositData.amount);

        RelayData memory relayData =
            RelayData({
                relayState: RelayState.Pending,
                slowRelayer: msg.sender,
                relayId: numberOfRelays++, // Note: Increment numberOfRelays at the same time as setting relayId to its current value.
                realizedLpFeePct: realizedLpFeePct,
                priceRequestTime: priceRequestTime,
                proposerBond: proposerBond,
                finalFee: l1TokenFinalFee
            });
        bytes32 relayHash = _getRelayHash(depositData, relayData);
        relays[depositHash] = _getRelayDataHash(relayData);

        bytes32 instantRelayHash = _getInstantRelayHash(depositHash, relayData);
        require(
            instantRelays[instantRelayHash] == address(0),
            "Relay cannot be sped up"
        );

        require(liquidReserves - pendingReserves >= depositData.amount, "Insufficient pool balance");

        uint256 totalBond = proposerBond + l1TokenFinalFee;

        uint256 feesTotal =
            _getAmountFromPct(
                relayData.realizedLpFeePct + depositData.slowRelayFeePct + depositData.instantRelayFeePct,
                depositData.amount
            );
        uint256 recipientAmount = depositData.amount - feesTotal;

        bonds += totalBond;
        pendingReserves += depositData.amount;

        instantRelays[instantRelayHash] = msg.sender;

        l1Token.safeTransferFrom(msg.sender, address(this), recipientAmount + totalBond);

        if (isWethPool) {
            _unwrapWETHTo(depositData.l1Recipient, recipientAmount);
        } else l1Token.safeTransfer(depositData.l1Recipient, recipientAmount);

        emit DepositRelayed(depositHash, depositData, relayData, relayHash);
        emit RelaySpedUp(depositHash, msg.sender, relayData);
    }
```

### 争议

当对待处理的中继提出争议时，争议者需要想 Optimistic Oracle 提交提案，并等待争议解决。

```solidity
    // 由 Disputer 调用以对待处理的中继提出争议。
		// 这个方法的结果是总是抛出中继，为另一个中继者提供处理相同存款的机会。
		// 在争议者和提议者之间，谁不正确，谁就失去了他们的质押。谁是正确的，谁就拿回来并获得一笔钱。
		function disputeRelay(DepositData memory depositData, RelayData memory relayData) public nonReentrant() {
        require(relayData.priceRequestTime + optimisticOracleLiveness > getCurrentTime(), "Past liveness");
        require(relayData.relayState == RelayState.Pending, "Not disputable");
        // 检验输入数据
        bytes32 depositHash = _getDepositHash(depositData);
        _validateRelayDataHash(depositHash, relayData);

        // 将提案和争议提交给 Optimistic Oracle。
        bytes32 relayHash = _getRelayHash(depositData, relayData);

        // 注意：在某些情况下，这会由于 Optimistic Oracle 的变化而失败，并且该方法将退还中继者。
        bool success =
            _requestProposeDispute(
                relayData.slowRelayer,
                msg.sender,
                relayData.proposerBond,
                relayData.finalFee,
                _getRelayAncillaryData(relayHash)
            );

				// 放弃中继并从跟踪的保证金中移除中继的保证金。
        bonds -= relayData.finalFee + relayData.proposerBond;
        pendingReserves -= depositData.amount;
        delete relays[depositHash];
        if (success) emit RelayDisputed(depositHash, _getRelayDataHash(relayData), msg.sender);
        else emit RelayCanceled(depositHash, _getRelayDataHash(relayData), msg.sender);
    }
```

其中， `_requestProposeDispute` 的函数内容如下：

```solidity
    // 向 optimistic oracle 提议与 `customAncillaryData` 相关的中继事件的新价格为真。
		// 如果有人不同意中继参数，不管他们是否映射到 L2 存款，他们可以与预言机争议。
    function _requestProposeDispute(
        address proposer,
        address disputer,
        uint256 proposerBond,
        uint256 finalFee,
        bytes memory customAncillaryData
    ) private returns (bool) {
        uint256 totalBond = finalFee + proposerBond;
        l1Token.safeApprove(address(optimisticOracle), totalBond);
        try
            optimisticOracle.requestAndProposePriceFor(
                identifier,
                uint32(getCurrentTime()),
                customAncillaryData,
                IERC20(l1Token),
                // 将奖励设置为 0，因为在中继提案经过挑战期后，我们将直接从该合约中结算提案人奖励支出。
                0,
                // 为价格请求设置 Optimistic oracle 提议者保证金。
                proposerBond,
                // 为价格请求设置 Optimistic oracle 活跃时间。
                optimisticOracleLiveness,
                proposer,
                // 表示 "True"; 及提议的中继是合法的
                int256(1e18)
            )
        returns (uint256 bondSpent) {
            if (bondSpent < totalBond) {
                // 如果 Optimistic oracle 拉取得更少（由于最终费用的变化），则退还提议者。
                uint256 refund = totalBond - bondSpent;
                l1Token.safeTransfer(proposer, refund);
                l1Token.safeApprove(address(optimisticOracle), 0);
                totalBond = bondSpent;
            }
        } catch {
            // 如果 Optimistic oracle 中出现错误，这意味着已经更改了某些内容以使该请求无可争议。
						// 为确保请求不会默认通过，退款提议者并提前返回，允许调用方法删除请求，但 Optimistic oracle 没有额外的追索权。
            l1Token.safeTransfer(proposer, totalBond);
            l1Token.safeApprove(address(optimisticOracle), 0);

            // 提早返回，注意到提案+争议的尝试没有成功。
            return false;
        }

        SkinnyOptimisticOracleInterface.Request memory request =
            SkinnyOptimisticOracleInterface.Request({
                proposer: proposer,
                disputer: address(0),
                currency: IERC20(l1Token),
                settled: false,
                proposedPrice: int256(1e18),
                resolvedPrice: 0,
                expirationTime: getCurrentTime() + optimisticOracleLiveness,
                reward: 0,
                finalFee: totalBond - proposerBond,
                bond: proposerBond,
                customLiveness: uint256(optimisticOracleLiveness)
            });

        // 注意：在此之前不要提取资金，以避免任何不需要的转账。
        l1Token.safeTransferFrom(msg.sender, address(this), totalBond);
        l1Token.safeApprove(address(optimisticOracle), totalBond);
        // 对我们刚刚发送的请求提出争议。
        optimisticOracle.disputePriceFor(
            identifier,
            uint32(getCurrentTime()),
            customAncillaryData,
            request,
            disputer,
            address(this)
        );

        // 返回 true 表示提案 + 争议调用成功。
        return true;
    }
```

最后，我们来看看 `settleRelay`。

```solidity
    // 如果待处理中继价格请求在 OptimisticOracle 上有可用的价格，则奖励中继者，并将中继标记为完成。
	  // 我们使用 relayData 和 depositData 来计算中继价格请求在 OptimisticOracle 上唯一关联的辅助数据。
		// 如果传入的价格请求与待处理的中继价格请求不匹配，那么这将恢复(revert)。
		function settleRelay(DepositData memory depositData, RelayData memory relayData) public nonReentrant() {
        bytes32 depositHash = _getDepositHash(depositData);
        _validateRelayDataHash(depositHash, relayData);
        require(relayData.relayState == RelayState.Pending, "Already settled");
        uint32 expirationTime = relayData.priceRequestTime + optimisticOracleLiveness;
        require(expirationTime <= getCurrentTime(), "Not settleable yet");

        // 注意：此检查是为了给中继者一小段但合理的时间来完成中继，然后再被其他人“偷走”。
				// 这是为了确保有动力快速解决中继。
        require(
            msg.sender == relayData.slowRelayer || getCurrentTime() > expirationTime + 15 minutes,
            "Not slow relayer"
        );

        // 将中继状态更新为已完成。 这可以防止中继的任何重新设处理。
        relays[depositHash] = _getRelayDataHash(
            RelayData({
                relayState: RelayState.Finalized,
                slowRelayer: relayData.slowRelayer,
                relayId: relayData.relayId,
                realizedLpFeePct: relayData.realizedLpFeePct,
                priceRequestTime: relayData.priceRequestTime,
                proposerBond: relayData.proposerBond,
                finalFee: relayData.finalFee
            })
        );

        // 奖励中继者并支付 l1Recipient。
         // 此时有两种可能的情况：
         // - 这是一个慢速中继：在这种情况下，a) 向慢速中继者支付奖励 b) 向 l1Recipient 支付
         //   金额减去已实现的 LP 费用和慢速中继费用。 转账没有加快，所以没有即时费用。
         // - 这是一个即时中继：在这种情况下，a) 向慢速中继者支付奖励 b) 向即时中继者支付
         //   全部桥接金额，减去已实现的 LP 费用并减去慢速中继费用。
				//    当即时中继者调用 speedUpRelay 时，它们存入的金额相同，减去即时中继者费用。
				//    结果，他们实际上得到了加速中继时所花费的费用 + InstantRelayFee。

        uint256 instantRelayerOrRecipientAmount =
            depositData.amount -
                _getAmountFromPct(relayData.realizedLpFeePct + depositData.slowRelayFeePct, depositData.amount);

        // 如果即时中继参数与批准的中继相匹配，则退款给即时中继者。
        bytes32 instantRelayHash = _getInstantRelayHash(depositHash, relayData);
        address instantRelayer = instantRelays[instantRelayHash];

        // 如果这是 WETH 池并且即时中继者是地址 0x0（即中继没有加速），那么：
        // a) 将 WETH 提取到 ETH 和 b) 将 ETH 发送给接收者。
        if (isWethPool && instantRelayer == address(0)) {
            _unwrapWETHTo(depositData.l1Recipient, instantRelayerOrRecipientAmount);
            // 否则，这是一个正常的慢速中继正在完成，合约将 ERC20 发送给接收者，
						// 或者这是一个即时中继的最终完成，我们需要用 WETH 偿还即时中继者。
        } else
            l1Token.safeTransfer(
                instantRelayer != address(0) ? instantRelayer : depositData.l1Recipient,
                instantRelayerOrRecipientAmount
            );

        // 需要支付费用和保证金。费用归解决者。保证金总是归到慢速中继者。
        // 注意：为了 gas 效率，我们使用 `if`，所以如果它们是相同的地址，我们可以合并这些转账。
        uint256 slowRelayerReward = _getAmountFromPct(depositData.slowRelayFeePct, depositData.amount);
        uint256 totalBond = relayData.finalFee + relayData.proposerBond;
        if (relayData.slowRelayer == msg.sender)
            l1Token.safeTransfer(relayData.slowRelayer, slowRelayerReward + totalBond);
        else {
            l1Token.safeTransfer(relayData.slowRelayer, totalBond);
            l1Token.safeTransfer(msg.sender, slowRelayerReward);
        }

        uint256 totalReservesSent = instantRelayerOrRecipientAmount + slowRelayerReward;

        // 按更改的金额和分配的 LP 费用更新储备。
        pendingReserves -= depositData.amount;
        liquidReserves -= totalReservesSent;
        utilizedReserves += int256(totalReservesSent);
        bonds -= totalBond;
        _updateAccumulatedLpFees();
        _allocateLpFees(_getAmountFromPct(relayData.realizedLpFeePct, depositData.amount));

        emit RelaySettled(depositHash, msg.sender, relayData);

        // 清理状态存储并获得gas退款。
				// 这也可以防止 `priceDisputed()` 重置这个新的 Finalized 中继状态。
        delete instantRelays[instantRelayHash];
    }

    function _allocateLpFees(uint256 allocatedLpFees) internal {
        undistributedLpFees += allocatedLpFees;
        utilizedReserves += int256(allocatedLpFees);
    }
```

至此，我们分析完了 Across 合约的主要功能的代码。

## 合约部署

部署合约目录 `deploy` 下包含 8 脚本，依次部署了管理合约，WETH 桥接池，Optimism，Arbitrum和Boba的信使，以及 Arbitrum，Optimism 和 Boba 的存款合约。由于过程比较简单，这里就不仔细分析了。

```bash
deploy/
├── 001_deploy_across_bridge_admin.js
├── 002_deploy_across_weth_bridge_pool.js
├── 003_deploy_across_optimism_wrapper.js
├── 004_deploy_across_optimism_messenger.js
├── 005_deploy_across_arbitrum_messenger.js
├── 006_deploy_across_boba_messenger.js
├── 007_deploy_across_ovm_bridge_deposit_box.js
└── 008_deploy_across_avm_deposit_box.js
```

## 总结

Across 协议整体结构简单，流程清晰，支持了 Across 协议安全，快速的从 L2 向 L1 的资金转移。

代码中调用了 Optimistic Oracle 的接口来出和解决争议，对应的逻辑有空之后详说。

### Comments

