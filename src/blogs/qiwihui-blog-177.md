# 写一个 pump.fun 智能合约，创建以太坊上的Meme发售平台


Pump.fun 是 Solana 的超级 meme 发射平台。当成功在 pump.fun 上部署一枚 Meme 后，一旦代币市值达到 69,000 美元，会自动将 pump.fun 的流动性添加到 Raydium 交易所。

对于用户来说，可以降低发币费用以及繁琐的流程，主要解决的痛点是rug和老鼠仓问题，也就是公平发射问题。pump.fun 将 Meme 团队要做的事情产品化，从代币名称、logo 到流动性和流动性销毁做到了一条龙服务。

这个系列的视频实现了EVM 下的类似代币发射合约。

代码仓库： https://github.com/qiwihui/pumpeth

 ## 第一部分

视频链接： <https://youtu.be/k-LTUa9g1sU>

主要包含如下功能：

1. 创建代币
2. 购买代币
3. 卖出代币

## 第二部分

视频链接： <https://youtu.be/1zdCAg2d3nk>

主要包含如下功能：

1. 检查 token 状态
2. Fork mainnet 然后测试
3. minimal proxy 模式
4. Bonding Curve 曲线

## 第三部分

视频链接：  <https://youtu.be/BMukVfQVwHg>

主要讲解了 $$ y=a*e^(bx)$$ 指数型联合曲线的实现。

对应的联合曲线文档：https://qiwihui.notion.site/Pump-fun-Clone-759c1b3f1ec94b8a8b5b180f72abc838?pvs=4


[View on GitHub](https://github.com/qiwihui/blog/issues/177)


