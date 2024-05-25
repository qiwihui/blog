---
title: "使用免费的let’s encrypt证书为网站开启https（已过时）"
description: "使用免费的let’s encrypt证书为网站开启https（已过时）"
tags: 
- 技术
top: 23
date: 10/09/2018, 13:39:29
author: qiwihui
update: 31/01/2019, 16:05:58
categories: 技术
---

这篇博客将介绍使用免费的let's encrypt证书, 为网站开启https。
<!--more-->

## HTTPS简介

(https, http over ssl)

## 为啥要用Let's Encrypt

(free, easy)

## Let's Encrypt介绍

(directory tree)

## 安装实践

我使用的是Debian 7，其他系统类似。

1. 使用官方推荐的`letsencrypt-auto`安装：

```sh
$ git clone https://github.com/letsencrypt/letsencrypt

$ cd letsencrypt

$ ./letsencrypt-auto --help
```

2. 获取证书

实验前，我已将`www.qiwihui.com`站点移到了要安装的服务器上，nginx已经在运行，因此可以使用 webroot 模式来获取证书，
先安装webroot插件，这是一个可以不用停止 Web 服务就能让 Let’s Encrypt 验证域名的插件：

```
location ~ /.well-known {
    allow all;
}
```

安装证书命令如下：

```sh
$ ./letsencrypt-auto certonly --webroot --webroot-path /var/www/blog/ -d qiwihui.com -d www.qiwihui.com --agree-tos --email qiwihui@qiwihui.com
```

其中`/var/www/blog/`为网站根目录。证书申请成功后会提示一下信息，包括证书存放目录和证书过期时间：

```sh
IMPORTANT NOTES:

- Congratulations! Your certificate and chain have been saved at
/etc/letsencrypt/live/qiwihui.com/fullchain.pem. Your cert will
expire on 2016-07-08. To obtain a new version of the certificate in
the future, simply run Let's Encrypt again.

- If you like Let's Encrypt, please consider supporting our work by:

Donating to ISRG / Let's Encrypt:  https://letsencrypt.org/donate
Donating to EFF:                    https://eff.org/donate-le
```

*重要提示*：需要将站点的DNS指向对用的服务器，否则会提示申请不过。

3. 配置Nginx

首先生成2048位 DH parameters：

```sh
$ mkdir -p /var/www/ssl/
$ sudo openssl dhparam -out /var/www/ssl/dhparam.pem 2048
```

Nginx的配置如下：

```nginx
server {
        listen 443 ssl;

        server_name qiwihui.com www.qiwihui.com;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_certificate     /etc/letsencrypt/live/qiwihui.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/qiwihui.com/privkey.pem;

        ssl_dhparam /var/www/ssl/dhparam.pem;

        ssl_prefer_server_ciphers  on;
        ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';

	#网站其他配置
}
```

如果想要开启全站 https 的话，需要将 http 转向到 https，再添加一个 server 就好了：

```nginx
server {
    listen 80;
    server_name qiwihui.com www.qiwihui.com;
    return 301 https://$server_name$request_uri;
}
```

修改完成后reload nginx 就可以了：`nginx -s reload`

### 验证检测

1. 用浏览器打开目标网址`https://qiwihui.com`，可以查看到证书信息：

<img width="792" alt="10-https-on-qiwihui-com" src="https://user-images.githubusercontent.com/3297411/45278285-064a6880-b4ff-11e8-9ff2-24cce84cdec8.png">

2. 使用 [Qualys ssllabs](https://www.ssllabs.com/ssltest/index.html) 在线测试服务器证书强度以及配置正确性：

<img width="1374" alt="10-ssllabs-results" src="https://user-images.githubusercontent.com/3297411/45278293-0cd8e000-b4ff-11e8-80c6-a6cd4c8ce89e.png">


### 后续更新

Let’s Encrypt 的有效期只有90天，官方客户端不支持持续更新，所以要设置自动更新，让证书一直有效。

在crontab 中设置定时任务：

```sh
30 2 * * 1 /root/letsencrypt/letsencrypt-auto renew >> /var/log/le-renew.log
35 2 * * 1 /etc/init.d/nginx reload
```

上述配置会再每周一凌晨2:30执行`letsencrypt-auto renew`，在2点35分重新加载nginx配置，同时更新日志会在写在`/var/log/le-renewal.log`中。

## 总结

Let's Encrypt TLS/SSL is free.



### Comments

