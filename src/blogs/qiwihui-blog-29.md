# 使用 Travis CI 自动更新博客

Travis CI 自动检测代码变化，拉取，编译博客并部署到 GitHub Pages

写好博客之后，部署总会占去一段时间：编译、部署、推送和检查。手动部署多了也就烦了，一则容易出错，
比如把 master 分支用 gh-pages 分支覆盖了，二则劳动是重复的，重复的劳动就应该自动化去解决。

<!--more-->
## 最早的想法

使用 GitHub Webhooks 实现自动部署，这就需要有一台服务器，在服务器上启动服务接受 Github 的
回调，然后拉取代码，编译，将编译后的代码要么部署在同一台服务器上，要么推送到代码 gh-pages 分
支上。前者额外需要编写服务，配置博客 Nginx，可能还需要配置 HTTPS，以及对服务器进行加固，总归
就是需要额外的更多东西来支持。所以还是觉得用已经存在的线上自动化服务方便一些（其实就是懒）。

## Travis CI

持续集成（Continuous Integration，CI）的 SaaS 服务，好处不言而喻。

## 配置 Travis

```bash
gem install travis
travis login
```

```yml
language: node_js
node_js:
- 6.9.0
install:
- git submodule update --init
- npm install hexo-cli -g
- npm install
script:
- hexo clean
- hexo generate --deploy --quiet
branches:
  only:
  - master
cache:
  directories:
  - node_modules
notifications:
  email:
    recipients:
    - qwh005007@gmail.com
    on_success: change
    on_failure: always
```

## 使用 Travis 自动部署

`ERROR Deployer not found: git`

[hexo-deployer-git](https://github.com/hexojs/hexo-deployer-git)

`npm install hexo-deployer-git --save`

## 配置认证

往 Github 仓库中提交代码是需要认证的，不管是用用户密码，Access Token还是SSH key。一种方法是
直接将认证写在 `.config.yml` 中，不是说不行，是太年轻。好在 Travis CI 不仅支持[加密文件](https://docs.travis-ci.com/user/encrypting-files/)，
也支持[加密 Keys](https://docs.travis-ci.com/user/encryption-keys/)，这就为认证这一块
扫清了道路，我决定使用 OAuth 认证 Git 来提交代码到仓库中。

操作步骤：

1. 生成 Github Personal Access Token；
2. 使用 Travis CI 命令行加密 Personal Access Token；

    ```bash
    travis encrypt GH_TOKEN=<token> --add
    ```

3. 在 `.travis.yml` 中添加配置

    ```yml
    before_install:
    - git config --global push.default matching
    - git config --global user.name "qiwihui via Travis CI"
    - git config --global user.email "qwh005007@gmail.com"
    - sed -i'' "/^ *repo/s~github\.com~${GH_TOKEN}@github.com~" _config.yml
    ```

    ```yml
    env:
      global:
      - secure: IYXTVHItgbEn...
    ```

## 在 Travsi CI 中配置项目

1. Publicizing or hiding organization membership

## 自定义域名

1. qiwihui.github.io/qiwihui/ => blog.qiwihui.com
2. Enforce https

胜利完成!

## 参考

- [使用 Travis CI 自动更新 GitHub Pages](https://notes.iissnan.com/2016/publishing-github-pages-with-travis-ci/)
- [Hexo 自动部署到 Github](http://lotabout.me/2016/Hexo-Auto-Deploy-to-Github/)
- [Easier builds and deployments using Git over HTTPS and OAuth](https://blog.github.com/2012-09-21-easier-builds-and-deployments-using-git-over-https-and-oauth/)
- [Publicizing or hiding organization membership](https://help.github.com/articles/publicizing-or-hiding-organization-membership/)

