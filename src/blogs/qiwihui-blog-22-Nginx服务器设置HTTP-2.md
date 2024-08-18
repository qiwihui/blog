# Nginx服务器设置HTTP/2


我的博客已经支持了 HTTP/2, 在此将介绍如何在 Nginx 上设置 HTTP/2 及相关注意事项(坑)。

## 前提

HTTP/2 安装需要以下前提：

- Nginx 版本在1.9.5以上
- OpenSSL 版本在 1.0.2g 以上（支持 ALPN）

<!--more-->

不同 Linux 系统对于 `ALPN` 和 `NPN` 的支持可以参见下表

|Operating System	            |OpenSSL Version	|ALPN and NPN Support|
|-------------------------------|--------------------|--------------------|
|CentOS/Oracle Linux/RHEL 5.10+	|0.9.8e	            |Neither|
|CentOS/Oracle Linux/RHEL 6.5+, 7.0+    |1.0.1e	    |NPN|
|Ubuntu 12.04 LTS	            |1.0.1	            |NPN|
|Ubuntu 14.04 LTS	            |1.0.1f	            |NPN|
|Ubuntu 16.04 LTS	            |1.0.2g	            |ALPN and NPN|
|Debian 7.0	                    |1.0.1e	            |NPN|
|Debian 8.0	                    |1.0.1k	            |NPN|

所以要么升级使用带有 OpenSSL 1.0.2 的 Ubuntu 16.04 LTS，要么从头编译 Nginx.

我的服务器系统是 Debian 7, OpenSSL 版本是1.0.1t, 所以需要重新编译 Nginx 和 OpenSSL.

## 安装过程

### 安装 OpenSSL

下载并安装 OpenSSL:

```bash
# cd ~
# wget http://www.openssl.org/source/openssl-1.1.0e.tar.gz
# tar -zxf openssl-1.1.0e.tar.gz
# cd openssl-1.1.0e
# ./configure
# make
# sudo make install
```

使用 `openssl version` 来查看安装好的 OpenSSL 的版本。

### 其他 Nginx 编译需要的环境

需要编译 `PCRE` 库和 `zlib` 库[]：

```bash
# wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.40.tar.gz
# tar -zxf pcre-8.40.tar.gz
# cd pcre-8.40
# ./configure
# make
# sudo make install
```
```bash
# wget http://zlib.net/zlib-1.2.11.tar.gz
# tar -zxf zlib-1.2.11.tar.gz
# cd zlib-1.2.11
# ./configure
# make
# sudo make install
```

### 编译 Nginx

首先，下载最新的 nginx，我使用 1.10.3.
    
```bash
cd ~
wget -c http://nginx.org/download/nginx-1.10.3.tar.gz
tar xzvf nginx-1.10.3.tar.gzcd nginx-1.10.3
```

其实，获取 Nginx 配置参数，使新版 Nginx 和之前的配置一样

```bash
# nginx -V

nginx version: nginx/1.9.6
built by gcc 4.7.2 (Debian 4.7.2-5) 
built with OpenSSL 1.0.1t  3 May 2016
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-file-aio --with-threads --with-ipv6 --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_ssl_module --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'
```

上述配置用已经有 `--with-http_v2_module` 选项了，还需要在上述配置参数后面加上 `--with-openssl=/path/to/your/openssl-1.1.0e` 指向新版本的 OpenSSL 文件夹

```bash
./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-file-aio --with-threads --with-ipv6 --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_ssl_module --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie' --with-openssl=/home/qiwihui/openssl-1.1.0e
```    

可以看到大致输出为

