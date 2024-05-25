# GitHub Actions 第9天：部署到GitHub Packages

本月到目前为止，我们已经研究了许多执行构建并运行一些测试的方案。这些都是很棒的工作流程──它们确保进入你的项目的pull request是高质量的，并且你的主分支是健康的。

但是，你通常想采取下一步并部署自己构建的内容。例如，你可能想构建一个容器，并在每次新的主分支合入新功能时将其上传到[GitHub Packages](https://github.com/features/packages)。这将确保你有一个可以运行并验证每个更改的容器。

为此，我们要触发向master的推送。（无论是从 `git push` 还是从合并pull request，只要[集成到master](https://www.edwardthomson.com/blog/github_actions_1_cicd_triggers.html)中，`push` 触发器都将运行。）

然后，我们将从docker登录到GitHub Packages。我们可以简单地使用GitHub Actions提供给我们的 `GITHUB_TOKEN`──令牌对我们存储库中的软件包具有发布权限。

<!--more-->

然后，我们将构建容器，并使用包注册的名称对其进行标记（在本例中是 `docker.pkg.github.com` 其后为容器的名称 `ethomson/myrepo/app`），并为其指定版本号，即Unix时间。

最后，我们[将容器推送到GitHub Packages](https://gist.github.com/ethomson/60e664ef09051cea66dada5d53c62e6d)。

<script src="https://gist.github.com/ethomson/60e664ef09051cea66dada5d53c62e6d.js"></script>

现在，我有一个简单的连续部署系统，该系统将始终使用包含来自master分支的最新版本的容器来更新GitHub Packages。

原文链接：https://www.edwardthomson.com/blog/github_actions_9_deploy_to_github_packages.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

