# 在 Mac OS X 上使用 iodine 配置 DNS 隧道


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


[View on GitHub](https://github.com/qiwihui/blog/issues/53)