```bash
Configuration summary
  + using threads
  + using system PCRE library
  + using OpenSSL library: /home/qiwihui/openssl-1.1.0e
  + md5: using OpenSSL library
  + sha1: using OpenSSL library
  + using system zlib library

  nginx path prefix: "/etc/nginx"
  nginx binary file: "/usr/sbin/nginx"
  nginx modules path: "/usr/lib/nginx/modules"
  nginx configuration prefix: "/etc/nginx"
  nginx configuration file: "/etc/nginx/nginx.conf"
  nginx pid file: "/var/run/nginx.pid"
  nginx error log file: "/var/log/nginx/error.log"
  nginx http access log file: "/var/log/nginx/access.log"
  nginx http client request body temporary files: "/var/cache/nginx/client_temp"
  nginx http proxy temporary files: "/var/cache/nginx/proxy_temp"
  nginx http fastcgi temporary files: "/var/cache/nginx/fastcgi_temp"
  nginx http uwsgi temporary files: "/var/cache/nginx/uwsgi_temp"
  nginx http scgi temporary files: "/var/cache/nginx/scgi_temp"
```

最后，编译并安装

```bash
# make
# sudo make install
```

之后就可以看到已经安装好了新版 Nginx了。

### 配置

#### 配置 HTTPS

请参考之前博客 [使用免费的let’s encrypt证书为网站开启https](https://blog.qiwihui.com/2016/04/10/enable-https/)

#### 开启 http/2

第一步完成后就设置好了一个 HTTPS 的网站了，在此基础之上开始 HTTP/2。首先，开启 HTTP/2：

```bash
listen 443 ssl http2 default_server;
```

其次，去除HTTP/2不支持的旧的不安全的密码套件[5]:

```bash
ssl_prefer_server_ciphers on;
ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
```

最后，检查配置并重启 Nginx:

```bash
# nginx -t

nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

# sudo /etc/init.d/nginx restart
```

## 检查

至此，不出问题的话你的服务器已经开始支持 HTTP/2 了，可以使用 [HTTP/2 Test](https://tools.keycdn.com/http2-test) 来检测是否支持了 HTTP/2

![](/media/files/2017/02/19-qiwihui-com-http2.png)

其中，对 `ALPN` 的支持可以使用 OpenSSL 来检测：

```bash
echo | openssl s_client -alpn h2 -connect qiwihui.com:443 | grep ALPN
```

如果输出中包含 `ALPN protocol: h2`，说明服务端支持 `ALPN`，如果输出中包含 `No ALPN negotiated`，说明服务端不支持 `ALPN`。

同时，在 Chrome 的开发者工具中也可以看到协议的版本

![](/media/files/2017/02/19-qiwihui-com-chrome-http2.png)

同时还可以对 HTTP/2 进行优化，请参见[6]，不赘述了。

## 附录

附录一份 Nginx 的 http/2 简单配置

```bash
server {
        listen 443 ssl http2 default_server;
        listen [::]:443 ssl http2 default_server;

        server_name example.com www.example.com; 

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

        ssl_dhparam /path/to/your/dhparam.pem;
        ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;

        ssl_prefer_server_ciphers  on;
        add_header Strict-Transport-Security "max-age=31536000; includeSubdomains;";
        ssl_session_cache shared:SSL:5m;
        ssl_session_timeout 1h;
        
        root /path/to/your/folder/;
        index index.html;
}

server {

    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}
```

## 参考

[1]. [Supporting HTTP/2 for Google Chrome Users](https://www.nginx.com/blog/supporting-http2-google-chrome-users/)
[2]. [为什么我们应该尽快支持 ALPN？](https://imququ.com/post/enable-alpn-asap.html)
[3]. [Nginx官方教程 INSTALLING NGINX OPEN SOURCE](https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/)
[4]. [serverfault问题: Nginx configured with http2 doesn't deliver HTTP/2](http://serverfault.com/a/733556/296724)
[5]. [TLS 1.2 Cipher Suite Black List](https://http2.github.io/http2-spec/#BadCipherSuites)
[6]. [Optimizing Nginx for Best Performance](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-16-04#step-10-—-optimizing-nginx-for-best-performance)


[View on GitHub](https://github.com/qiwihui/blog/issues/22)


