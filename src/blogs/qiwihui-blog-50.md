# Hexo git deployer 删除了提交历史记录该怎么整？


原文：[Hexo git deployer removes commits history? Let's do something about that!](https://e.printstacktrace.blog/hexo-git-deployer-removes-commits-history-lets-do-something-about-that/)

我发现 [Hexo](https://hexo.io/) 是构建博客和应用许多知名的软件开发原则的好工具，其中之一是自动化。这就是我决定将此博客与 [Travis CI](https://travis-ci.org/wololock/wololock.github.io) 集成以执行 GitHub pages 部署的原因。但几天之后我注意到一个重要问题 - 从 CI 服务器部署新版本的博客导致从 `master` 分支中删除所有提交并从一次又一次地初始化提交开始。我花了一段时间才找到解决这个问题的工作方案。这篇博文解释了这个问题的简单解决方案。

<!--more-->
### 为什么 `hexo deploy` 会首先删除历史记录？

让我们从了解实际发生的事情开始。当你为 git 部署选项运行 `hexo deploy` [1]命令时，Hexo 会创建一个名为 `.deploy_git` 的隐藏文件夹，并将生成的文件从 `public` 文件夹复制到该文件夹。接下来，它初始化目标为 Hexo 远程部署分支的git存储库（如果它尚不存在），并从该文件夹执行 `git push --force` 到仓库和你在 `_config.yml` [2]文件中定义的分支。

清单1. 博客的部署配置

```yml
deploy:
  type: git
  repo: git@github.com:wololock/wololock.github.io.git
  branch: master
```

如果你从本地计算机构建和部署博客，并且永远不会删除（或意外丢失）你的博客源代码，你可能永远不会遇到此问题。当你从未被擦除的工作空间执行此操作时，则存在具有完整历史记录的文件夹 `.deploy_git`，并且 `hexo deploy` 仅推送实际修改的那些文件。当你迁移到像 `Travis CI` 这样的 CI 服务器时，这就变了，因为它使用干净的工作区和仓库的新克隆执行构建。在这种情况下，`.deploy_git` 文件夹根本不存在，将从头开始重新创建。

### 那么如何部署和保存历史呢？

我发现解决方案非常简单。以前我负责部署的 `.travis.yml` 文件部分看起来像这样：

清单2. 以前的 `Travis CI` 部署配置

```yml
deploy:
  skip_cleanup: true
  provider: script
  script: hexo deploy
  on:
    branch: develop
```

只要我将更改推送到 `develop` 分支，它就会触发 `hexo deploy`。在这种情况下，它最终创建了一个新的 `.deploy_git` 文件夹并强制将初始提交推送到 GitHub 仓库。然后，我做了一个小改进 - 我创建了一个简短的 bash 脚本。

清单3. 部署博客使用的脚本

```yml
#!/bin/bash

# 使用已部署文件初始化目标
git clone --depth 1 --branch=master https://github.com/wololock/wololock.github.io.git .deploy_git

cd .deploy_git

＃从 ../public/ 复制之前删除所有文件
# 这样 git 可以跟踪上次提交中删除的文件
find . -path ./.git -prune -o -exec rm -rf {} \; 2> /dev/null

cd ../

# 部署
hexo clean
hexo deploy
```

这个脚本完全按照它在注释中所说的那样做：

- 它将 `master` 分支从远程存储库克隆到 `.deploy_git` 以获取现有提交历史记录。
- 然后它从 `.deploy_git` 中删除所有非 git 对象存储库文件，因此从 `public` 文件夹复制文件将跟踪已删除的文件。
- 最后 - 它执行常规部署的 `hexo deploy` 命令。

最后，这是在引入部署bash脚本后的部署配置部分：

清单4. 当前的 `Travis CI` 部署配置

```yml
deploy:
  skip_cleanup: true
  provider: script
  script: sh deploy.sh
  on:
    branch: develop
```

由于这个解决方案，我能够保留站点更新的历史记录，并跟踪使用给定站点更新实际修改的文件的更改。

![github hexo history](https://e.printstacktrace.blog/images/github-hexo-history.png)

### 最后的话

我希望你发现这篇文章很有用。它描述了 Hexo + Travis CI + GitHub 用例的解决方案，但它可以解决从 CI 服务器环境运行时其他类似静态站点生成器可能遇到的问题。

### 参考

1. Documentation: https://hexo.io/docs/deployment
2. https://github.com/wololock/wololock.github.io/blob/develop/_config.yml#L88-L93


[View on GitHub](https://github.com/qiwihui/blog/issues/50)


