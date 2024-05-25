# GitHub Pages 自定义域名实践整理

这篇博客将整理在配置博客以及项目 Pages 的自定义域名过程，遇到的问题以及解决方法。[Github 的文档](https://help.github.com/articles/using-a-custom-domain-with-github-pages/)对于如何配置自定义域名有详细的介绍，这里不会全部翻译，只重点记录实践的过程，内容涉及为用户网站，公司网站，以及项目网站添加 `Apex` 域名（qiwihui.com），二级域名（www.qiwihui.com）以及开启 HTTPS。最后，所有指向 `www.qiwihui.com` 的请求将会被重定向至 `https://qiwihui.com`。

<!--more-->

## 一些注意

### Github 支持的自定义域名类型

支持的自定义域名类型 | 域名例子
-- | --
www subdomain | `www.example.com`
**one apex domain & one www subdomain** | `example.com` & `www.example.com`
apex domain | `example.com`
custom subdomain | `blog.example.com`

### GitHub Pages 站支持的域名

GitHub Pages 站类型 | 在 Github 上 Pages 的默认域名和主机地址 | 页面被如何重定向 | 自定义域名举例
-- | -- | -- | --
User Pages 站 | `username.github.io` | 自动重定向到设置的自定义域名 | `user.example.com`
Organization Pages 站 | `orgname.github.io` | 自动重定向到设置的自定义域名 | `org.example.com`
用户拥有的 Project Pages 站 | `username.github.io/projectname` | 自动重定向到 User Pages 站自定义域名的子目录（`user.example.com/projectname`） | `project.example.com`
公司拥有的 Project Pages 站 | `orgname.github.io/projectname` | 自动重定向到 Organization Pages 站自定义域名的子目录（`org.example.com/projectname`）| `project.example.com`

## 以个人 Pages 项目为例子

### 开启 Github Pages 功能

在项目 `Settings` 中，找到 `GitHub Pages` 这一区域，选择 `Source` 为对应的要部署的分支，这里我选择 `gh-pages branch`：

![gh-pages](https://user-images.githubusercontent.com/3297411/51802835-b4756580-2288-11e9-8aab-b5add026d737.png)

其中，选择 `master branch` 会视 `/README.md` 为 web 的 `index.html`，选择 `master branch /docs folder` 会视 `/docs/README.md` 为 web 的 `index.html`。

### 在项目配置中自定义域名

在 `Custom domain` 中添加自己的域名并保存：

![custom-domain](https://user-images.githubusercontent.com/3297411/51802765-141f4100-2288-11e9-8e8d-8980ed3e63b3.png)

或者，在项目分支中添加 `CNAME` 文件，`CNAME` 文件的内容为

```conf
qiwihui.com
```

这里推荐第二种，尤其对于有设置 CI 的项目，因为 CI 上将第一种设置覆盖。
这一步是比较重要却又容易忽视的一步：

- 如果添加到 GitHub Pages 中的是 `qiwihui.com`，那么 `www.qiwihui.com` 会被重定向到 `qiwihui.com`；
- 如果添加到 GitHub Pages 中的是 `www.qiwihui.com`，那么 `qiwihui.com` 会被重定向到 `www.qiwihui.com`；

这里我选择重定向到 `www.qiwihui.com`，所以设置为 `qiwihui.com`

### 添加 DNS 记录

为了能设置`Apex` 域名，需要在 DNS 中配置 A 记录指向 github 的 IP：

```conf
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

![a-record](https://user-images.githubusercontent.com/3297411/51803023-1040ee00-228b-11e9-90f7-20a4a99d9069.png)

同时，设置 `CNAME`  记录将 `www.qiwihui.com` 指向 `qiwihui.github.io`，即 `<你的 github 用户名>.github.io`。对于公司来说，这个地址是 `<公司名称>.github.io`。

![www-record](https://user-images.githubusercontent.com/3297411/51803045-539b5c80-228b-11e9-8e60-03c854f7097b.png)

### 确认 DNS 记录

以下是设置好之后的 DNS 记录情况：

```bash
$ dig +noall +answer qiwihui.com
qiwihui.com.            60      IN      A       185.199.111.153
qiwihui.com.            60      IN      A       185.199.110.153
qiwihui.com.            60      IN      A       185.199.108.153
qiwihui.com.            60      IN      A       185.199.109.153
```

```bash
$ dig www.qiwihui.com +nostats +nocomments +nocmd 

; <<>> DiG 9.10.6 <<>> www.qiwihui.com +nostats +nocomments +nocmd
;; global options: +cmd
;www.qiwihui.com.               IN      A
www.qiwihui.com.        28      IN      CNAME   qiwihui.github.io.
qiwihui.github.io.      28      IN      A       185.199.110.153
qiwihui.github.io.      28      IN      A       185.199.108.153
qiwihui.github.io.      28      IN      A       185.199.111.153
qiwihui.github.io.      28      IN      A       185.199.109.153
```

### SSL（HTTPS）配置，强烈推荐开启

勾选 `Enforce HTTPS`

![enfore_https](https://user-images.githubusercontent.com/3297411/51798435-2760eb00-224d-11e9-917c-a4942a652d35.png)

Github 会自动保持 HTTPS 证书的有效。

## 项目 Pages

当给项目设置 Pages 时，一般都已经有一个个人或者公司的 Pages 了，如果没有，就可以按以上的过程添加。如果已经设置了，则只需要很简单的两步即可：

以下以个人项目 `[qiwihui/fullstackpython.com](https://github.com/qiwihui/fullstackpython.com)`，设置地址为 `fullstackpython.qiwihui.com`

1. 在项目中开启 Github Pages，并添加 `CNAME` 文件指向 `fullstackpython.qiwihui.com`：

![fullstackpython](https://user-images.githubusercontent.com/3297411/51803267-2dc38700-228e-11e9-8ee8-03e80ec711c9.png)

2. 在 DNS 记录中添加 CNAME 记录将 `fullstackpython.qiwihui.com` 指向 `qiwihui.github.io`，即 `<你的 github 用户名>.github.io`。对于公司来说，这个地址是 `<公司名称>.github.io`。

![fullstackpython-record](https://user-images.githubusercontent.com/3297411/51803299-8004a800-228e-11e9-8721-e640e4377df1.png)

一段时间后即可。
 
## 参考

- [Using a custom domain with GitHub Pages](https://help.github.com/articles/using-a-custom-domain-with-github-pages/)
- [Custom domain redirects for GitHub Pages sites](https://help.github.com/articles/custom-domain-redirects-for-github-pages-sites/)
- [Custom domain for GitHub project pages 的回答](https://stackoverflow.com/a/9123911/3218128)
- [Custom subdomains in GitHub project pages](https://anmonteiro.com/2015/08/custom-subdomains-in-github-project-pages/)
