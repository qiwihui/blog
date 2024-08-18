# 在 “Deploy to Heroku” 之后手动更新Heroku应用


这个tips以RSSHub为例子。我在Heroku上部署了RSSHub用以日常RSS需求，这个已经部署很久了（2018年11月），准备更新一版，记录如下。

<!--more-->

1. 登录Heroku，按照提示进行认证并登录。

```shell
$ heroku login
```

2. 获取最新代码，这里我在RSSHub项目目录中进行了拉取（pull）：

```shell
$ cd RSSHub
$ git pull origin master
```

3. 添加Heroku中项目url，可在 `Settings` 中 `Heroku Git URL` 找到：

```shell
$ heroku git:remote -a rss-qiwihui                       
set git remote heroku to https://git.heroku.com/rss-qiwihui.git
```

4. 向Heroku推送，这时Heroku会自动进行部署，结果如下：

```shell
$ git push heroku master
Enumerating objects: 12288, done.
Counting objects: 100% (12288/12288), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3324/3324), done.
Writing objects: 100% (12288/12288), 6.32 MiB | 40.44 MiB/s, done.
Total 12288 (delta 8027), reused 12287 (delta 8026)
remote: Compressing source files... done.
remote: Building source:
remote: 
remote: -----> Node.js app detected
remote:        
remote: -----> Creating runtime environment
remote:        
remote:        NPM_CONFIG_LOGLEVEL=error
remote:        NODE_ENV=production
remote:        NODE_MODULES_CACHE=true
remote:        NODE_VERBOSE=false
remote:        
remote: -----> Installing binaries
remote:        engines.node (package.json):  >=8.0.0
remote:        engines.npm (package.json):   unspecified (use default)
remote:        engines.yarn (package.json):  unspecified (use default)
remote:        
remote:        Resolving node version >=8.0.0...
remote:        Downloading and installing node 12.1.0...
remote:        Using default npm version: 6.9.0
remote:        Resolving yarn version 1.x...
remote:        Downloading and installing yarn (1.16.0)...
remote:        Installed yarn 1.16.0
remote:        
remote: -----> Restoring cache
remote:        Cached directories were not restored due to a change in version of node, npm, yarn or stack
remote:        Module installation may take longer for this build
remote:        
remote: -----> Installing dependencies
remote:        Installing node modules (yarn.lock)
remote:        yarn install v1.16.0
remote:        [1/4] Resolving packages...
remote:        [2/4] Fetching packages...
remote:        info fsevents@1.2.8: The platform "linux" is incompatible with this module.
remote:        info "fsevents@1.2.8" is an optional dependency and failed compatibility check. Excluding it from installation.
remote:        [3/4] Linking dependencies...
remote:        [4/4] Building fresh packages...
remote:        Done in 55.40s.
remote:        
remote: -----> Build
remote:        
remote: -----> Caching build
remote:        - node_modules
remote:        
remote: -----> Pruning devDependencies
remote:        yarn install v1.16.0
remote:        [1/4] Resolving packages...
remote:        [2/4] Fetching packages...
remote:        info fsevents@1.2.8: The platform "linux" is incompatible with this module.
remote:        info "fsevents@1.2.8" is an optional dependency and failed compatibility check. Excluding it from installation.
remote:        [3/4] Linking dependencies...
remote:        [4/4] Building fresh packages...
remote:        warning Ignored scripts due to flag.
remote:        Done in 8.07s.
remote:        
remote: -----> Build succeeded!
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote: 
remote: -----> Compressing...
remote:        Done: 143.8M
remote: -----> Launching...
remote:        Released v5
remote:        https://rss-qiwihui.herokuapp.com/ deployed to Heroku
remote: 
remote: Verifying deploy... done.
To https://git.heroku.com/rss-qiwihui.git
 * [new branch]      master -> master
```

5. 设置环境变量 `HEROKU_SLUG_COMMIT`:

```shell
$ heroku config:set HEROKU_SLUG_COMMIT=$(git rev-parse --short HEAD)
Setting HEROKU_SLUG_COMMIT and restarting ⬢ rss-qiwihui... done, v8
 ▸    Warning: The "HEROKU_" namespace is protected and shouldn't be used.
HEROKU_SLUG_COMMIT: a8066bd
```

6. 验证：

前往相应的页面验证，可以看到在Debug中的 githash值已经是当前最新的hash值了。

![githash](https://user-images.githubusercontent.com/3297411/57205060-5b873d00-6fee-11e9-893f-14b2978d3b92.png)


[View on GitHub](https://github.com/qiwihui/blog/issues/69)


