# 极路由+shadowsocks翻墙


翻墙折腾无止境.
使用路由器翻墙的一个好处在于，对于一些翻墙配置很繁琐的设备，只需要简单地连上路由wifi就可以实现翻墙，
来家里的朋友也可以不需要配置就可以一连翻墙.
<!--more-->

## 一些背景

在旧版本的极路由已经有很不错的翻墙设置方式，感谢前人的大树：三流火的shadwosocks插件.在旧版本的极路由上
设置shadowsocks翻墙可已参考[极路由Shadowsocks家庭无痛翻墙实践](https://luolei.org/hiwifi-shadowsocks/).

最近极路由更新了新版本，管理界面风格大变导致之前的插件不能使用，在网上找了一段时间也没有看到有人对之前的
插件进行更新，所以决定自己写一个(其实后来才知道stary.love也有可用的插件,比我修改的插件功能强大很多).
所谓的自己写也只是在前人的基础上修改为适应新的极路由后台管理假面. 这过程要感谢stary.love的帮助，为我提供了
早期插件的一些源代码，以及许多帮着测试使用的人.

## 一些方法

项目地址: [qiwihui/hiwifi-ss](https://github.com/qiwihui/hiwifi-ss), 现在插件的状态：

1. 界面结构适应了新的hiwifi后台管理；

<img width="1006" alt="07-ss-settings" src="https://user-images.githubusercontent.com/3297411/45278213-a9e74900-b4fe-11e8-962b-8fd448edfbed.png">


3. 开启关闭翻墙功能和设置dns解析功能也都恢复；

<img width="1008" alt="07-ss-advance" src="https://user-images.githubusercontent.com/3297411/45278223-b5d30b00-b4fe-11e8-88c5-cdf2437bfe6f.png">


3. 新增加了最新的gfwlist列表(截止到2016年8月7日)的路由规则,解决了之前有部分网站无法访问的问题;

### 安装过程

(1). 开启极路由开发者模式
   
  需要开发者模式才能安装. 网上有很多教程,不赘述.

(2). 登录路由器, 一键安装脚本.
    
  极路由默认开启1022端口作为ssh端口,故使用`ssh root@192.168.199.1 -p 1022`登录路由器,运行如下一键脚本:

```sh
cd /tmp && curl -k -o shadow.sh https://raw.githubusercontent.com/qiwihui/hiwifi-ss/master/shadow.sh && sh shadow.sh && rm shadow.sh
```

然后登录后台管理界面,在`互联网`菜单下的`shadowsocks设置`配置ss账号就可以了.

## 一些展望

未来要做的一些工作:

1. 功能的改进: 包括但不限于ss版本的更新, 规则的更新, 流量混淆等;
2. 可能支持更多种类的工具;
3. 最重要的是: 开源. 包括底层的代码重写或者是找到之前的代码.

## 一些感想

 - "免费"是最贵的

怎么说呢, 我在最开始的时候, 寻找免费的vpn是获得翻墙的唯一方式, 这种方式的不好之处在于: vpn不稳定, 经常换, 
而且花费在寻找上的精力和时间算下来不合算. 之后精力了`地下铁路vpn`的消失之后, 自己搭建翻墙才成为我的主要翻墙
方式. 一个月花费的费用不到10美元, 带来的时稳定的流量和方式. VPS+shadowsocks/v2ray就可以提供稳定持久的方式.

 - 风险

不怎么使用vpn(免费或者收费)以及一些其他的收费翻墙服务，一则担心不安全, 流量劫持或者流量分析都有可能，甚者蜜罐, 
二则是重点观察对象, 服务失效的可能性还是存在的. 因此, 加密翻墙流量和混淆翻墙行为时十分重要的过程.

 - 技术人员获取资讯和信息的广度和及时性

因为GFW, 墙内封闭的环境使得获取技术知识的广度和及时性都受到了很严重的影响, 翻墙让搞技术的我们与世界更接近.

分享 [@lepture](https://twitter.com/lepture)的一个tweet: 

> 「我的互联网，上谷歌维基搜知识，上Reddit看看头条，上YouTube学习和开眼界，上Twitter关注一些正在改变世界的人和事，
去Quora上看看好的问题和回答，去SlideShare上学习以及了解不同的想法和观点」

## 总结

翻墙在于不断折腾.



[View on GitHub](https://github.com/qiwihui/blog/issues/21)


