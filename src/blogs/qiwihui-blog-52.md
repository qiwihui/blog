# 在 Mac OS X 上使用 hans 配置 ICMP 隧道


最近因为电信白名单，高端口基本无法使用，解决办法就是将翻墙服务启动在80，443等可访问端口。但是最近防火墙又一次升级，国外的服务器基本只能 ping 通，TCP 请求无法完成，能访问世界的方式越来越困难。本文介绍一种方法，将数据包封装在 ping 包中进行传输。本方法中使用 [hans](http://code.gerade.org/hans/) 这个项目结合 shadowsocks-libev 翻墙。

<!--more-->

## 安装

### 服务器端

同样，需要在服务器端编译安装 `hans`：

```bash
wget -c https://github.com/friedrich/hans/archive/v1.0.tar.gz
tar zxvf v1.0.tar.gz
cd hans-1.0/
make
```

编译完成后会产生 `hans` 执行程序，按以下命令以 `root` 启动，程序会进入 Deamon 模式。如果要看到输出，可以加上 `-f` 参数。

```bash
./hans -s 10.1.2.0 -p password
```

其中，`password` 为设置的密码。然后使用 `netstat -rn` 可以看到多了一个 `tun0` 设备

```bash
$ netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
(省略其他的)
10.1.2.0        0.0.0.0         255.255.255.0   U         0 0          0 tun0
```

### 客户端

在 Mac OS X 上，先安装 `tuntap` 内核扩展来允许创建虚拟网卡，可以直接使用 Homebrew-Cask 安装，安装过程中需要按照指示给程序权限。

```bash
$ brew cask install tuntap
```

下载 Mac 版本程序并解压：[hans](https://sourceforge.net/projects/hanstunnel/files/osx/)

运行程序：

```bash
sudo ./hans -c <server-ip> -p password -d tun0
```

其中 `server-ip` 是你服务器的 IP，`-d` 指定Mac上新启设备的名称。Mac 上停止 `hans` 程序请使用 `kill -9`。如果启动正常，这时在Mac上也同样可以观察到tun0设备：

```bash
$ ifconfig

(省略其他)
tun0: flags=8851<UP,POINTOPOINT,RUNNING,SIMPLEX,MULTICAST> mtu 1467
        inet 10.1.2.100 --> 10.1.2.1 netmask 0xffffffff 
        open (pid 74236)
```

理论上这时服务器 IP 是无法 ping 通了：

```bash
$ ping <server-ip>
PING <server-ip>: 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2
Request timeout for icmp_seq 3
^C
--- <server-ip> ping statistics ---
5 packets transmitted, 0 packets received, 100.0% packet loss
```

此时，就建立了一条从本地到服务器的 hanstunnel tunnel 了。

现在只需要将本地 `ss-local` 的配置中的 `server` 参数改为 `tun0` 的 gateway 地址（本例为`10.1.2.1`）即可，其他不需要做任何修改。

### 检查流量

在服务器网卡上抓包可以不断看到 ICMP 的 ｀echo request｀ 和 ｀echo reply｀ 包，在 `tun0` 上可以看到实际的数据包。

```bash
$ tcpdump -ni ens3

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens3, link-type EN10MB (Ethernet), capture size 262144 bytes
02:16:29.146644 IP <local-ip> > <server-ip>: ICMP echo request, id 38174, seq 7330, length 93
02:16:29.146647 IP <local-ip> > <server-ip>: ICMP echo request, id 38174, seq 7330, length 13
02:16:29.146652 IP <local-ip> > <server-ip>: ICMP echo request, id 38174, seq 7330, length 13
02:16:29.146684 IP <local-ip> > <server-ip>: ICMP echo request, id 38174, seq 7330, length 93
02:16:29.146704 IP <server-ip> > <local-ip>: ICMP echo reply, id 38174, seq 7330, length 257
02:16:29.146858 IP <server-ip> > <local-ip>: ICMP echo reply, id 38174, seq 7330, length 833
02:16:29.146942 IP <server-ip> > <local-ip>: ICMP echo reply, id 38174, seq 7330, length 257

(略去一堆)
```

以上就是使用 TCP over ICMP 的方法进行数据传输的配置过程。


[View on GitHub](https://github.com/qiwihui/blog/issues/52)


