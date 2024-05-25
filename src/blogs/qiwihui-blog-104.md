---
title: "Shadowsocks 和 V2ray 共用443端口"
description: "Shadowsocks 和 V2ray 共用443端口"
tags: 
- 技术
- GFW
top: 104
date: 14/10/2020, 17:13:12
author: qiwihui
update: 16/10/2020, 10:05:41
categories: 技术
---

## 配置过程

之前部署了 Shadowsocks 和 V2ray 在两台服务器上，最近由于费用增加，于是决定将两个服务合并到同一台服务器上，并保持原来的配置文件不变。此文简单记录。

Shadowsocks 配置了 simple-obfs 浑下，参数为 `obfs=tls`。V2ray 使用 nginx + tls + websocket，并使用letsencrypt自动生成 HTTPS 证书。两个均使用不同的域名访问。

主要的难点在于需要根据不同的域名将流量分发到后端不同的代理上，方法使用 Nginx 基于 SNI 的 4 层转发，即识别 SNI 信息，然后直接转发 TCP/UDP 数据流。使用的模块是 `ngx_stream_ssl_preread_module`，这个模块在 Nginx 1.11.5 之后才引入，注意开启。

<!--more-->

```
                                     ----> shadowsocks
                                     |
客户端 --[请求]--> Nginx ----[分发]---->
                                     |
                                     ----> v2ray
```

为了方便部署，使用 docker-compose 完成整个部署过程，项目地址 [qiwihui/ssv2ray](https://github.com/qiwihui/ssv2ray)。

Nginx 关键配置：

```conf

stream {
    # SNI, domain to config
    map $ssl_preread_server_name $backend_name {
        domain1.com v2fly;
        domain2.com shadowsocks;
        # 因为使用了混淆，所以这里需要填入混淆的域名，比如 www.bing.com
        www.bing.com shadowsocks;
        default v2fly;
    }

    # v2ray
    upstream v2fly {
        server nginx-proxy:443;
    }
    upstream v2fly80 {
        server nginx-proxy:80;
    }

    # shadowsocks
    upstream shadowsocks {
        server shadowsocks:443;
    }

    # 80，这个端口用于自动生成证书
    server {
        listen 80;
        listen [::]:80;
        proxy_pass v2fly80;
    }

    server {
        listen 443 reuseport;
        listen [::]:443 reuseport;
        proxy_pass  $backend_name;
        ssl_preread on;
    }
}
```

## 参考

1. [Trojan 共用 443 端口方案](https://www.chengxiaobai.cn/record/trojan-shared-443-port-scheme.html)

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

