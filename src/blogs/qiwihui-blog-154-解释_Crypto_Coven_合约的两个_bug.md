# 解释 Crypto Coven 合约的两个 bug


Crypto Coven 合约作者在他的文章 [Crypto Coven Contract Bugs: An Arcanist’s Addendum](https://cryptocoven.mirror.xyz/0eZ0tjudMU0ByeXLlRtPzDqxGzMMZw6ldzf-HfYETW0) 中描述了合约中的两个 bug，这篇文章我们来看看这两个bug。这两个 bug 并不会影响女巫 NFT 的所有权。

<!--more-->

## Bug 1：总共可铸造女巫的数量

在合约中有一个修改器 `canMintWitches()` 用来检查地址是否能够在公开发售阶段铸造更多的 NFT：

```solidity
uint256 public maxWitches; // 初始化为 9,999
uint256 public maxGiftedWitches; // 初始化为 250

modifier canMintWitches(uint256 numberOfTokens) {
    require(
        tokenCounter.current() + numberOfTokens <=
            maxWitches - maxGiftedWitches,
        "Not enough witches remaining to mint"
    );
    _;
}
```

这里面的 bug 只会在特定的条件下触发。问题在于应该有 9749 个女巫在公开函数中铸造，250个在 owner-only 函数中铸造，共计9999个。这个逻辑在公开发售阶段如果没有女巫被赠送，则完全正常。然而，项目方在这期间铸造并赠送了女巫，这意味着在上面的条件检查中，右边的总数应该也要变化才正确。铸造赠送越多，相应能允许的 `tokenId` 越高。

在公开发售结束的时候，有93个女巫被赠送，这意味着 `tokenCounter.current()` 到达 9749 使得公开发售结束时，总共只有 9656 个女巫被铸造。

`canGiftWitches()` 函数的作用是为了限制可以赠送的女巫数量最大为 250，所以我们不能通过以下的方式规避：

```solidity
uint256 public maxWitches; // 初始化为 9,999
uint256 public maxGiftedWitches; // 初始化为 250
uint256 private numGiftedWitches;

modifier canGiftWitches(uint256 num) {
    require(
        numGiftedWitches + num <= maxGiftedWitches,
        "Not enough witches remaining to gift"
    );
    require(
        tokenCounter.current() + num <= maxWitches,
        "Not enough witches remaining to mint"
    );
    _;
}
```

结果是，有93个女巫永久消失，合约总共铸造了9906个女巫。

### 修复方法

我们可以通过 `numGiftedWitches` 记录已经赠送的女巫数量来修正。

```solidity
uint256 public maxWitches; // 初始化为 9,999
uint256 public maxGiftedWitches; // 初始化为 250
uint256 private numGiftedWitches;

modifier canMintWitches(uint256 numberOfTokens) {
    require(
        tokenCounter.current() + numberOfTokens <=
            maxWitches - maxGiftedWitches + numGiftedWitches,
        "Not enough witches remaining to mint"
    );
    _;
}
```

## Bug 2：版税

Crypto Coven 认为拥有链上版税很重要，而不仅仅是使用特定于平台的链下实现，这就使得他们使用了 [EIP-2981](https://eips.ethereum.org/EIPS/eip-2981)。 支持该标准的代码很简单：

```solidity
function royaltyInfo(uint256 tokenId, uint256 salePrice)
    external
    view
    override
    returns (address receiver, uint256 royaltyAmount)
{
    require(_exists(tokenId), "Nonexistent token");

    return (address(this), SafeMath.div(SafeMath.mul(salePrice, 5), 100));
}
```

它是如何工作的呢？ 市场调用该函数来读取接收方地址和版税金额的数据，然后相应地发送版税。 在上述例子中，接收方是合约地址，版税金额是 5%。然而，从 Solifidy 0.6.x 开始，合约必需要实现 `receive()` 方法才能接收以太，而女巫合约没有实现。并且，合约的测试在检查 `royaltyInfo()` 函数时，检查了是否返回正确的值，但是没有测试接收版税，所以如果市场尝试发送版税给合约会引起 `revert` 。

幸运的是，在这种情况下，补救措施非常简单，这要归功于 [Royalty Registry](https://royaltyregistry.xyz/)。 项目方配置了一个覆盖指向不同的接收者 `receiver` 地址（在本例中，是他们的多重签名钱包），所以现在从 Royalty Registry 读取的市场将使用覆盖后的值。

### 修复方法

修复此错误以支持 EIP-2981 的最简单方法是简单地返回接收提款的所有者地址，而不是合约地址。 另一种选择是添加一个 `royalReceiverAddress` 变量和一个 `setter` 函数来配置这个值。

如果确实想将以太接收到合约地址，你需要做的就是在合约中添加一个 `receive()` 函数：

```solidity
receive() external payable {}
```

## 总结

学习在 Solidity 中进行开发可能是一场考验——无论是小错误还是大错误，都会永远存在于区块链上，而且通常要付出巨大的代价。 但是，这僵化、无情的空间却有它自己的魅力，在约束中诞生的创造力，通过共同的不眠之夜形成的团结。 对于任何在荒野中闯出自己道路的初出茅庐的奥术师：我希望这里所提供的知识能够进一步照亮这条道路。

[View on GitHub](https://github.com/qiwihui/blog/issues/154)


