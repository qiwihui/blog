# 用Homebrew 安装 v2ray 以及 Homebrew-cask 安装 V2RayX

最近开始转向使用 v2ray 作为主要的翻墙工具，在 macOS 上安装和使用都需要下载编译好的软件包然后解包使用，不是很方便，联系到 macOS 下常用的包管理 Homebrew，何不自己提交一个？
<!--more-->

### v2ray及V2RayX是啥？

> V2Ray 是一个模块化的代理软件包，它的目标是提供常用的代理软件模块，简化网络代理软件的开发。

简单说 [v2ray](https://github.com/v2ray/v2ray-core) 就是翻墙代理软件（但不止于软件，是一个平台）。[V2RayX](https://github.com/Cenmrev/V2RayX) 就是 macOS 下一个简单的 v2ray 的GUI程序。

### Homebrew呢？

macOS上强大的包管理工具，类似于Ubuntu的apt。

安装：

```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

使用，比如下载 `curl`:

```
brew install curl
```

### 安装v2ray

不知道为啥，官方的Homebrew Formula不接受 v2ray 源，所以只能自己写了，见 [qiwihui/homebrew-v2ray](https://github.com/qiwihui/homebrew-v2ray)。

安装：

```bash
brew tap qiwihui/v2ray
brew install v2ray-core
```

使用：

首先，需要配置 `/usr/local/etc//v2ray.config.json`；
其次，配置v2ray登录时自动开启：

```bash
brew services start v2ray-core
```
或者，可以手动运行：

```bash
v2ray -config=/usr/local/etc//v2ray.config.json
```

### 安装V2RayX

我向官方 [Homebrew-Cask](https://caskroom.github.io/) 提交了一个Formula，可以直接使用如下命令安装

```bash
brew cask install v2rayx
```

不过GUI毕竟不能覆盖命令行的全部功能，所以能用命令行v2ray的话，就尽量不使用V2RayX吧。
