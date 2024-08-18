# Tornado Cash 基本原理


假设地址 A 发送了 100 ETH 给地址 B，由于在区块链上所有的数据都是公开的，所以全世界都知道地址 A 和地址 B 进行了一次交易，如果地址A和地址 B 属于同一个用户 Alice，则大家知道Alice仍然拥有 100 ETH，如果地址B属于用户 Bob，则大家知道 Bob 现在有 100ETH 了。一个问题就是：如何在交易的过程中保持隐蔽呢，或者说隐藏发送用户与接收用户之前的练习？那就要用到 Tornado Cash。

用户将资金存入Tornado Cash，然后将资金提取到另一个地址中，在区块链上记录上，这两个地址之间的联系就大概率断开了。那 Tornado Cash 是如何做到的呢？

<!--more-->

## 存款（deposit）过程

首先我们看一下存款过程。用户在存款时需要生产两个随机数 secret 和 nullifier，并计算这两个数的一个哈希 commitment = hash(secret, nullifier)，然后用户将需要混币的金额（比如 1 ETH）和 commitment 发送给 TC 合约的 deposit 函数，TC合约将保存这两个数据，commitment之后会用于提取存入的资金。

同时，用户会得到一个凭证，通过这个凭证，用户（或者任何人）就可以提取存入的资金。

### 为什么存入 1 ETH？

如果不同的用户会存入不同的金额，比如 Alice 和 Bob 存入 1 ETH，Chris 存入 73 ETH，当取出存款时，某个地址提取了 73 ETH，我们会有很大程度怀疑这个地址属于 Chris。因此，在TC 合约中规定了每次存入的金额为 1 ETH，这样就不会有地址与其他地址不一致。

实际上，TC 有不同金额的 ETH 存款池，分别为 0.1，1，10，100，以满足不同数量的存取款需求。

## 取款（withdraw）过程

当进行取款时，一种错误方法是将之前随机生成的 secret 和 nullifier 作为参数发送给合约的取款函数，合约检查 hash(secret,nullifier) 是否等于之前保存的 commitment，如果相等就发送 1 ETH给取款者。但是这个过程就使得取款者的身份暴露了，因为 hash 过程是不可逆的，当我们从存款日志中找到相等的commitment时，我们就可以通过 commitment 建立存款者和取款者之间的联系，因为只有这个存款者知道获得 commitment 的 secret 和 nullifier。

如果解决这个过程呢？如果有人有一种方法可以证明他知道一组(secret, nullifier) 使得 hash(secret, nullifier) 在合约记录的commitment列表中，但是却不公开这组(secret, nullifier) ，那这个人就可以只用发送这个证明给合约进行验证，就可以证明他拥有之前存入过资金，当却不知道对应于哪一组存入的资金，所以仍然保持匿名。

这个证明就是零知识证明，它可以证明你知道某个信息但却不用公开这个信息。TC 使用的零知识证明称为 zk-SNARK。

我们注意到当用户存款和取款时，使用了两个随机数 secret 和 nullifier，nullifier 的作用是什么呢？当用户取款时，合约其实不知道到底是谁在取款，为了避免用户存入 1 ETH 然后进行多次提取，TC要求当用户发送证明的同时发送 nullifier 的哈希nullifierHash，在zk-SNARK的证明中，他会检查两件事情：一是检查 hash(secret, nullifier) 在 commitment 的列表中，二是 nullifierHash 等于 hash(nullifier)，一旦验证成功，合约就会记录这个哈希。当同一个证明第二次被提交时就会失败，因为对应的 nullifier 哈希已经使用过了，这样就避免了二次提款。

### Tornado Cash 如何保存 commitment 呢

使用 Merkle 树。Merkle树具体参见之前的介绍文章。

TC 会首先初始化一组叶子节点为 `keccak256("tornado")`，并以这些叶子节点构建一颗 Merkle 树。当用户存款时，对应的 commitment 存入 Merkle 树的第一个叶子节点，然后合约更新整棵 Merkle 树，然后是第二个用户的commitment 存入第二个叶子节点并更新整棵 Merkle 树，依次类推。

![Untitled](https://user-images.githubusercontent.com/3297411/188539564-5178bafe-dd46-4409-8de5-fdcc194e88e4.png)

如何证明 commitment 在这棵 Merkle 树中呢？

![Untitled 1](https://user-images.githubusercontent.com/3297411/188539594-233fbff1-9cc8-43c9-99a2-86a7045f3efe.png)

假设需要证明c3在这棵Merkel中，我们需要找到从叶子节点 c3 到根的路径过程中的哈希，使得他们与 c3 依次进行 hash 可以得到根哈希，即图中绿色节点的哈希列表。

Tornado Cash 中，我们需要提供这些节点哈希，并通过 zk-SNARK 生成零知识证明，以此证明 c3 在这棵以 root（`=h(h(h(c0,c1),h(c2,c3)),h(h(c4,c5), z1))`）为根的 Merkle 中，但却不用告诉大家 c3 的值。

![Untitled 2](https://user-images.githubusercontent.com/3297411/188539613-fe0ccd14-c7e7-4143-847a-e71d3b475e1f.png)

因此我们将证明 proof 和 Merkle 树根 root 发送给合约，一旦合约验证成功，我们就可以取出之前存入的存款。

## solidity 中的 zk-SNARK 实现

TC 合约包含三个部分：

1. 存款和取款合约，用于与用户交互；
2. Merkle 树，用于记录存款哈希；
3. zk-SNARK 验证器合约，用于验证取款时证明合法。

zk-SNARK 验证器合约由 circom 编写的验证电路通过 snarkjs 库生成。

## 参考

- [Tornado Cash - How it Works | DeFi + Zero Knowledge Proof](https://www.youtube.com/watch?v=z_cRicXX1jI)


[View on GitHub](https://github.com/qiwihui/blog/issues/164)


