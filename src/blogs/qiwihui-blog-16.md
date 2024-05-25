---
title: "树莓派启动时自动连接wifi"
description: "树莓派启动时自动连接wifi"
tags: 
- 技术
top: 16
date: 10/09/2018, 13:31:11
author: qiwihui
update: 31/01/2019, 16:08:50
categories: 技术
---

这篇文章的目的是为了配置树莓派，使其在启动时自动获取静态IP.
<!--more-->

## 启动并连接树莓派

#### 1. 启动树莓派并找到其IP地址

把树莓派用网线连接到路由器上，插上SD卡，打开树莓派电源，等大约90秒.  
在Mac上打开命令行终端，输入`arp -a`命令，可以看到树莓派的ip地址为 `192.168.199.199`. 
当然也可以从路由器后台看到这个IP地址.

```bash
$ arp -a
? (169.254.99.51) at (incomplete) on en0 [ethernet]
hiwifi.lan (192.168.199.1) at d4:ee:7:20:18:6e on en0 ifscope [ethernet]
raspberrypi.lan (192.168.199.199) at f0:f6:1c:af:7a:28 on en0 ifscope [ethernet]
```

#### 2. 使用SSH连接树莓派

输入"ssh pi@192.168.199.199", 根据要求输入密码，默认为`raspberry`.

```bash
$ ssh pi@192.168.199.199
pi@192.168.199.199s password: 
Linux qiwihuisrpi 3.18.7+ #755 PREEMPT Thu Feb 12 17:14:31 GMT 2015 armv6l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Apr 17 14:45:28 2015 from 192.168.199.186
```

## 配置网络连接

#### 1. 设置网络接口文件`/etc/network/interfaces`

编辑这个文件：

```bash
$ sudo nano /etc/network/interfaces
```

添加如下内容：

```bash
auto lo
iface lo inet loopback

auto eth0
allow-hotplug eth0
iface eth0 inet dhcp

auto wlan0
allow-hotplug wlan0
iface wlan0 inet manual
# iface wlan0 inet dhcp # 如果想自动获取ip
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

# 设置静态ip
iface wlan0 inet static
address 192.168.199.199
netmask 255.255.255.0
gateway 192.168.199.1

iface default inet dhcp
```

#### 2. 设置`wpa_supplicant.conf`配置文件

编辑文件`wpa_supplicant.conf`设置连接的网络热点.

```bash
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

为：

```bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOU_NETWORK_PASSWORD"
    proto=RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP
    auth_alg=OPEN
}
```

其中:

- `proto` 可以是 `RSN` (WPA2) 或者 `WPA` (WPA1).
- `key_mgmt` 可以是 `WPA-PSK` (大部分) 或者 `WPA-EAP` (企业网络)
- `pairwise` 可以是 `CCMP` (WPA2) 或者 `TKIP` (WPA1)
- `auth_alg` 常为 `OPEN`, 其他可选为 `LEAP` 和 `SHARED`

重启树莓派，之后就会自动连上wifi了.


### Comments

