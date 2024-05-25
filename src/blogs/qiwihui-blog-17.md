# 使用Nginx，supervisor在DigitalOcean中部署tornado项目

一直在想把微信的公众号的文章导出为RSS阅读，方便阅读和减少对微信的依赖，后来看到 
[zhu327/rss](https://github.com/zhu327/rss) 这个项目，这是一个用来生成微博，微信公众号，知乎日报 RSS 的Web APP。
但是这个项目的demo部署在Red Hat的openshift上，
囿于对这个cloud的操作不是很熟，所以想着把这个项目重新部署到自己在DigitalOcean的机器上，就fork了这个项目开始啦！
<!--more-->

以下涉及到的内容有：

 - Linux创建用户和修改用户组
 - git hooks实现自动部署
 - tornado项目的基本框架结构
 - supervisor管理进程
 - Nginx配置HTTP服务代理
 - DNS的记录添加

## 基本服务器设置

因为之前并没有在我的服务器上创建过其他用户，如果直接用root用户的话不好，所以需要专门的一个账户来负责部署。

0. 登陆服务器：`ssh root@<server-ip>`
1. 创建一个用户`deploy`: `sudo adduser deploy`
2. 将用户加入sudoers中: `sudo usermod -a -G sudo deploy`
3. 添加远程连接的权限，这样就省去了输入密码了：

    ```
    sudo su - deploy
    mkdir .ssh
    chmod 700 .ssh
    touch .ssh/authorized_keys
    chmod 600 .ssh/authorized_keys
    ```

    其中，`700`表示只有文件拥有者才能读，写以及打开文件，`600`表示只能读和写。
4. 接着将自己的公钥加入`authorized_keys`文件中，这个公钥在自己本机`~.ssh/id_rsa.pub`中。没有的话可以用
`ssh-keygen -t rsa -C "qwh005007@gmail.com"`来生成。

## 创建使用git hooks的自动部署

自动部署的好处就是省去了每次都要上服务器。可以参见之前的一篇博客
[使用 Git Hooks 实现项目自动部署](http://daozhang.info/deploy-projects-with-git-hooks/) 来创建这个远程的git server。

这里，我们要先fork [zhu327/rss](https://github.com/zhu327/rss) 这个项目，然后用`git clone --bare rss rss.git`生成原来
项目的裸仓库，然后将其复制到服务器上。我使用的是`~/remoteRepo/rss.git`做为git server，`~/deployment/rss`做为真正
生产的代码文件目录。

其中，git hooks中的`post-receive`文件的内容为

```
#!/bin/sh
# Check the remote git repository whether it is bare
IS_BARE=$(git rev-parse --is-bare-repository)
if [ -z "$IS_BARE" ]; then
echo >&2 "fatal: post-receive: IS_NOT_BARE"
exit 1
fi

unset GIT_DIR
# current user is git
DeployPath=/home/deploy/deployment/rss
if [ ! -d $DeployPath ] ; then
echo >&2 "fatal: post-receive: DEPLOY_DIR_NOT_EXIST: \"$DeployPath\""
exit 1
fi

cd $DeployPath
git add . -A && git stash
git pull origin master
```

## 修改源代码

[zhu327/rss](https://github.com/zhu327/rss) 项目的部署在openshift，为了将其部署在自己服务器上，修改
是必须的。

 - 删除了项目中的openshift hooks部分
 - 将其中用到openshift环境变量`OPENSHIFT_DIY_IP`和`OPENSHIFT_DIY_PORT`修改为对应的`localhost`和`8000`端口
 - 将`diy/templates/`中的`https://diy-devz.rhcloud.com`修改为之后要用到的地址 `http://rss.daozhang.info`
 - 然后将修改好的代码在本地的virtualenv环境中测试，并生成需要的python的模块文件`requirement.txt`。如下：

    ```
    Jinja2==2.7.3
    MarkupSafe==0.23
    backports.ssl-match-hostname==3.4.0.2
    certifi==2015.04.28
    lxml==3.4.4
    python-dateutil==2.4.2
    python-memcached==1.54
    six==1.9.0
    tornado==4.2
    wsgiref==0.1.2
    ```

这些都好了之后就可以将本地的文件第一次push到服务器上了。因为之前已经设置好了git hook，所以可以在服务器上的
`deployment/rss`看到项目的代码更新了。

## 使用supervisor管理进程

`supervisor`是Linux中非常好用的进程管理工具，我们将使用它和Nginx一起来组成我们的服务的部署。

1. 安装supervisor：`pip install supervisor` 或者 `sudo apt-get install supervisor`
2. 创建一个目录来装supervisor的配置文件：`mkdir -p ~/local/etc/supervisord`
3. 创建superviosr的出要的配置文件：`touch ~/local/etc/supervisord.conf`，并加入如下内容：

   ```
    [unix_http_server]
    file=/home/deploy/tmp/supervisor.sock
     
    [supervisord]
    user=deploy
    logfile=/home/deploy/logs/user/supervisord.log
    logfile_maxbytes=50MB
    logfile_backups=10 
    loglevel=info
    pidfile=/home/deploy/local/run/supervisord.pid supervisord.pid)
     
    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
     
    [supervisorctl]
    serverurl=unix:///home/deploy/tmp/supervisor.sock
     
    [include]
    files = /home/deploy/local/etc/supervisord/*.ini
    ```

    其中我们都适用用户目录下创建的`local`，`logs`和`tmp`文件夹来装这些文件。
4. 创建一个rss.ini的文件用来作为rss服务：`touch ~/local/etc/supervisord/rss.ini`，放入如下内容：

    ```
    [program:rss]
    command=python2.7 /home/deploy/deployment/rss/diy/start.py
    ```

    其中，`start.py`是这个tornado项目的入口。

5. 启动服务：`supervisord -c /home/deploy/local/etc/supervisord.conf`，因为用的是非默认的配置文件，这里
指定相应的配置文件位置。

6. 一旦我们在之后修改了项目push了之后，我们需要重新启动rss：`supervisorctl restart rss`，因此，为了方便，
可以将这条命令加入项目git hooks中的`post-receive`文件末尾。

## 配置Nginx

Nginx很好很强大，我们用它来做为我们的HTTP服务器。

1. 安装Nginx，这里，我们适用从源代码安装Nginx，并配置一些log，pid等的目录到deploy的用户目录下，这里，写
一个安装的脚本`install.sh`：

    ```
    mkdir -p ~/src
    mkdir -p ~/tmp/nginx/fcgi ~/tmp/nginx/proxy ~/tmp/nginx/client
    
    cd ~/src
    curl -O  http://nginx.org/download/nginx-1.2.1.tar.gz
    tar -xzvf nginx-1.2.1.tar.gz
    cd nginx-1.2.1
    
    ./configure   --prefix=$HOME/local/nginx  \
    --sbin-path=$HOME/local/sbin/nginx \
    --conf-path=$HOME/local/etc/nginx.conf  \
    --error-log-path=$HOME/logs/user/nginx/error.log \
    --http-log-path=$HOME/logs/user/nginx/access.log \
    --pid-path=$HOME/local/run/nginx/nginx.pid \
    --lock-path=$HOME/local/lock/nginx.lock \
    --http-client-body-temp-path=$HOME/tmp/nginx/client/ \
    --http-proxy-temp-path=$HOME/tmp/nginx/proxy/  \
    --http-fastcgi-temp-path=$HOME/tmp/nginx/fcgi/ \
    --with-http_flv_module \
    --with-http_ssl_module \
    --with-http_gzip_static_module
    
    make && make install
    ```

    在Nginx的安装过程中会列出这些配置信息：

    ```
    Configuration summary
      + using system PCRE library
      + using system OpenSSL library
      + md5: using OpenSSL library
      + sha1: using OpenSSL library
      + using system zlib library
    
      nginx path prefix: "/home/deploy/local/nginx"
      nginx binary file: "/home/deploy/local/sbin/nginx"
      nginx configuration prefix: "/home/deploy/local/etc"
      nginx configuration file: "/home/deploy/local/etc/nginx.conf"
      nginx pid file: "/home/deploy/local/run/nginx/nginx.pid"
      nginx error log file: "/home/deploy/logs/user/nginx/error.log"
      nginx http access log file: "/home/deploy/logs/user/nginx/access.log"
      nginx http client request body temporary files: "/home/deploy/tmp/nginx/client/"
      nginx http proxy temporary files: "/home/deploy/tmp/nginx/proxy/"
      nginx http fastcgi temporary files: "/home/deploy/tmp/nginx/fcgi/"
      nginx http uwsgi temporary files: "uwsgi_temp"
      nginx http scgi temporary files: "scgi_temp"
    ```

2. 添加路径到PATH中： 

    ```
    export PATH=/home/you/local/sbin:$PATH
    source ~/.bashrc
    ```

3. 创建配置文件：`~/local/etc/nginx.conf`，在其中添加我们服务的配置：

    ```
    #user  deploy;
    worker_processes  1;
    
    error_log /home/deploy/logs/user/nginx/error.log;
    pid /home/deploy/local/run/nginx/nginx.pid;
    
    events {
        worker_connections  1024;
    }
    
    http {
        upstream rsstornado {
            server 127.0.0.1:8000;
        }
        include       mime.types;
        default_type  application/octet-stream;
    
        access_log /home/deploy/logs/user/nginx/access.log;
    
        keepalive_timeout 65;
        proxy_read_timeout 200;
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        gzip on;
        gzip_min_length 1000;
        gzip_proxied any;
        # Relevant docs: http://wiki.nginx.org/HttpGzipModule#gzip_types
        # Enables compression for additional MIME-types besides "text/html".
        # "text/html" is always compressed.
        gzip_types text/plain text/css text/xml
                   application/x-javascript application/xml
                   application/atom+xml text/javascript;
    
        # Only retry if there was a communication error, not a timeout
        # on the Tornado server (to avoid propagating "queries of death"
        # to all frontends)
        proxy_next_upstream error;
    
        server {
            listen       80;
            # server_name  localhost;
            # Allow file uploads
            client_max_body_size 50M;
    
            location / {
                proxy_pass_header Server;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_pass http://rsstornado;
            }
    
        }
    }
    ```

    其中，`upstream rsstornado`指向了我们的rss的端口。

4. 之后使用`/home/deploy/local/sbin/nginx -t`来检查这些配置，期望的输出为：

    ```
    nginx: the configuration file /home/deploy/local/etc/nginx.conf syntax is ok
    nginx: configuration file /home/deploy/local/etc/nginx.conf test is successful
    ```

5. 运行服务：`/home/deploy/local/sbin/nginx`

如果一切顺利，这时，我们在浏览器中输入服务器对应的ip时就可以看到这个web app了。

## 添加`A`纪录

最后的话需要在自己的dns服务商中添加一条指向服务器ip的`A`距离，例如在 [he.net](http://dns.he.net) 中添加
一条`A`记录即可。很快，就可以直接使用 <http://rss.daozhang.info> 访问这个app了。

## 最后

这样，我们就完成了这个server的配置。在我部署这个server的过程中，微信对应的RSS生成的解析实效了，
我觉得是因为sogou在其url中添加了一个序列，这个序列是有AES算法得出来的，并且一段时间会换一个key来
生成这个序列，所以我暂时也不知道怎么处理这个，有待进一步研究。

