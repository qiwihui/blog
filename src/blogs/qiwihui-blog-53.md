---
title: "在 Mac OS X 上使用 iodine 配置 DNS 隧道"
description: "在 Mac OS X 上使用 iodine 配置 DNS 隧道"
tags: 
- 技术
top: 53
date: 30/01/2019, 15:31:20
author: qiwihui
update: 09/05/2019, 14:50:20
categories: 技术
---

> DNS 隧道，是隐蔽信道的一种，通过将其他协议封装在DNS协议中传输建立通信。

本文是在 Mac OS X 上实践的 DNS 隧道的一个记录，关于这个方法的原理，请具体参考 [DNS Tunneling及相关实现](https://cloud.tencent.com/developer/article/1040276)。

<!--more-->

## 安装和配置

### 配置域名

准备一台 VPS 以及一个域名（比如 `qiwihui.com`），在域名的 DNS 配置中添加两条记录：

| Name  | Type  | TTL  | Data  |
|---|---|---|---|
| dns  | A  | 1h  | `vps-ip`  |
| dt  | NS  | 1h  | dns.qiwihui.com  |

### 服务端

以 Debian 系统为例，安装：

```bash
apt update
apt install iodine
```

使用

```bash
$ iodined -f -c -P password 172.18.0.1 dt.qiwihui.com 
Opened dns0
Setting IP of dns0 to 172.18.0.1
Setting MTU of dns0 to 1130
Opened IPv4 UDP socket
Listening to dns for domain dt.qiwihui.com
```

其中，`password` 是客户端和服务器之前的密码，`172.18.0.1` 为虚拟局域网的IP地址，可自行设定，但不要与现有网络重复了。此时，服务端已经就绪。

### 客户端（本地）安装 `iodine`

1. 本地安装 `tuntap`

```bash
brew cask install tuntap
```

2. 安装 `iodine`

因为官方没有提供 Mac OS X 的可执行文件，需要从源码编译，或者使用我已经设置好的 Homebrew tap 进行安装。从源码编译：

```bash
wget -c http://code.kryo.se/iodine/iodine-0.7.0.tar.gz
tar zxvf iodine-0.7.0.tar.gz
cd iodine-0.7.0
make
make install
```

或者使用 Homebrew：

```bash
brew tap qiwihui/core
brew install qiwihui/core/iodine
```

使用：

```bash
$ sudo iodine -f -P password dns.qiwihui.com dt.qiwihui.com
Opened /dev/tun0
Opened IPv4 UDP socket
Sending DNS queries for dt.qiwihui.com to <vps-ip>
Autodetecting DNS query type (use -T to override).
Using DNS type NULL queries
Version ok, both using protocol v 0x00000502. You are user #1
Setting IP of tun0 to 172.18.0.3
Adding route 172.18.0.0/27 to 172.18.0.3
add net 172.18.0.0: gateway 172.18.0.3
Setting MTU of tun0 to 1130
Server tunnel IP is 172.18.0.1
Testing raw UDP data to the server (skip with -r).
Server is at 10.170.0.3, trying raw login: ....failed
Retrying EDNS0 support test...
Using EDNS0 extension
Switching upstream to codec Base128
Server switched upstream to codec Base128
No alternative downstream codec available, using default (Raw)
Switching to lazy mode for low-latency
Server switched to lazy mode
Autoprobing max downstream fragment size... (skip with -m fragsize)
768 ok.. ...1152 not ok.. 960 ok.. 1056 ok.. 1104 ok.. 1128 ok.. 1140 ok.. will use 1140-2=1138
Setting downstream fragment size to max 1138...
Retrying set fragsize...
Retrying set fragsize...
Connection setup complete, transmitting data.
```

此时，客户端配置完成。

### 测试和使用

在本地尝试 ping 172.18.0.1 即可：

```bash
$ ping 172.18.0.1
PING 172.18.0.1 (172.18.0.1): 56 data bytes
64 bytes from 172.18.0.1: icmp_seq=0 ttl=64 time=233.914 ms
64 bytes from 172.18.0.1: icmp_seq=1 ttl=64 time=232.870 ms
64 bytes from 172.18.0.1: icmp_seq=2 ttl=64 time=230.201 ms
64 bytes from 172.18.0.1: icmp_seq=3 ttl=64 time=268.602 ms
64 bytes from 172.18.0.1: icmp_seq=4 ttl=64 time=230.573 ms
^C
--- 172.18.0.1 ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 230.201/239.232/268.602/14.751 ms
```

这时，只要通过这个 DNS 隧道就可就传递其他数据了。

## 用途

当防火墙限制了一些网站的访问，但是能进行 DNS 查询时，可使用这种方法进行绕过，比如在公司，又或者在某些国家，犯罪分子也常用这中方式进行内网数据传出。

## 参考

- http://code.kryo.se/iodine/：iodine 官方网站，kryo.se: iodine (IP-over-DNS, IPv4 over DNS tunnel)
- https://github.com/yarrick/iodine：Official git repo for iodine dns tunnel
- [DNS Tunneling及相关实现](https://cloud.tencent.com/developer/article/1040276)
- [iodine - IP over DNS](http://jeremy5189.logdown.com/posts/263029-iodine-ip-over-dns)
- [Tunnel IP through DNS](http://wiki.attie.co.uk/wiki/Tunnel_IP_through_DNS)


### Comments

---
> from: [**shaohuihu**](https://github.com/qiwihui/blog/issues/53#issuecomment-486480977) on: **4/25/2019**

mac上使用 iodined: open_tun: Failed to open tunneling device: No such file or directory
楼主mac上如何解决的TUN/TAP?
---
> from: [**qiwihui**](https://github.com/qiwihui/blog/issues/53#issuecomment-486482390) on: **4/25/2019**

@shaohuihu 你需要tuntap：`brew cask install tuntap`
---
> from: [**shaohuihu**](https://github.com/qiwihui/blog/issues/53#issuecomment-486503799) on: **4/25/2019**

请问  这个dns服务器 以及iodine 客户端 服务端自己搭建在本地好使不？
---
> from: [**qiwihui**](https://github.com/qiwihui/blog/issues/53#issuecomment-486529656) on: **4/25/2019**

@shaohuihu  在直连模式下可看youtube 720p, 中继模式下没试过，看相关文章速度也是在其他几种DNS tunneling中是最快的。

---
> from: [**shaohuihu**](https://github.com/qiwihui/blog/issues/53#issuecomment-486972412) on: **4/26/2019**

客服端和服务端都配置好后。ping ip 报错：ping: sendto: No buffer space available 请问这个是什么原因呢？@qiwihui
---
> from: [**shaohuihu**](https://github.com/qiwihui/blog/issues/53#issuecomment-487355342) on: **4/28/2019**

@qiwihui  这个困扰了好久了 服务端我也check了 是对的，客户端也连接完成53端口我也开放了，服务端和客户端版本也是一样的，就是ping 不通。不能通信，你知道为什么吗
---
> from: [**qiwihui**](https://github.com/qiwihui/blog/issues/53#issuecomment-487360896) on: **4/28/2019**

@shaohuihu 这个问题原因很多，可是试试重置网卡

1. 确定使用的网卡

```shell
$ sudo route -n get 172.18.0.1
   route to: 172.18.0.1
destination: 172.18.0.0
       mask: 255.255.255.224
    gateway: 172.18.0.2
  interface: tun0
      flags: <UP,GATEWAY,DONE,STATIC,PRCLONING>
 recvpipe  sendpipe  ssthresh  rtt,msec    rttvar  hopcount      mtu     expire
       0         0         0         0         0         0      1130         0 
```

2. 重置

```shell
sudo ifconfig tun0 down
sudo ifconfig tun0 up
```
---
> from: [**qiwihui**](https://github.com/qiwihui/blog/issues/53#issuecomment-487361085) on: **4/28/2019**

可以参考：
- https://docs.netgate.com/pfsense/en/latest/routing/no-buffer-space-available.html
- https://odino.org/ping-sendto-no-buffer-space-available-with-du-dnses/
---
> from: [**badtoken**](https://github.com/qiwihui/blog/issues/53#issuecomment-490726534) on: **5/9/2019**

> @shaohuihu 这个问题原因很多，可是试试重置网卡
> 
> 1. 确定使用的网卡
> 
> ```shell
> $ sudo route -n get 172.18.0.1
>    route to: 172.18.0.1
> destination: 172.18.0.0
>        mask: 255.255.255.224
>     gateway: 172.18.0.2
>   interface: tun0
>       flags: <UP,GATEWAY,DONE,STATIC,PRCLONING>
>  recvpipe  sendpipe  ssthresh  rtt,msec    rttvar  hopcount      mtu     expire
>        0         0         0         0         0         0      1130         0 
> ```
> 
> 1. 重置
> 
> ```shell
> sudo ifconfig tun0 down
> sudo ifconfig tun0 up
> ```

你好，请问有win的解决方案吗。
我现在也是ping不通，win客户端ping隧道的服务端内网地址，死活不通（ping隧道服务端外网地址是通的）
---
> from: [**qiwihui**](https://github.com/qiwihui/blog/issues/53#issuecomment-490766765) on: **5/9/2019**

@badtoken 应该也有吧，比如这个 https://kb.wisc.edu/helpdesk/page.php?id=6653 ，具体我也没有试过
