# SVG NFT 全面实践 ── scaffold-eth loogies-svg-nft 项目完整指南

> Issue: #153  
> State: open  
> Source: [https://github.com/qiwihui/blog/issues/153](https://github.com/qiwihui/blog/issues/153)

注：这篇文章是我投稿于“李大狗Leeduckgo”公众号的文章，原文地址：[SVG NFT 全面实践 | Web3.0 dApp 开发（六）](https://mp.weixin.qq.com/s/WvTFk3E6FjfHtXfp2uHkrw)。

---

loogies-svg-nft 是 scaffold-eth 提供的一个简单的 NFT 铸造和展示的项目，在本教程中，我们将带领大家一步步分析和实现这个项目。

由于项目的 `loogies-svg-nft` 分支与 `master` 分支在组件库和主页上有一些变化，故先将 `master` 分支代码与 `loogies-svg-nft` 分支进行了合并，解决冲突，得到一份基新组件库的全新的代码。可以参考项目地址： [https://github.com/qiwihui/scaffold-eth.git](https://github.com/qiwihui/scaffold-eth.git) 的 `loogies-svg-nft` 分支。本文以下内容将基于这些代码进行部署和分析。

<!--more-->

## 本地运行和测试

首先我们先运行项目查看我们将要分析实现的功能。

### 本地运行

首先我们在本地运行项目：

clone 项目并切换到 `loogies-svg-nft` 分支：

```bash
git clone https://github.com/qiwihui/scaffold-eth.git loogies-svg-nft
cd loogies-svg-nft
git checkout loogies-svg-nft
```

安装依赖包

```bash
yarn install
```
    
运行前端
    
```bash
yarn start
```
    
在第二个终端窗口中，运行本地测试链
    
```bash
yarn chain
```
    
![yarn-chain](https://user-images.githubusercontent.com/3297411/153822009-3154003e-6433-4a29-a511-b33b5f37a99a.png)
    
在第三个终端窗口中，运行部署合约
    
```bash
yarn deploy
```
    
![yarn-deploy](https://user-images.githubusercontent.com/3297411/153822065-4c4a0ffa-95e3-4e16-8272-ace2f102625b.png)
    
此时在浏览器中访问 [`http://localhost:3000`](http://localhost:3000/) ，就可以看到程序了。

![yarn-start](https://user-images.githubusercontent.com/3297411/153822123-f6f7e3b0-ac6e-4625-a0bd-9bc4170d6aeb.png)

### 本地测试

1. 首先在 MetaMask 钱包中添加本地网络，并切换到本地网络；
    - 网络名称： `Localhost 8545`
    - 新增 RPC URL： `http://localhost:8545`
    - 链 ID： `31337`
    - Currency Symbol： `ETH`
2. 创建一个新的本地钱包账号；
3. 复制钱包地址，在页面左下角给这个地址发送一些测试 ETH；
4. 点击在页面右上角 `connect` 连接钱包；
5. 点击 Mint 铸造；
6. 当交易成功后，可以看到新铸造的 NFT；

	![nft-display](https://user-images.githubusercontent.com/3297411/153822198-6442f4d1-fa49-43e1-bb7c-eacc1b1d082d.png)

下面，我们开始对项目合约进行分析。

## Loogies 合约分析

### NFT 与 ERC721

**NFT**，全称为Non-Fungible Token，指非同质化代币，对应于以太坊上 ERC-721 标准。 一般在智能合约中，NFT 的定义包含 `tokenId` 和 `tokenURI` ，每一个 NFT 的 `tokenId` 是唯一的， `tokenURI` 对于保存了NFT的元数据，可以是图像URL、描述、属性等。如果一个 NFT 想在 NFT 市场上进行展示和销售，则 `tokenURI` 内容需要对应符合 NFT 市场的标准，比如，在 NFT 市场 OpenSea [元数据标准](https://docs.opensea.io/docs/metadata-standards)中，就指出了 NFT 展示需要设置的属性。

![OpenSea 中 NFT 元数据与展示对应关系](https://user-images.githubusercontent.com/3297411/153822292-ac9fa169-199b-49cb-b8bd-4ec3e680842c.png)

OpenSea 中 NFT 元数据与展示对应关系

### 合约概览

[loogies-svg-nft 项目](https://github.com/scaffold-eth/scaffold-eth/tree/loogies-svg-nft)的合约文件在 `packages/hardhat/contracts/` 路径下，包含以下三个文件：

```bash
packages/hardhat/contracts/
├── HexStrings.sol
├── ToColor.sol
└── YourCollectible.sol
```

- `HexString.sol` ：生成地址字符串；
- `ToColor.sol`：生成颜色编码字符串；
- `YourCollectible.sol`： `Loogies` NFT的合约文件，主要功能涉及合约铸造和元数据生成。

合约的主要结构和方法为：

```solidity
contract YourCollectible is ERC721, Ownable {

	// 构造函数
  constructor() public ERC721("Loogies", "LOOG") {
  }
  // 铸造 NFT
  function mintItem()
      public
      returns (uint256)
  {
    ...
  }
	// 获取 tokenId 对应 tokeURI
  function tokenURI(uint256 id) public view override returns (string memory) {
    ...
  }
	// 生成 tokenId 对应 svg 代码
  function generateSVGofTokenById(uint256 id) internal view returns (string memory) {
    ...
  }

	// 生成 tokenId 对应 svg 代码，主要用于绘制图像
  function renderTokenById(uint256 id) public view returns (string memory) {
    ...
  }

}
```

### 构造函数

```solidity
constructor() public ERC721("Loogies", "LOOG") {
    // RELEASE THE LOOGIES!
  }
```

代币符号： `Loogies`

代币名称： `LOOG`

合约继承自 OpenZeppelin 的 `ERC721.sol`，这是 OpenZeppelin 提供的基本合约代码，可以方便开发者使用。

### 应用库函数

合约中分别对 `uint256`， `uint160` 和 `bytes3` 等应用了不同库函数，扩展对应功能：

```solidity
// 使 uint256 具有 toHexString 功能
using Strings for uint256;
// 使 uint160 具有自定义 toHexString 功能
using HexStrings for uint160;
// 使 bytes3 可以方便生成前端颜色表示
using ToColor for bytes3;
// 计数功能
using Counters for Counters.Counter;
```

### Mint 期限

以下代码是 Mint 时间限制：

```solidity
uint256 mintDeadline = block.timestamp + 24 hours;

function mintItem()
      public
      returns (uint256)
  {
      require( block.timestamp < mintDeadline, "DONE MINTING");
...
```

合约在部署之后的24小时内可以铸造，超过24小时则会引发异常。这个机制类似于预售，由于这个合约比较简单，所以没有使用白名单机制，一般在实际情况，会使用预售和白名单的方式来控制 NFT 的发行。

### Mint 铸造

铸造 NFT 其实就是在合约中设置两个信息：

- `tokenId` 及其 `owner`
- `tokenId` 及其 `tokenURI`

我们首先看铸造函数 `mintItem`：

```solidity
// 用于保存每一个铸造的 Loogies 的特征，其中，color 表示颜色，chubbiness 表示胖瘦
mapping (uint256 => bytes3) public color;
mapping (uint256 => uint256) public chubbiness;

...

function mintItem()
      public
      returns (uint256)
  {
      require( block.timestamp < mintDeadline, "DONE MINTING");
			// 每次铸造前自增 _tokenIds，确保 _tokenIds 唯一
      _tokenIds.increment();

      uint256 id = _tokenIds.current();
			// 铸造者与 tokenId 绑定
      _mint(msg.sender, id);
			// 随机生成对应 tokenId 的属性
      bytes32 predictableRandom = keccak256(abi.encodePacked( blockhash(block.number-1), msg.sender, address(this), id ));
      color[id] = bytes2(predictableRandom[0]) | ( bytes2(predictableRandom[1]) >> 8 ) | ( bytes3(predictableRandom[2]) >> 16 );
      chubbiness[id] = 35+((55*uint256(uint8(predictableRandom[3])))/255);

      return id;
  }
```

其中：

- `tokenId` 在每次铸造时会自增，确保 `tokenId` 唯一；
- `_mint` 函数绑定 `tokenId` 及其 `owner`；
- 每一个 `tokenId` 对应的属性通过随机方式生成，具体为：
    - 通过前一个区块的哈希（ `blockhash(block.number-1)` ），当前铸造账户（ `msg.sender`），合约地址（ `address(this)` ）和 `tokenId` 生成哈希 `predictableRandom`；
    - 计算 NFT 颜色：按位或 `predictableRandom` 前三位得到颜色，颜色表示用 bytes3 表示，其中 `bytes2(predictableRandom[0])` 对应最低位蓝色数值， `( bytes2(predictableRandom[1]) >> 8 )`对应中间位绿色数值， `( bytes3(predictableRandom[2]) >> 16 )` 对应最高位红色数值；
    - 计算 NFT 胖瘦： `35+((55*uint256(uint8(predictableRandom[3])))/255);` ，`uint8(predictableRandom[3])`介于0~255，故最小值为35，最大值为 35+55 = 90；

例如： `color` 为 `0x4cc4c1` ， `chubbiness` 为 88 时对应的 NFT 图片为：

![loogies-1](https://user-images.githubusercontent.com/3297411/153822433-3a1a41a4-f846-45f9-b74e-f699ccba6a81.png)

### tokenURI 函数

函数 `tokenURI` 接受 `tokenId` 参数，返回编码之后的元数据字符串：

```solidity
function tokenURI(uint256 id) public view override returns (string memory) {
			// 检查 id 是否存在
      require(_exists(id), "not exist");
      string memory name = string(abi.encodePacked('Loogie #',id.toString()));
      string memory description = string(abi.encodePacked('This Loogie is the color #',color[id].toColor(),' with a chubbiness of ',uint2str(chubbiness[id]),'!!!'));
      // 生成图片的svg base64 编码
			string memory image = Base64.encode(bytes(generateSVGofTokenById(id)));

      return
          string(
              abi.encodePacked(
                'data:application/json;base64,',
								// 通过 base64 编码元数据
                Base64.encode(
                    bytes(
                          abi.encodePacked(
                              '{"name":"',
                              name,
                              '", "description":"',
                              description,
                              '", "external_url":"https://burnyboys.com/token/',
                              id.toString(),
                              '", "attributes": [{"trait_type": "color", "value": "#',
                              color[id].toColor(),
                              '"},{"trait_type": "chubbiness", "value": ',
                              uint2str(chubbiness[id]),
                              '}], "owner":"',
                              (uint160(ownerOf(id))).toHexString(20),
                              '", "image": "',
                              'data:image/svg+xml;base64,',
                              image,
                              '"}'
                          )
                        )
                    )
              )
          );
  }
// 生成的 SVG 字符串
function generateSVGofTokenById(uint256 id) internal view returns (string memory) {
...
}

// 绘制图像
// Visibility is `public` to enable it being called by other contracts for composition.
function renderTokenById(uint256 id) public view returns (string memory) {
...
}
```

其中， `generateSVGofTokenById` 函数返回 `tokenId` 对应的颜色和胖瘦属性生成的 SVG 字符串， `renderTokenById` 用户绘制图像。

我们可以看到，NFT 元数据中包含的属性有：

- name：名称
- description： 描述
- external_url：外部链接
- attributes：属性
    - color 颜色
    - chubbiness：胖瘦
    - owner：所有者，以太坊地址16进制形式
    - image：图片对应 SVG 的 base64 编码

这里，我们通过实际数据了解一下什么是 SVG。`tokenId` 为 1 时对应的 `tokenURI` 结果为：

```bash
data:application/json;base64,eyJuYW1lIjoiTG9vZ2llICMxIiwiZGVzY3JpcHRpb24iOiJUaGlzIExvb2dpZSBpcyB0aGUgY29sb3IgIzRjYzRjMSB3aXRoIGEgY2h1YmJpbmVzcyBvZiA4OCEhISIsImV4dGVybmFsX3VybCI6Imh0dHBzOi8vYnVybnlib3lzLmNvbS90b2tlbi8xIiwiYXR0cmlidXRlcyI6W3sidHJhaXRfdHlwZSI6ImNvbG9yIiwidmFsdWUiOiIjNGNjNGMxIn0seyJ0cmFpdF90eXBlIjoiY2h1YmJpbmVzcyIsInZhbHVlIjo4OH1dLCJvd25lciI6IjB4MTY5ODQxYWEzMDI0Y2ZhNTcwMDI0ZWI3ZGQ2YmY1Zjc3NDA5MjA4OCIsImltYWdlIjoiZGF0YTppbWFnZS9zdmcreG1sO2Jhc2U2NCxQSE4yWnlCM2FXUjBhRDBpTkRBd0lpQm9aV2xuYUhROUlqUXdNQ0lnZUcxc2JuTTlJbWgwZEhBNkx5OTNkM2N1ZHpNdWIzSm5Mekl3TURBdmMzWm5JajQ4WnlCcFpEMGlaWGxsTVNJK1BHVnNiR2x3YzJVZ2MzUnliMnRsTFhkcFpIUm9QU0l6SWlCeWVUMGlNamt1TlNJZ2NuZzlJakk1TGpVaUlHbGtQU0p6ZG1kZk1TSWdZM2s5SWpFMU5DNDFJaUJqZUQwaU1UZ3hMalVpSUhOMGNtOXJaVDBpSXpBd01DSWdabWxzYkQwaUkyWm1aaUl2UGp4bGJHeHBjSE5sSUhKNVBTSXpMalVpSUhKNFBTSXlMalVpSUdsa1BTSnpkbWRmTXlJZ1kzazlJakUxTkM0MUlpQmplRDBpTVRjekxqVWlJSE4wY205clpTMTNhV1IwYUQwaU15SWdjM1J5YjJ0bFBTSWpNREF3SWlCbWFXeHNQU0lqTURBd01EQXdJaTgrUEM5blBqeG5JR2xrUFNKb1pXRmtJajQ4Wld4c2FYQnpaU0JtYVd4c1BTSWpOR05qTkdNeElpQnpkSEp2YTJVdGQybGtkR2c5SWpNaUlHTjRQU0l5TURRdU5TSWdZM2s5SWpJeE1TNDRNREEyTlNJZ2FXUTlJbk4yWjE4MUlpQnllRDBpT0RnaUlISjVQU0kxTVM0NE1EQTJOU0lnYzNSeWIydGxQU0lqTURBd0lpOCtQQzluUGp4bklHbGtQU0psZVdVeUlqNDhaV3hzYVhCelpTQnpkSEp2YTJVdGQybGtkR2c5SWpNaUlISjVQU0l5T1M0MUlpQnllRDBpTWprdU5TSWdhV1E5SW5OMloxOHlJaUJqZVQwaU1UWTRMalVpSUdONFBTSXlNRGt1TlNJZ2MzUnliMnRsUFNJak1EQXdJaUJtYVd4c1BTSWpabVptSWk4K1BHVnNiR2x3YzJVZ2NuazlJak11TlNJZ2NuZzlJak1pSUdsa1BTSnpkbWRmTkNJZ1kzazlJakUyT1M0MUlpQmplRDBpTWpBNElpQnpkSEp2YTJVdGQybGtkR2c5SWpNaUlHWnBiR3c5SWlNd01EQXdNREFpSUhOMGNtOXJaVDBpSXpBd01DSXZQand2Wno0OEwzTjJaejQ9In0=
```

通过 base64 解码 `data:application/json;base64,` 之后的字符串可以得到如下 json（以下 json 经过了格式化，方便阅读）：

```json
{
  "name": "Loogie #1",
  "description": "This Loogie is the color #4cc4c1 with a chubbiness of 88!!!",
  "external_url": "https://burnyboys.com/token/1",
  "attributes": [
    {
      "trait_type": "color",
      "value": "#4cc4c1"
    },
    {
      "trait_type": "chubbiness",
      "value": 88
    }
  ],
  "owner": "0x169841aa3024cfa570024eb7dd6bf5f774092088",
  "image": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBpZD0iZXllMSI+PGVsbGlwc2Ugc3Ryb2tlLXdpZHRoPSIzIiByeT0iMjkuNSIgcng9IjI5LjUiIGlkPSJzdmdfMSIgY3k9IjE1NC41IiBjeD0iMTgxLjUiIHN0cm9rZT0iIzAwMCIgZmlsbD0iI2ZmZiIvPjxlbGxpcHNlIHJ5PSIzLjUiIHJ4PSIyLjUiIGlkPSJzdmdfMyIgY3k9IjE1NC41IiBjeD0iMTczLjUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlPSIjMDAwIiBmaWxsPSIjMDAwMDAwIi8+PC9nPjxnIGlkPSJoZWFkIj48ZWxsaXBzZSBmaWxsPSIjNGNjNGMxIiBzdHJva2Utd2lkdGg9IjMiIGN4PSIyMDQuNSIgY3k9IjIxMS44MDA2NSIgaWQ9InN2Z181IiByeD0iODgiIHJ5PSI1MS44MDA2NSIgc3Ryb2tlPSIjMDAwIi8+PC9nPjxnIGlkPSJleWUyIj48ZWxsaXBzZSBzdHJva2Utd2lkdGg9IjMiIHJ5PSIyOS41IiByeD0iMjkuNSIgaWQ9InN2Z18yIiBjeT0iMTY4LjUiIGN4PSIyMDkuNSIgc3Ryb2tlPSIjMDAwIiBmaWxsPSIjZmZmIi8+PGVsbGlwc2Ugcnk9IjMuNSIgcng9IjMiIGlkPSJzdmdfNCIgY3k9IjE2OS41IiBjeD0iMjA4IiBzdHJva2Utd2lkdGg9IjMiIGZpbGw9IiMwMDAwMDAiIHN0cm9rZT0iIzAwMCIvPjwvZz48L3N2Zz4="
}
```

我们对 `image` 字段进行解码并格式化就得到图片的 SVG：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
   <g id="eye1">
      <ellipse stroke-width="3" ry="29.5" rx="29.5" id="svg_1" cy="154.5" cx="181.5" stroke="#000" fill="#fff" />
      <ellipse ry="3.5" rx="2.5" id="svg_3" cy="154.5" cx="173.5" stroke-width="3" stroke="#000" fill="#000000" />
   </g>
   <g id="head">
      <ellipse fill="#4cc4c1" stroke-width="3" cx="204.5" cy="211.80065" id="svg_5" rx="88" ry="51.80065" stroke="#000" />
   </g>
   <g id="eye2">
      <ellipse stroke-width="3" ry="29.5" rx="29.5" id="svg_2" cy="168.5" cx="209.5" stroke="#000" fill="#fff" />
      <ellipse ry="3.5" rx="3" id="svg_4" cy="169.5" cx="208" stroke-width="3" fill="#000000" stroke="#000" />
   </g>
</svg>
```

SVG是一种用 XML 定义的语言，用来描述二维矢量及矢量/栅格图形。它可以任意放大图形显示，也不会牺牲图像质量，它可以使用代码进行描述，方便编辑，因此被广泛使用。

从上面的代码结合以下的图像可以看出，这个 SVG 包含如下内容：

- 第一行为 XML 声明，标明版本和编码类型，之后是SVG 的宽度和高度；
- `eye1`：由两个椭圆（ellipse）绘制的眼圈和黑色眼珠；
- `head`：填充 `#4cc4c1` 颜色的椭圆作为身体；
- `eye2`：与 `eye1` 一致，位置不同；

`eye1`，`head`和`eye2`依次叠加得到最终的图形：

![loogies-1](https://user-images.githubusercontent.com/3297411/153822497-6cdd7677-9594-4e78-8bc1-8f1b4c1158b8.png)

### 辅助函数解析

1. `uint2str` 将 `uint` 转变为字符串，例如 `123` 变为 `'123'`

```solidity
function uint2str(uint _i) internal pure returns (string memory _uintAsString) {
      if (_i == 0) {
          return "0";
      }
      uint j = _i;
			// uint 位数
      uint len;
      while (j != 0) {
          len++;
          j /= 10;
      }
      bytes memory bstr = new bytes(len);
      uint k = len;
      while (_i != 0) {
          k = k-1;
			    // _i 个位数字
          uint8 temp = (48 + uint8(_i - _i / 10 * 10));
          bytes1 b1 = bytes1(temp);
          bstr[k] = b1;
          _i /= 10;
      }
      return string(bstr);
  }
```

1.  `ToColor.sol` 库：将 `byte3` 类型转换为前端颜色字符串，例如：输入 `0x4cc4c1` 输出 `'4cc4c1'`

```solidity
library ToColor {
    bytes16 internal constant ALPHABET = '0123456789abcdef';

    function toColor(bytes3 value) internal pure returns (string memory) {
      bytes memory buffer = new bytes(6);
      for (uint256 i = 0; i < 3; i++) {
          buffer[i*2+1] = ALPHABET[uint8(value[i]) & 0xf];
          buffer[i*2] = ALPHABET[uint8(value[i]>>4) & 0xf];
      }
      return string(buffer);
    }
}
```

1.  `HexStrings.sol` 库：主要作用是将 `uint` 按 `length` 位提取，对应于生成公钥时截取前20位的功能： `(*uint160*(ownerOf(id))).toHexString(20)`，此表达式生成对应 `tokenId` 所有者的地址。

```solidity
library HexStrings {
    bytes16 internal constant ALPHABET = '0123456789abcdef';

    function toHexString(uint256 value, uint256 length) internal pure returns (string memory) {
        bytes memory buffer = new bytes(2 * length + 2);
        buffer[0] = '0';
        buffer[1] = 'x';
        for (uint256 i = 2 * length + 1; i > 1; --i) {
            buffer[i] = ALPHABET[value & 0xf];
            value >>= 4;
        }
        return string(buffer);
    }
}
```

至此，合约源码分析完成。

下面我们将对前端的逻辑进行简要分析，然后我们将一步步实现 NFT 铸造和展示的功能。将代码切换到前端代码提交之前，按照以下的步骤一步步添加功能。

```bash
git checkout a98156f6a03a0bc8fc98c8c77cef6fbf59f03b31
```

## 前端逻辑分析

项目前端文件在 `packages/react-app` 内，以下文章中涉及文件的位置都将在这个文件中寻找。

我们首先来看一下 `src/App.jsx` ，这是项目的主要页面，我们可以利用代码编辑器查看这个文件的主要部分：

![Appjsx](https://user-images.githubusercontent.com/3297411/153822564-f2f96aa8-1336-475b-adc8-cc251405cdff.png)

其中包含的功能和组件包括：

- `Header`：标题栏，显示标题
- *`NetworkDisplay`：所处网络状态*
- *`Menu`， `Switch`：菜单切换*
- *`ThemeSwitch`：右下角明暗主题切换*
- *`Account`：右上角账户信息组件*
- 接下来的两个 `Row` 对应左下角的 Gas 显示、支持和本地的水龙头

下面我们主要看一下 *`NetworkDisplay`和 `Account` 的逻辑实现，以及 `Menu`， `Switch` 中的功能。*

### *`NetworkDisplay`*

组件位置： `src/components/NetworkDisplay.jsx`

主要包含两个功能：

1. 显示当前所选择的网络名称；
2. 如果当前钱包所在网络与项目中网络设置不一致，则提示警告，其中，当选择本地网络是，网络 ID 需要设置为 `31337` 。

```jsx
function NetworkDisplay({
  NETWORKCHECK,
  localChainId,
  selectedChainId,
  targetNetwork,
  USE_NETWORK_SELECTOR,
  logoutOfWeb3Modal,
}) {
  let networkDisplay = "";
  if (NETWORKCHECK && localChainId && selectedChainId && localChainId !== selectedChainId) {
    const networkSelected = NETWORK(selectedChainId);
    const networkLocal = NETWORK(localChainId);
    if (selectedChainId === 1337 && localChainId === 31337) {
			// 提示错误的网络ID
			...
    } else {
			// 提示网络错误
			...
    }
  } else {
    networkDisplay = USE_NETWORK_SELECTOR ? null : (
      // 显示网络名称
      <div style={{ zIndex: -1, position: "absolute", right: 154, top: 28, padding: 16, color: targetNetwork.color }}>
        {targetNetwork.name}
      </div>
    );
  }

  console.log({ networkDisplay });

  return networkDisplay;
}
```

### *`Account`*

组件位置： `src/components/Account.jsx`

主要包含两个功能：

1. 显示当前钱包
2. 显示钱包余额
3. 显示 `Connect` 或者 `Logout`

其中，当用户点击 `Connect` 时，前端调用 *`loadWeb3Modal`，代码如下，这个函数的需要功能是与MetaMask等钱包进行连接，并监听钱包的*  `chainChanged`，`accountsChanged` 和 `disconnect` 事件，即当我们在钱包中切换网络，选择连接账户以及取消连接时对应修改显示状态。

```jsx
  const loadWeb3Modal = useCallback(async () => {
		// 连接钱包
    const provider = await web3Modal.connect();
    setInjectedProvider(new ethers.providers.Web3Provider(provider));
		// 监听切换网络
    provider.on("chainChanged", chainId => {
      console.log(`chain changed to ${chainId}! updating providers`);
      setInjectedProvider(new ethers.providers.Web3Provider(provider));
    });
    // 监听切换账户
    provider.on("accountsChanged", () => {
      console.log(`account changed!`);
      setInjectedProvider(new ethers.providers.Web3Provider(provider));
    });
		// 监听断开连接
    // Subscribe to session disconnection
    provider.on("disconnect", (code, reason) => {
      console.log(code, reason);
      logoutOfWeb3Modal();
    });
    // eslint-disable-next-line
  }, [setInjectedProvider]);
```

同理，在连接钱包情况下，用户点击 `Logout` 会调用 `logoutOfWeb3Modal` 功能，

```jsx
const logoutOfWeb3Modal = async () => {
		// 清楚缓存的网络提供商，并断开连接
    await web3Modal.clearCachedProvider();
    if (injectedProvider && injectedProvider.provider && typeof injectedProvider.provider.disconnect == "function") {
      await injectedProvider.provider.disconnect();
    }
    setTimeout(() => {
      window.location.reload();
    }, 1);
  };
```

### *`Menu`， `Switch`*

这两个分别对应显示菜单和对应切换菜单功能，这些菜单包括：

- `App Home` ：项目希望我们将需要实现的功能放在这个菜单中，比如我们将要实现的 NFT 的铸造和展示功能；
- `Debug Contracts`：调试自己编写的合约功能，将会根据合约的 ABI 文件 展示可以合约的状态变量和可以调用的函数；
- `Hints`：编程提示
- `ExampleUI`：示例UI，可以做为编程使用
- `Mainnet DAI`：以太坊主网 `DAI` 的合约状态和可用函数，与 `Debug Contracts` 功能一直
- `Subgraph`：使用 The Graph 协议对合约中的事件进行监听和查询。

### 调试信息

`App.jsx` 中还包含了打印当前页面状态的调试信息，可以在开发的过程中实时查看当前状态变量。

```jsx
  //
  // 🧫 DEBUG 👨🏻‍🔬
  //
  useEffect(() => {
    if (
      DEBUG &&
      mainnetProvider &&
      address &&
      selectedChainId &&
      yourLocalBalance &&
      yourMainnetBalance &&
      readContracts &&
      writeContracts &&
      mainnetContracts
    ) {
      console.log("_____________________________________ 🏗 scaffold-eth _____________________________________");
      console.log("🌎 mainnetProvider", mainnetProvider);
      console.log("🏠 localChainId", localChainId);
      console.log("👩‍💼 selected address:", address);
      console.log("🕵🏻‍♂️ selectedChainId:", selectedChainId);
      console.log("💵 yourLocalBalance", yourLocalBalance ? ethers.utils.formatEther(yourLocalBalance) : "...");
      console.log("💵 yourMainnetBalance", yourMainnetBalance ? ethers.utils.formatEther(yourMainnetBalance) : "...");
      console.log("📝 readContracts", readContracts);
      console.log("🌍 DAI contract on mainnet:", mainnetContracts);
      console.log("💵 yourMainnetDAIBalance", myMainnetDAIBalance);
      console.log("🔐 writeContracts", writeContracts);
    }
  }, [
    mainnetProvider,
    address,
    selectedChainId,
    yourLocalBalance,
    yourMainnetBalance,
    readContracts,
    writeContracts,
    mainnetContracts,
    localChainId,
    myMainnetDAIBalance,
  ]);
```

查看完主页的基本功能，下面我们开始实现 NFT 铸造和展示 NFT 列表这两个功能。

## NFT 功能实现

我们将主要实现以下三个部分功能：

- 铸造 NFT；
- 展示 NFT 列表；
- 展示 NFT 合约接口列表。

### 铸造 NFT

首先我们找到 `App Home` 对应使用的组件，从下面的代码中可以看到，对应使用 `Home` 组件，所在位置为 `src/views/Home.jsx` 。

```jsx
    ...
    <Switch>
        <Route exact path="/">
          {/* pass in any web3 props to this Home component. For example, yourLocalBalance */}
          <Home yourLocalBalance={yourLocalBalance} readContracts={readContracts} />
        </Route>
    ....
```

删除 `Home.jsx` 中内容，添加以下 Mint 按钮：

```jsx
import React, { useState } from "react";
import { Button, Card, List } from "antd";

function Home({ 
  isSigner,
  loadWeb3Modal,
  tx,
  writeContracts,
}) {

  return (
    <div>
      {/* Mint button */}
      <div style={{ maxWidth: 820, margin: "auto", marginTop: 32, paddingBottom: 32 }}>
        {isSigner?(
          <Button type={"primary"} onClick={()=>{
            tx( writeContracts.YourCollectible.mintItem() )
          }}>MINT</Button>
        ):(
          <Button type={"primary"} onClick={loadWeb3Modal}>CONNECT WALLET</Button>
        )}
      </div>
    </div>
  );
}

export default Home;
```

同时将 `Switch` 中对应组件使用修改为：

```jsx
      ...
      <Switch>
        <Route exact path="/">
          {/* pass in any web3 props to this Home component. For example, yourLocalBalance */}
          <Home
            isSigner={userSigner}
            loadWeb3Modal={loadWeb3Modal}
            tx={tx}
            writeContracts={writeContracts}
          />
       ...
```

效果图为：

![mint-button](https://user-images.githubusercontent.com/3297411/153822638-2ce70ded-289b-411e-9ed5-c78507617427.png)

点击 Mint 之后，我们可以看到交易成功发出，这时，虽然我们成功 mint 了 NFT，但是我们还需要添加列表来展示我们的 NFT。

### 展示 NFT 列表

添加列表展示，其中包含 NFT 的转移功能可以将对应的 NFT 发送给其他地址。

```jsx
import React, { useState } from "react";
import { Button, Card, List } from "antd";
import { useContractReader } from "eth-hooks";
import { Address, AddressInput} from "../components";

function Home({ 
  isSigner,
  loadWeb3Modal,
  yourCollectibles,
  address,
  blockExplorer,
  mainnetProvider,
  tx,
  readContracts,
  writeContracts,
}) {
  const [transferToAddresses, setTransferToAddresses] = useState({});

  return (
    <div>
      {/* Mint 按钮 */}
			...
			{/* 列表 */}
      <div style={{ width: 820, margin: "auto", paddingBottom: 256 }}>
        <List
          bordered
          dataSource={yourCollectibles}
          renderItem={item => {
            const id = item.id.toNumber();
            console.log("IMAGE",item.image)
            return (
              <List.Item key={id + "_" + item.uri + "_" + item.owner}>
                <Card
                  title={
                    <div>
                      <span style={{ fontSize: 18, marginRight: 8 }}>{item.name}</span>
                    </div>
                  }
                >
                  <a href={"https://opensea.io/assets/"+(readContracts && readContracts.YourCollectible && readContracts.YourCollectible.address)+"/"+item.id} target="_blank">
                  <img src={item.image} />
                  </a>
                  <div>{item.description}</div>
                </Card>
								{/* NFT 转移 */}
                <div>
                  owner:{" "}
                  <Address
                    address={item.owner}
                    ensProvider={mainnetProvider}
                    blockExplorer={blockExplorer}
                    fontSize={16}
                  />
                  <AddressInput
                    ensProvider={mainnetProvider}
                    placeholder="transfer to address"
                    value={transferToAddresses[id]}
                    onChange={newValue => {
                      const update = {};
                      update[id] = newValue;
                      setTransferToAddresses({ ...transferToAddresses, ...update });
                    }}
                  />
                  <Button
                    onClick={() => {
                      console.log("writeContracts", writeContracts);
                      tx(writeContracts.YourCollectible.transferFrom(address, transferToAddresses[id], id));
                    }}
                  >
                    Transfer
                  </Button>
                </div>
              </List.Item>
            );
          }}
        />
      </div>
      {/* 信息提示 */}
      <div style={{ maxWidth: 820, margin: "auto", marginTop: 32, paddingBottom: 256 }}>
        🛠 built with <a href="https://github.com/austintgriffith/scaffold-eth" target="_blank">🏗 scaffold-eth</a>
        🍴 <a href="https://github.com/austintgriffith/scaffold-eth" target="_blank">Fork this repo</a> and build a cool SVG NFT!
      </div>
    </div>
  );
}

export default Home;
```

对应组件使用修改为：

```jsx
      ...
      <Switch>
        <Route exact path="/">
          {/* pass in any web3 props to this Home component. For example, yourLocalBalance */}
          <Home
            isSigner={userSigner}
            loadWeb3Modal={loadWeb3Modal}
            yourCollectibles={yourCollectibles}
            address={address}
            blockExplorer={blockExplorer}
            mainnetProvider={mainnetProvider}
            tx={tx}
            writeContracts={writeContracts}
            readContracts={readContracts}
          />
       ...
```

效果图为：

![nft-display-list](https://user-images.githubusercontent.com/3297411/153822686-e7f7c3c7-65ee-4b1c-ade2-204c6365177f.png)

但是我们发现，当我们再次 mint 时，列表并不会更新，还是原来的样子，因此我们需要在 `App.jsx` 中添加事件监听，一旦我们铸造 NFT 之后，列表将刷新：

```jsx
  // 跟踪当前 NFT 数量
  const balance = useContractReader(readContracts, "YourCollectible", "balanceOf", [address]);
  console.log("🤗 balance:", balance);

  const yourBalance = balance && balance.toNumber && balance.toNumber();
  const [yourCollectibles, setYourCollectibles] = useState();
  //
  // 🧠 这个 effect 会在 balance 变化时更新 yourCollectibles 
  //
  useEffect(() => {
    const updateYourCollectibles = async () => {
      const collectibleUpdate = [];
      for (let tokenIndex = 0; tokenIndex < balance; tokenIndex++) {
        try {
          console.log("GEtting token index", tokenIndex);
          const tokenId = await readContracts.YourCollectible.tokenOfOwnerByIndex(address, tokenIndex);
          console.log("tokenId", tokenId);
          const tokenURI = await readContracts.YourCollectible.tokenURI(tokenId);
          const jsonManifestString = atob(tokenURI.substring(29))
          console.log("jsonManifestString", jsonManifestString);

          try {
            const jsonManifest = JSON.parse(jsonManifestString);
            console.log("jsonManifest", jsonManifest);
            collectibleUpdate.push({ id: tokenId, uri: tokenURI, owner: address, ...jsonManifest });
          } catch (e) {
            console.log(e);
          }

        } catch (e) {
          console.log(e);
        }
      }
      setYourCollectibles(collectibleUpdate.reverse());
    };
    updateYourCollectibles();
  }, [address, yourBalance]);
```

此时，当我们再次 Mint 时，就是自动更新列表，显示最新铸造的 NFT 了。

### 展示 NFT 合约接口列表

这个功能比较简单，只需要修改对应 debug 部分即可：

```jsx
      <Route exact path="/debug">
          {/*
                🎛 this scaffolding is full of commonly used components
                this <Contract/> component will automatically parse your ABI
                and give you a form to interact with it locally
            */}

          <Contract
            name="YourCollectible"
            price={price}
            signer={userSigner}
            provider={localProvider}
            address={address}
            blockExplorer={blockExplorer}
            contractConfig={contractConfig}
          />
```

更新之后，可以在 `Debug Contracts` 菜单下看到合约的可以调用的函数。

![contract-funcs](https://user-images.githubusercontent.com/3297411/153822741-30c8d3c6-077b-49b9-8b88-bc62119215cf.png)

至此，我们就完成了一个简单 NFT 铸造和展示的 DApp 了。

## 总结

通过这个项目，我们可以学习并了解以下知识：

1. NFT 合约基本内容以及如何在 Opensea 等市场中展示 NFT；
2. 前端如何连接诸如 MetaMask 等钱包；
3. 前端如何调用合约函数。

