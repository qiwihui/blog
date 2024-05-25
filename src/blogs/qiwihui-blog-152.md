---
title: "Crypto Coven 加密女巫 NFT 合约解读"
description: "Crypto Coven 加密女巫 NFT 合约解读"
tags: 
- 区块链
top: 152
date: 27/01/2022, 11:24:44
author: qiwihui
update: 27/01/2022, 11:28:13
categories: 技术
---

本文主要是对 [@mannynotfound](https://twitter.com/mannynotfound) 的推文 [https://twitter.com/mannynotfound/status/1470535464922845187](https://twitter.com/mannynotfound/status/1470535464922845187) 的整理和补充。

加密女巫的合约代码堪称艺术品。代码出自工程师 Matthew Di Ferrante([@matthewdif](https://twitter.com/matthewdif))，涉及 gas 优化，修改器以及 Opensea 预授权等诸多优化措施，对于学习 NFT 合约是个很好的参考材料。

### 基本情况

名称；Crypto Coven

符号： WITCH

合约地址：0x5180db8f5c931aae63c74266b211f580155ecac8

合约代码地址：[https://etherscan.io/address/0x5180db8f5c931aae63c74266b211f580155ecac8#code](https://etherscan.io/address/0x5180db8f5c931aae63c74266b211f580155ecac8#code)

Solidity版本： `^0.8.0`

<!--more-->

### Banner

这个 banner 可以体会到项目方想要做的不是像 Crypto Punks 或者其他像素风格 NFT 一样的作品。

```solidity
/*
.・。.・゜✭・.・✫・゜・。..・。.・゜✭・.・✫・゜・。.✭・.・✫・゜・。..・✫・゜・。.・。.・゜✭・.・✫・゜・。..・。.・゜✭・.・✫・゜・。.✭・.・✫・゜・。..・✫・゜・。

                                                       s                                            _                                 
                         ..                           :8                                           u                                  
             .u    .    @L           .d``            .88           u.                       u.    88Nu.   u.                u.    u.  
      .    .d88B :@8c  9888i   .dL   @8Ne.   .u     :888ooo  ...ue888b           .    ...ue888b  '88888.o888c      .u     x@88k u@88c.
 .udR88N  ="8888f8888r `Y888k:*888.  %8888:u@88N  -*8888888  888R Y888r     .udR88N   888R Y888r  ^8888  8888   ud8888.  ^"8888""8888"
<888'888k   4888>'88"    888E  888I   `888I  888.   8888     888R I888>    <888'888k  888R I888>   8888  8888 :888'8888.   8888  888R 
9888 'Y"    4888> '      888E  888I    888I  888I   8888     888R I888>    9888 'Y"   888R I888>   8888  8888 d888 '88%"   8888  888R 
9888        4888>        888E  888I    888I  888I   8888     888R I888>    9888       888R I888>   8888  8888 8888.+"      8888  888R 
9888       .d888L .+     888E  888I  uW888L  888'  .8888Lu= u8888cJ888     9888      u8888cJ888   .8888b.888P 8888L        8888  888R 
?8888u../  ^"8888*"     x888N><888' '*88888Nu88P   ^%888*    "*888*P"      ?8888u../  "*888*P"     ^Y8888*""  '8888c. .+  "*88*" 8888"
 "8888P'      "Y"        "88"  888  ~ '88888F`       'Y"       'Y"          "8888P'     'Y"          `Y"       "88888%      ""   'Y"  
   "P'                         88F     888 ^                                  "P'                                "YP'                 
                              98"      *8E                                                                                            
                            ./"        '8>                                                                                            
                           ~`           "                                                                                             

.・。.・゜✭・.・✫・゜・。..・。.・゜✭・.・✫・゜・。.✭・.・✫・゜・。..・✫・゜・。.・。.・゜✭・.・✫・゜・。..・。.・゜✭・.・✫・゜・。.✭・.・✫・゜・。..・✫・゜・。
*/
```

### 避免使用 ERC721Enumerable

使用 `ERC721Enumerable` 会带来大量 gas 消耗，合约中使用 `ERC721 + Counters` 的方式节省 Gas。主要原因是由于 `totalSupply()` 函数的使用。

详细可以阅读文章：[Cut Minting Gas Costs By Up To 70% With One Smart Contract Tweak](https://shiny.mirror.xyz/OUampBbIz9ebEicfGnQf5At_ReMHlZy0tB4glb9xQ0E)

```solidity
contract CryptoCoven is ERC721, IERC2981, Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    using Strings for uint256;

    Counters.Counter private tokenCounter;
```

### 修改器让代码更简洁和清晰

合约中使用修改器对权限进行控制，其中包括：

- `publicSaleActive` 公开销售状态
- `communitySaleActive` 社区销售状态
- `maxWitchesPerWallet` 每个钱包最大 token 数量
- `canMintWitches` 控制token总数量
- `canGiftWitches`
- `isCorrectPayment` 判断购买时价格是否正确
- `isValidMerkleProof` 用于白名单机制中的 Merkle 验证

这些修改器可以使得权限控制更简便，代码的可读性也大大提升。

```solidity
// ============ ACCESS CONTROL/SANITY MODIFIERS ============

    modifier publicSaleActive() {
        require(isPublicSaleActive, "Public sale is not open");
        _;
    }

    modifier communitySaleActive() {
        require(isCommunitySaleActive, "Community sale is not open");
        _;
    }

    modifier maxWitchesPerWallet(uint256 numberOfTokens) {
        require(
            balanceOf(msg.sender) + numberOfTokens <= MAX_WITCHES_PER_WALLET,
            "Max witches to mint is three"
        );
        _;
    }

    modifier canMintWitches(uint256 numberOfTokens) {
        require(
            tokenCounter.current() + numberOfTokens <=
                maxWitches - maxGiftedWitches,
            "Not enough witches remaining to mint"
        );
        _;
    }

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

    modifier isCorrectPayment(uint256 price, uint256 numberOfTokens) {
        require(
            price * numberOfTokens == msg.value,
            "Incorrect ETH value sent"
        );
        _;
    }

    modifier isValidMerkleProof(bytes32[] calldata merkleProof, bytes32 root) {
        require(
            MerkleProof.verify(
                merkleProof,
                root,
                keccak256(abi.encodePacked(msg.sender))
            ),
            "Address does not exist in list"
        );
        _;
    }
```

### NFT 素材的存储

NFT 项目都需要包含图片的存储，合约将 NFT 对应的元信息存储在 IPFS 中，并将对应的图片存储都在 Amazon S3 存储中。

```solidity
    string private baseURI;    

    function setBaseURI(string memory _baseURI) external onlyOwner {
        baseURI = _baseURI;
    }

    /**
     * @dev See {IERC721Metadata-tokenURI}.
     */
    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(_exists(tokenId), "Nonexistent token");

        return
            string(abi.encodePacked(baseURI, "/", tokenId.toString(), ".json"));
    }
```

比如 `tokenId` 为 `1` 的 NFT，对应的 `tokenURI` 为 `ipfs://QmZHKZDavkvNfA9gSAg7HALv8jF7BJaKjUc9U2LSuvUySB/1.json`，在 IPFS 中可以看到这里面的内容为：

```json
{
  "description": "You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
  "external_url": "https://www.cryptocoven.xyz/witches/1",
  "image": "https://cryptocoven.s3.amazonaws.com/nyx.png",
  "name": "nyx",
  "background_color": "",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Sepia"
    },
    {
      "trait_type": "Skin Tone",
      "value": "Dawn"
    },
    {
      "trait_type": "Body Shape",
      "value": "Lithe"
    },
    {
      "trait_type": "Top",
      "value": "Sheer Top (Black)"
    },
    {
      "trait_type": "Eyebrows",
      "value": "Medium Flat (Black)"
    },
    {
      "trait_type": "Eye Style",
      "value": "Nyx"
    },
    {
      "trait_type": "Eye Color",
      "value": "Cloud"
    },
    {
      "trait_type": "Mouth",
      "value": "Nyx (Mocha)"
    },
    {
      "trait_type": "Hair (Front)",
      "value": "Nyx"
    },
    {
      "trait_type": "Hair (Back)",
      "value": "Nyx Long"
    },
    {
      "trait_type": "Hair Color",
      "value": "Steel"
    },
    {
      "trait_type": "Hat",
      "value": "Witch (Black)"
    },
    {
      "trait_type": "Necklace",
      "value": "Moon Necklace (Silver)"
    },
    {
      "trait_type": "Archetype of Power",
      "value": "Witch of Woe"
    },
    {
      "trait_type": "Sun Sign",
      "value": "Taurus"
    },
    {
      "trait_type": "Moon Sign",
      "value": "Aquarius"
    },
    {
      "trait_type": "Rising Sign",
      "value": "Capricorn"
    },
    {
      "display_type": "number",
      "trait_type": "Will",
      "value": 9
    },
    {
      "display_type": "number",
      "trait_type": "Wisdom",
      "value": 9
    },
    {
      "display_type": "number",
      "trait_type": "Wonder",
      "value": 9
    },
    {
      "display_type": "number",
      "trait_type": "Woe",
      "value": 10
    },
    {
      "display_type": "number",
      "trait_type": "Wit",
      "value": 9
    },
    {
      "display_type": "number",
      "trait_type": "Wiles",
      "value": 9
    }
  ],
  "coven": {
    "id": 1,
    "name": "nyx",
    "type": "Witch of Woe",
    "description": {
      "intro": "You are a WITCH of the highest order.",
      "hobby": "You are borne of chaos that gives the night shape.",
      "magic": "Your magic spawns from primordial darkness.",
      "typeSpecific": "You are called oracle by those wise enough to listen.",
      "exclamation": "ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!"
    },
    "skills": {
      "will": 9,
      "wisdom": 9,
      "wonder": 9,
      "woe": 10,
      "wit": 9,
      "wiles": 9
    },
    "birthChart": {
      "sun": "taurus",
      "moon": "aquarius",
      "rising": "capricorn"
    },
    "styles": [
      {
        "attribute": "background",
        "name": "solid",
        "color": "sepia",
        "fullName": "background_solid_sepia"
      },
      {
        "attribute": "base",
        "name": "lithe",
        "color": "dawn",
        "fullName": "base_lithe_dawn"
      },
      {
        "attribute": "body-under",
        "name": "sheer-top",
        "color": "black",
        "fullName": "body-under_sheer-top_black"
      },
      {
        "attribute": "eyebrows",
        "name": "medium-flat",
        "color": "black",
        "fullName": "eyebrows_medium-flat_black"
      },
      {
        "attribute": "eyes",
        "name": "nyx",
        "color": "cloud",
        "fullName": "eyes_nyx_cloud"
      },
      {
        "attribute": "mouth",
        "name": "nyx",
        "color": "mocha",
        "fullName": "mouth_nyx_mocha"
      },
      {
        "attribute": "hair-back",
        "name": "nyx",
        "color": "steel",
        "fullName": "hair-back_nyx_steel"
      },
      {
        "attribute": "hair-bangs",
        "name": "nyx",
        "color": "steel",
        "fullName": "hair-bangs_nyx_steel"
      },
      {
        "attribute": "hat-back",
        "name": "witch",
        "color": "black",
        "fullName": "hat-back_witch_black"
      },
      {
        "attribute": "hat-front",
        "name": "witch",
        "color": "black",
        "fullName": "hat-front_witch_black"
      },
      {
        "attribute": "necklace",
        "name": "moon-necklace",
        "color": "silver",
        "fullName": "necklace_moon-necklace_silver"
      }
    ],
    "hash": "nyx"
  }
}
```

其中包含女巫的ID，名称，图片地址，属性等信息。

不得不说，如果 Amazon S3 出问题了，可能这些图片就没法显示了。

### 使用 Merkle 证明实现白名单机制

对于预售，项目方使用白名单方式进行，而对于白名单验证，合约中使用 Merkle 证明的方式进行验证。

在 mint 时，只需发送正确的 Merkle 证明来验证即可实现白名单功能，这个方法不仅效率高，而且省去了在合约中存储所有白名单地址造成的 Gas 消耗。

```solidity
    modifier isValidMerkleProof(bytes32[] calldata merkleProof, bytes32 root) {
        require(
            MerkleProof.verify(
                merkleProof,
                root,
                keccak256(abi.encodePacked(msg.sender))
            ),
            "Address does not exist in list"
        );
        _;
    }

...

    function mintCommunitySale(
        uint8 numberOfTokens,
        bytes32[] calldata merkleProof
    )
        external
        payable
        nonReentrant
        communitySaleActive
        canMintWitches(numberOfTokens)
        isCorrectPayment(COMMUNITY_SALE_PRICE, numberOfTokens)
        isValidMerkleProof(merkleProof, communitySaleMerkleRoot)
    {
        // ...
    }

    function claim(bytes32[] calldata merkleProof)
        external
        isValidMerkleProof(merkleProof, claimListMerkleRoot)
        canGiftWitches(1)
    {
			// ...
    }
```

详细细节可以参考我之前的一篇文章：

### 预先批准 Opensea 合约

可以看到在 OpenSea 上列出这些 NFT 费用为 0 gas，因为合约预先批准了 OpenSea 合约以节省用户的 gas，同时合约还包括一个紧急功能来消除这种行为！

```solidity
    /**
     * @dev Override isApprovedForAll to allowlist user's OpenSea proxy accounts to enable gas-less listings.
     */
    function isApprovedForAll(address owner, address operator)
        public
        view
        override
        returns (bool)
    {
        // Get a reference to OpenSea's proxy registry contract by instantiating
        // the contract using the already existing address.
        ProxyRegistry proxyRegistry = ProxyRegistry(
            openSeaProxyRegistryAddress
        );
        if (
            isOpenSeaProxyActive &&
            address(proxyRegistry.proxies(owner)) == operator
        ) {
            return true;
        }

        return super.isApprovedForAll(owner, operator);
    }

...

// These contract definitions are used to create a reference to the OpenSea
// ProxyRegistry contract by using the registry's address (see isApprovedForAll).
contract OwnableDelegateProxy {

}

contract ProxyRegistry {
    mapping(address => OwnableDelegateProxy) public proxies;
}
```

为了防止 Opensea 关闭或者被入侵，合约可以通过 `setIsOpenSeaProxyActive` 方法关闭预先批准。

```solidity
    // function to disable gasless listings for security in case
    // opensea ever shuts down or is compromised
    function setIsOpenSeaProxyActive(bool _isOpenSeaProxyActive)
        external
        onlyOwner
    {
        isOpenSeaProxyActive = _isOpenSeaProxyActive;
    }
```

### ERC165

这是一种发布并能检测到一个智能合约实现了什么接口的标准，用于实现对合约实现的接口的查询。这个标准需要实现 `suppoetsInterface` 方法：

```solidity
interface ERC165 {
    /// @notice Query if a contract implements an interface
    /// @param interfaceID The interface identifier, as specified in ERC-165
    /// @dev Interface identification is specified in ERC-165. This function
    ///  uses less than 30,000 gas.
    /// @return `true` if the contract implements `interfaceID` and
    ///  `interfaceID` is not 0xffffffff, `false` otherwise
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}
```

加密女巫实现复写这个方法是因为它额外实现了 EIP2981 这个标准，需要指出。

```solidity
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721, IERC165)
        returns (bool)
    {
        return
            interfaceId == type(IERC2981).interfaceId ||
            super.supportsInterface(interfaceId);
    }
```

### EIP2981：NFT 版税标准

EIP-2981 实现了标准化的版税信息检索，可被任何类型的 NFT 市场接受。EIP-2981 支持所有市场检索特定 NFT 的版税支付信息，从而实现无论 NFT 在哪个市场出售或转售都可以实现准确的版税支付。

NFT 市场和个人可通过检索版税支付信息 `royaltyInfo()` 来实施该标准，它指定为特定的 NFT 销售价格向指定的单一地址支付特定比例的金额。对于特定的 `tokenId` 和 `salePrice`，在请求时需提供一个版税接收者的地址和要支付的预期版税金额（*百分比表示*）。

女巫合约规定了 5% 的版税，但是这个标准并不是强制性的，需要靠市场去实施此标准。

```solidity
    /**
     * @dev See {IERC165-royaltyInfo}.
     */
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

不太确定此函数中的注释 `See {IERC165-royaltyInfo}.` 是否正确，需要确认。

### 其他细节

1. 没有 `tokensOfOwner` 方法
    
    可能是基于女巫NFT的具体场景与优化 Gas 做的权衡，查询 token 所有者的功能需要靠 Opensea 的 API 或者 The Graph 去实现。
    

2. 在没有外部调用的函数中也加了 `nonReentrant`

1. `msg.sender` 可能是合约
2. 对 `onlyOwner` 也加了 `nonReentrant`，避免可能的被利用。

### 参考

1. **[为什么说 EIP-2981 的生效对于 NFT 创作者来说至关重要？](https://mp.weixin.qq.com/s/DVUYmHLJE75GJ2ATdtYhEw)**

### Comments

