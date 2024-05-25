# 如何创建一个代币承销商 dApp

这篇教程我们来完成 scaffold-eth 项目的第二个挑战：[代币承销商](https://speedrunethereum.com/challenge/token-vendor)，我们可以在网站 [speedrunethereum.com](http://speedrunethereum.com/) 中查看或者直接查看对应的 Github 连接：[scaffold-eth/scaffold-eth-typescript-challenges](https://github.com/scaffold-eth/scaffold-eth-typescript-challenges)。

这个挑战的目的是创建一个自己的ERC20代币，并编写承销商合约，实现用户对代币的购买和卖出。下面，我们一步步完成这个过程。

<!--more-->

### 一、安装并设置环境

首先，我们下载项目，并初始化环境。

```bash
git clone https://github.com/scaffold-eth/scaffold-eth-typescript-challenges.git challenge-2-token-vendor
cd challenge-2-token-vendor
git checkout challenge-2-token-vendor
yarn install
```

安装好依赖包之后，我们可以看到项目的主要目录为 `packages`，包含一下子目录

```bash
packages/
├── hardhat-ts
├── services
├── subgraph
└── vite-app-ts
```

其中：

- `hardhat-ts` 是项目合约代码，包含合约文件以及合约的部署等；
- `services` The Graph 协议的 graph-node 配置；
- `subgraph` The Graph 协议相应的处理设置，包括 mappings，数据结构等；
- `vite-app-ts` 前端项目，主要负责用户与合约交互。

The Graph 协议是去中心化的区块链数据索引协议，本片教程中暂时不涉及。我们需要启动三个命令终端，分别用于运行以下命令：

- `yarn chain` 使用 hardhat 运行本地区块链，作为合约部署的本地测试链；
- `yarn deploy` 编译、部署和发布合约；
- `yarn start` 启动 react 应用的前端；

按顺序分别运行上述命令之后，此时我们就可以在 `http://localhost:3000`中访问我们的应用。如果需要重新部署合约，运行 `yarn deploy --reset` 即可。

![yarn-start](https://user-images.githubusercontent.com/3297411/155913563-c0e773b7-60d1-4e5f-bdf7-2c4b0ae1df74.png)

## 二、编写 ERC20 代币合约

现在我们进入合约编写部分。我们的目标是编写一个 ERC20 代币合约，并为创建者铸造 1000 个代币。

### 什么是 ERC20 合约标准

代币可以在以太坊中表示任何东西，比如信誉积分，黄金等，而 ERC-20 提供了一个同质化代币的标准，每个代币与另一个代币（在类型和价值上）完全相同。

ERC20是各个代币的标准接口，包含以下方法：

```solidity
// 名称
function name() public view returns (string)
// 符号
function symbol() public view returns (string)
// 合约使用的小数位，常见为 18
function decimals() public view returns (uint8)
// 代币总供应量
function totalSupply() public view returns (uint256)
// 地址的代币持有量
function balanceOf(address _owner) public view returns (uint256 balance)
// 代币划转
function transfer(address _to, uint256 _value) public returns (bool success)
// 用于划转代币，但这些代币不一定属于调用合约的用户
function transferFrom(address _from, address _to, uint256 _value) public returns (bool success)
// 合约授予用户代币管理权限，调用者设置 spender 消费自己 amount 数量的代币
function approve(address _spender, uint256 _value) public returns (bool success)
// 检查代币的可消费余额
function allowance(address _owner, address _spender) public view returns (uint256 remaining)

// 事件
// 代币转移事件
event Transfer(address indexed from, address indexed to, uint256 value);
// 当调用 approve 时，触发 Approval 事件
event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
);
```

其中，合约必需设置 `totalSupply`、 `balanceOf` 、 `transfer` 、 `transferFrom`、 `approve` 以及 `allowance` 这六个函数，其他如 `name`、 `symbol` 和 `decimalsze` 则是可选实现。

### 使用 OpenZeppelin 库

如果从上述的合约标准开始，我们需要实现这六个函数的方法，幸运的是，OpenZeppelin 库是一个成熟的合约开发库，为我们实现了 ERC20 代币基本功能，我们可以基于这个库开发我们的 ERC20 代币，这将大大减少我们的工作量。我们可以在 [ERC20 标准](https://docs.openzeppelin.com/contracts/4.x/erc20) 页面查到相关的使用方法。

除了 ERC20，OpenZeppelin 库还提供了其他合约标准的实现，比如 ERC721，ERC777等，以及大量的经过安全审计的库，这些对于我们快速开发和实现安全的合约代码提供了支持。

### 编写代码

我们使用 ERC20.sol 来实现我们的合约，创见一个名为 `GOLD` 的代币，代币符号为 `GLD`，并为创建者铸造 1000 个代币：

```bash
pragma solidity >=0.8.0 <0.9.0;
// SPDX-License-Identifier: MIT

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';

// learn more: https://docs.openzeppelin.com/contracts/3.x/erc20

  constructor() public ERC20('Gold', 'GLD') {
    // 铸造 1000 * 10 ** 18 给 msg.sender
    _mint(msg.sender, 1000 * 10 ** 18);
  }
}
```

其中， `_mint` 方法是 ERC20 提供的方法，该方法创建相应数量的代币，并将代币发送给账户：

```solidity
    /** @dev Creates `amount` tokens and assigns them to `account`, increasing
     * the total supply.
     *
     * Emits a {Transfer} event with `from` set to the zero address.
     *
     * Requirements:
     *
     * - `account` cannot be the zero address.
     */
    function _mint(address account, uint256 amount) internal virtual {
        require(account != address(0), "ERC20: mint to the zero address");

        _beforeTokenTransfer(address(0), account, amount);

        _totalSupply += amount;
        _balances[account] += amount;
        emit Transfer(address(0), account, amount);

        _afterTokenTransfer(address(0), account, amount);
    }
```

代码地址：[https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol#L248](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol#L248)

### 部署脚本

接着我们使用脚本进行部署，并向地址发送 1000 代币，地址可以在 `http://localhost:3000` 中连接我们的 Metamask 得到。部署脚本地址：`packages/hardhat-ts/deploy/00_deploy_your_token.ts`。

```tsx
...

  const yourToken = await ethers.getContract('YourToken', deployer);

  // 发送代币
  const result = await yourToken.transfer('0x169841AA3024cfa570024Eb7Dd6Bf5f774092088', ethers.utils.parseEther('1000'));

...
```

然后我们运行 `yarn deploy --reset` 部署合约。

### 验证

1. 使用 Debug 页面功能进行检查，查看用户账户中的代币余额，可以看到账户中有 1000 个代币；
    
    ![balance](https://user-images.githubusercontent.com/3297411/155913531-951312e7-ea2e-497e-a323-722ecd295ca4.png)
    
2. 使用 `transfer()` 将代币转给另一个账户；
    
    在 Debug 中，使用 `transfer` 功能，输入目标钱包地址 `0xc12ae5Ba30Da6eB11978939379D383beb5Df9b33`，以及发送的数量 `1000000000000000000000`（1000*1E18，1后边有21个0），点击发送。等交易完成之后，可以分别查看原来账户和目标账户的代币数量，可以看到原来的变成了 0，目标账户是 1000。
    
    ![transfer](https://user-images.githubusercontent.com/3297411/155913544-122451a0-8533-46cf-9aa3-7f90e8fa59ab.png)
    
注意：

- 如果发送时出现余额不足的提示，可以使用页面左下角的 Faucet 为账户充值。
- 验证完成之后，需要将 `00_deploy_your_token.ts` 中的 transfer 代码注释了，不然会影响之后的步骤。

## 三、承销商合约 — 购买

接下来，我们创建一个承销商合约，这个合约允许用户通过以太购买代币。

为了完成这个功能，我们需要：

1. 设置兑换比例，教程中为 `tokensPerEth=100` ，也就是 1个以太可以兑换 100 GLD；
2. 实现 `buyTokens` 函数，这个函数必须是 `payable`，可以接受发送的以太，计算对应的 `GLD` 数量，然后使用 `transfer` 将相应的 `GLD` 代币发送给购买者 `msg.sender`；
3. 触发一个 `BuyTokens` 事件，记录购买者，使用的 ETH 数量以及购买的 GLD 数量；
4. 实现第二个函数 `withdraw`，用来将合约中的 ETH 全部提取到合约的所有者（owner）地址。我们可以使用两种方式设置合约的所有者：
    1. 部署时，使用我们能控制的钱包地址进行部署，并设置所有者；
    2. 使用任意地址部署，部署结束之后进行合约所有权转移；

在这个教程中，我们使用第二个方式，这样我们可以不用将我们控制的地址的私钥添加到项目配置中，降低暴露。

```solidity
pragma solidity >=0.8.0 <0.9.0;
// SPDX-License-Identifier: MIT

import "@openzeppelin/contracts/access/Ownable.sol";
import './YourToken.sol';

contract Vendor is Ownable {
  YourToken yourToken;
  uint256 public tokensPerEth = 100;

  // 购买代币事件
  event BuyTokens(address buyer, uint256 amountOfEth, uint256 amountOfTokens);

  constructor(address tokenAddress) public {
    yourToken = YourToken(tokenAddress);
  }

  // 允许用户使用 EHT 购买代币
  function buyTokens() payable public {
    // 检查是否有足够的 ETH
    require(msg.value > 0, "Not enought ether");

    uint256 amountOfTokens = msg.value * tokensPerEth;

    // 检查承销商是否有足够的代币
    uint256 tokenBalance = yourToken.balanceOf(address(this));
    require(tokenBalance > amountOfTokens, "Not enought tokens");
    
    // 发送代币
    bool sent =  yourToken.transfer(msg.sender, amountOfTokens);
    require(sent, "Failed to transfer token to the buyer");

    emit BuyTokens(msg.sender, msg.value, amountOfTokens);
  }

  // 允许所有者取出所有代币
  function withdraw() public onlyOwner {

    uint256 balance = address(this).balance;
    require(balance > 0, "No ether to withdraw");
    
    // 发送代币给所有者
    (bool sent, ) = msg.sender.call{value: balance}("");
    require(sent, "Failed to withdraw balance");
  }
    

  // ToDo: create a sellTokens() function:
}
```

其中， `Ownable` 可以进行权限控制，合约提供的`onlyOwner`修改器可以用来限制某些特定合约函数的访问权限。在这里，我们的 `withdraw` 函数必需限制合约的所有这才能提取所有的资金。同时，这个合约提供了 `transferOwnership` 函数，可以用来转移合约的所有者，这个将在我们的脚本部分中使用。

对于部署脚本，我们需要完成以下功能：

1. 在部署的时候将所有的代币发送到承销商的合约地址 `vendor.address` ，而不是我们之前的地址；
2. 为了能将承销商合约中的所有 ETH 提取出来，需要将合约的所有权 `ownership` 转移到我们能控制的地址，比如我们在前端使用的地址。

脚本位置： `packages/hardhat-ts/deploy/01_deploy_vendor.ts`

```tsx
  // You might need the previously deployed yourToken:
  const yourToken = await ethers.getContract('YourToken', deployer);

  // 部署承销商合约
  await deploy('Vendor', {
    // Learn more about args here: https://www.npmjs.com/package/hardhat-deploy#deploymentsdeploy
    from: deployer,
    args: [yourToken.address],
    log: true,
  });
	// 获取部署的合约
  const vendor = await ethers.getContract('Vendor', deployer);

  // 发送 1000 个代币给承销商
  console.log('\n 🏵  Sending all 1000 tokens to the vendor...\n');
  await yourToken.transfer(vendor.address, ethers.utils.parseEther('1000'));

  // 转移所有权
  await vendor.transferOwnership('0x169841AA3024cfa570024Eb7Dd6Bf5f774092088');
```

### 部署合约

完成上述代码之后，我们重新部署我们的合约：

```tsx
yarn deploy --reset
```

对应的输出结果为：

```tsx
$ yarn deploy --reset

Compiling 7 files with 0.8.6
Generating typings for: 7 artifacts in dir: ../vite-app-ts/src/generated/contract-types for target: ethers-v5
Successfully generated 15 typings!
Compilation finished successfully
deploying "YourToken" (tx: 0x758e492bc71e9de37cf109aa6aa966fc6c042d086babce32ddd76af02ec22acb)...: deployed at 0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82 with 639137 gas
deploying "Vendor" (tx: 0x7b0402937081b72f59abb9994e3773b0283116e1106665766af31bf246b466cc)...: deployed at 0x9A676e781A523b5d0C0e43731313A708CB607508 with 482680 gas

 🏵  Sending all 1000 tokens to the vendor...
```

可以从命令行输出中看到合约部署的地址为：

- 承销商合约地址： `0x9A676e781A523b5d0C0e43731313A708CB607508`
- 代币地址： `0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82`

### 验证

我们通过以下步骤进行验证：

1. 通过 Debug 页面查看承销商 （Vendor）合约地址初始时是否有 1000 个代币；
2. 使用 0.1 ETH 购买 10 个 GLD：我们使用 Buy Tokens 功能购买 10 个代币，可以看到此时的价格约为 0.1 ETH（ETH 价格为 2766.7 美元）。
    
    ![buyTokens](https://user-images.githubusercontent.com/3297411/155913532-492474ae-5a67-4fcc-8c37-eb768c8ae18e.png)
    
3. 将购买的代币发送给另一个账户：同样使用页面 Transfer Tokens 功能完成；
    
    ![tokenBalance](https://user-images.githubusercontent.com/3297411/155913543-fe8f7c93-aa6b-4333-8c3f-87dd30ced5d6.png)
    
4. 使用所有者账户，查看是否能全部取出合约中的 ETH：在 Debug 页面，我们使用 `withdraw` 功能，尝试将承销商合约中的 ETH 全部取出，可以看到，当交易完成以后，合约的余额变为了0：
    
    
    ![vendorBalanceBefore](https://user-images.githubusercontent.com/3297411/155913554-5f0e78f5-0836-4d53-b0b8-adb44a37413c.png)
    
    变为：
    
    ![vendorBalanceAfter](https://user-images.githubusercontent.com/3297411/155913548-289343ef-d51a-4fbb-8134-071918589636.png)
    

## 四、承销商合约 — 回购

接下来我们添加承销商合约的回购代币功能，也就是允许用户通过发送代币给承销商合约，承销商合约将对应的ETH发给用户账户。但是在以太坊中，合约只能通过 payable 接受 ETH，无法接受直接发送代币，如果直接向合约发送代币，代币将会永久消失。所以在 ERC20 标准中，我们需要使用 `approve` 和 `tranferFrom` 者两个函数来完成这个过程。

```tsx
approve(address spender, uint256 amount) -> bool
transferFrom(address from, address to, uint256 amount) -> bool
```

首先，用户通过调用 `approve` 函数授权承销商合约（ `spender` ）处理 `amount` 数量的代币，然后，调用 `transferFrom` 函数将代币从用户账户（ `from` ）转移 `amount` 数量的代币给承销商合约（ `to` ）。这其中的难点在于 `approve` 和 `transferFrom` 函数。我们来看一下这两个函数在 OpenZeppelin 中具体实现，首先是 `approve`：

```solidity
    mapping(address => mapping(address => uint256)) private _allowances;

		/**
     * @dev See {IERC20-approve}.
     *
     * NOTE: If `amount` is the maximum `uint256`, the allowance is not updated on
     * `transferFrom`. This is semantically equivalent to an infinite approval.
     *
     * Requirements:
     *
     * - `spender` cannot be the zero address.
     */
    function approve(address spender, uint256 amount) public virtual override returns (bool) {
        address owner = _msgSender();
        _approve(owner, spender, amount);
        return true;
    }

    /**
     * @dev Sets `amount` as the allowance of `spender` over the `owner` s tokens.
     *
     * This internal function is equivalent to `approve`, and can be used to
     * e.g. set automatic allowances for certain subsystems, etc.
     *
     * Emits an {Approval} event.
     *
     * Requirements:
     *
     * - `owner` cannot be the zero address.
     * - `spender` cannot be the zero address.
     */
    function _approve(
        address owner,
        address spender,
        uint256 amount
    ) internal virtual {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
```

从上面可以看出， `approve` 函数调用了 `_approve`， `_approve` 中用 `_allowances` 这个哈希记录了 `owner` 和 `spender` 之间的授权数量 `amount`。因此可以推断， `transferFrom` 函数以及其他需要授权情况的函数都使用了 `_allowances` 这个变量，比如 `allowance` 函数。

```solidity
    /**
     * @dev See {IERC20-allowance}.
     */
    function allowance(address owner, address spender) public view virtual override returns (uint256) {
        return _allowances[owner][spender];
    }

    /**
     * @dev Updates `owner` s allowance for `spender` based on spent `amount`.
     *
     * Does not update the allowance amount in case of infinite allowance.
     * Revert if not enough allowance is available.
     *
     * Might emit an {Approval} event.
     */
    function _spendAllowance(
        address owner,
        address spender,
        uint256 amount
    ) internal virtual {
        uint256 currentAllowance = allowance(owner, spender);
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "ERC20: insufficient allowance");
            unchecked {
                _approve(owner, spender, currentAllowance - amount);
            }
        }
    }

    /**
     * @dev Moves `amount` of tokens from `sender` to `recipient`.
     *
     * This internal function is equivalent to {transfer}, and can be used to
     * e.g. implement automatic token fees, slashing mechanisms, etc.
     *
     * Emits a {Transfer} event.
     *
     * Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `from` must have a balance of at least `amount`.
     */
    function _transfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");

        _beforeTokenTransfer(from, to, amount);

        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: transfer amount exceeds balance");
        unchecked {
            _balances[from] = fromBalance - amount;
        }
        _balances[to] += amount;

        emit Transfer(from, to, amount);

        _afterTokenTransfer(from, to, amount);
    }

    /**
     * @dev See {IERC20-transferFrom}.
     *
     * Emits an {Approval} event indicating the updated allowance. This is not
     * required by the EIP. See the note at the beginning of {ERC20}.
     *
     * NOTE: Does not update the allowance if the current allowance
     * is the maximum `uint256`.
     *
     * Requirements:
     *
     * - `from` and `to` cannot be the zero address.
     * - `from` must have a balance of at least `amount`.
     * - the caller must have allowance for ``from``'s tokens of at least
     * `amount`.
     */
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) public virtual override returns (bool) {
        address spender = _msgSender();
        _spendAllowance(from, spender, amount);
        _transfer(from, to, amount);
        return true;
    }
```

在 `transferFrom` 函数中，先使用 `_spendAllowance` 进行授权数量检查并更新授权数量，然后再使用 `_transfer` 进行代币划转，而 `_spendAllowance` 中正是调用了 `allowance` 这个函数。

### 合约实现

合约的函数实现如下：

```tsx
...
  event SellTokens(address seller, uint256 amountOfTokens, uint256 amountOfETH);

...

  // 允许用户使用代币换回 ETH
  function sellTokens(uint256 amountToSell) public {
    // 价差是否合理
    require(amountToSell > 0, "Amount to sell must be greater than 0");
    
    // 检查用户是否有足够的代币
    uint256 userBalance = yourToken.balanceOf(msg.sender));
    require(userBalance >= amountToSell, "Not enought tokens");

    // 检查承销商是否有足够的 ETH
    uint256 amountOfEthNeeded = amountToSell / tokensPerEth;
    uint256 venderBalance = address(this).balance;
    require(amountOfEthNeeded <= venderBalance, "Not enought ether");

    // 用户发送代币给承销商
    bool sent =  yourToken.transferFrom(msg.sender, address(this), amountToSell);
    require(sent, "Failed to transfer tokens from seller to vender");

    // 承销商发送 ETH 给用户
    (bool sent, ) = msg.sender.call{value: amountOfEthNeeded}("");
    require(sent, "Failed to send ether from vender to seller");

    emit SellTokens(msg.sender, amountToSell, amountOfEthNeeded);
  }

```

### 部署合约

我们再次部署新的合约：

```tsx
$ yarn deploy --reset
Compiling 7 files with 0.8.6

Generating typings for: 7 artifacts in dir: ../vite-app-ts/src/generated/contract-types for target: ethers-v5
Successfully generated 15 typings!
Compilation finished successfully
deploying "YourToken" (tx: 0xd087814faeb6a8f1a7205d443550419b68d252bcd071e30c7965844105b761ac)...: deployed at 0x68B1D87F95878fE05B998F19b66F4baba5De1aed with 639137 gas
deploying "Vendor" (tx: 0xafaf257948f8c87e0a836eac6e2bbc1ec38026a5c2a0dfc0f71823a4ace635fd)...: deployed at 0x3Aa5ebB10DC797CAC828524e59A333d0A371443c with 694098 gas

 🏵  Sending all 1000 tokens to the vendor...
```

此时，合约地址变为：

- 承销商合约地址： `0x3Aa5ebB10DC797CAC828524e59A333d0A371443c`
- 代币地址： `0x68B1D87F95878fE05B998F19b66F4baba5De1aed`

### 验证

验证过程需要包含两步：

1. 先在 Debug 页面使用代币的 `approve` 允许承销商合约处理 10 个代币：
    
    ![approve](https://user-images.githubusercontent.com/3297411/155913525-657975ef-e67c-4df6-bf03-36eff6801d7e.png)
    
    在 `编辑权限` 中，我们可以查看到授权的代币数量：
    
    ![approveAmount](https://user-images.githubusercontent.com/3297411/155913530-117ea47b-8000-4f8c-be5c-cd21a118ed04.png)
    
2. 使用承销商的 `sellTokens` 将 10 个代币换成 ETH。如果上一步没有使用 `approve` 的话，程序会报错。
    
    ![sellTokens](https://user-images.githubusercontent.com/3297411/155913537-c085ad8b-295b-42b8-8755-ae9a43eec4e9.png)
    

到这一步，我们就完成了合约的编写。

## 五、部署到测试网络

我们将部署合约到测试网络中，使用的测试网络是 `rinkeby` ：

1. 修改以下变量为 `rinkeby` ：
    1.  `packages/hardhat-ts/hardhat.config.ts` 的 `defaultNetwork` 变量，
    2. `packages/vite-app-ts/src/config/providersConfig.ts` 中的 `targetNetworkInfo` 变量
2. 查看可用账户： `yarn account` ，如果没有找到可用账户，则使用 `yarn generate` 生成；
3. 使用 [faucet.paradigm.xyz](https://faucet.paradigm.xyz/) 获取一些测试用的的 ETH，可以使用对应的区块浏览器查看账户情况，比如 [https://rinkeby.etherscan.io/](https://rinkeby.etherscan.io/)，当我们完成测试用币的申请之后，我们可以看到账户余额为 0.1ETH；
4. 再次使用 `yarn deploy` 进行合约部署：

```bash
$ yarn deploy
Nothing to compile
No need to generate any newer typings.
deploying "YourToken" (tx: 0xa7a89a2917cfa355d1305643dc89f54d776186c0059977b0a237737fa37dff62)...: deployed at 0x0F0D10eF3589cE896E9E54E09568cB7a5371e398 with 639137 gas
deploying "Vendor" (tx: 0x3a1f02b77de29704a16599067c8e10abb0da78e547ea0eea8200761da5d45715)...: deployed at 0xb335Fc61D759C041503dC17266575229E593DE17 with 694098 gas

 🏵  Sending all 1000 tokens to the vendor...
```

可以看到，合约部署成功，此时我们可以在线上测试网络查看到具体的合约部署情况：

- GLD 合约地址：[https://rinkeby.etherscan.io/address/0x0F0D10eF3589cE896E9E54E09568cB7a5371e398](https://rinkeby.etherscan.io/address/0x0F0D10eF3589cE896E9E54E09568cB7a5371e398)
- 承销商合约地址： [https://rinkeby.etherscan.io/address/0xb335Fc61D759C041503dC17266575229E593DE17](https://rinkeby.etherscan.io/address/0xb335Fc61D759C041503dC17266575229E593DE17)

并且部署完成了初始化代币分发和所有权转换。详情可以查看部署账户信息： [https://rinkeby.etherscan.io/address/0xccb20d43f62f31dd94436f04a1e90d7d08569e57](https://rinkeby.etherscan.io/address/0xccb20d43f62f31dd94436f04a1e90d7d08569e57)。

## 六、发布

接下来，我们将发布我们的前端项目到 Surge （或者使用 s3， ipfs 上）。Surge.sh 提供了免费的网站的部署，对于我们的测试网站来时再合适不过。

1. 编译前端项目： `yarn build`
2. 将项目发布到 surge 上： `yarn surge`

```bash
$ yarn surge

   Welcome to surge! (surge.sh)
   Login (or create surge account) by entering email & password.

          email: qwh005007@gmail.com
       password: 

   Running as qwh005007@gmail.com (Student)

        project: ./dist
         domain: qiwihui-scaffold-2.surge.sh
         upload: [====================] 100% eta: 0.0s (83 files, 16080214 bytes)
            CDN: [====================] 100%
     encryption: *.surge.sh, surge.sh (57 days)
             IP: 138.197.235.123

   Success! - Published to qiwihui-scaffold-2.surge.sh
```

Surge 在运行命令的过程中就设置了账户名称，以及可以自定义域名：[qiwihui-scaffold-2.surge.sh](http://qiwihui-scaffold-2.surge.sh)，当完成部署之后，我们就可以在浏览器中访问这个页面，和我们本地运行的结果是一致的。

## 七、合约验证

当我们向测试网络部署合约时，部署的是合约编译之后的字节码，合约源码不会发布。实际生产中，有时我们需要发布我们的源代码，以保证我们的代码真实可信。此时，我们就可以借助 etherscan 提供的功能进行验证。

1. 首先，我们获取 etherscan 的 API key，地址为 [https://etherscan.io/myapikey](https://etherscan.io/myapikey)，比如 `PSW8C433Q667DVEX5BCRMGNAH9FSGFZ7Q8` ；
2. 更新 `packages/hardhat-ts/package.json` 中对应的 api-key 参数：
    
    ```json
    ...
        "send": "hardhat send",
        "generate": "hardhat generate",
        "account": "hardhat account",
        "etherscan-verify": "hardhat etherscan-verify --api-key PSW8C433Q667DVEX5BCRMGNAH9FSGFZ7Q8"
      },
    ...
    ```
    
3. 由于项目中的一个 bug，需要在根目录下的 `packages.json` 中添加以下命令才能直接使用之后的命令：
    
    ```json
    "verify": "yarn workspace @scaffold-eth/hardhat etherscan-verify",
    ```
    
4. 运行 `yarn verify --network rinkeby` ，这个命令将通过 etherscan 接口进行合约验证，输出结果为：
    
    ```bash
    $ yarn verify --network rinkeby
    verifying Vendor (0xb335Fc61D759C041503dC17266575229E593DE17) ...
    waiting for result...
     => contract Vendor is now verified
    verifying YourToken (0x0F0D10eF3589cE896E9E54E09568cB7a5371e398) ...
    waiting for result...
     => contract YourToken is now verified
    ```
    
5. 验证完成后，我们可以看到 etherscan 中的合约页面已经加上了一个蓝色小钩，在合约中，也可以看到我们合约的源代码：
    
    ![contractVerified](https://user-images.githubusercontent.com/3297411/155913533-362162f2-eede-47f6-9c97-6f6e34bc9a70.png)
    

至此，我们就完成了合约的验证。 

## 八、提交结果

最后，当我们完成上述的所有步骤之后，我们可以将我们的结果提交到 [speedrunethereum.com](https://speedrunethereum.com/) 上，选择对应的挑战，并提交部署的前端地址和承销商合约的链接即可：

![submitChallenge](https://user-images.githubusercontent.com/3297411/155913539-e7c60b5c-261d-488d-a517-0218bf415aa5.png)

Congratulations! 你已经完成了这个教程

## 总结

通过篇教程，我们可以学习到如下内容：

1. 合约 `approve` 和 `transferFrom` 的使用；
2. 如何使用 OpenZeppelin 创建 ERC20 代币；
3. 创建承销商合约实现用户对代币的买卖；
4. 在测试网路 Rinkeby 上部署合约；
5. 在 [Surge.sh](http://Surge.sh) 上部署前端项目；
6. 在 etherscan 上查看合约以及验证合约；
7. 以及关于 web3 开发的知识，包括 hardhat，react 等。
