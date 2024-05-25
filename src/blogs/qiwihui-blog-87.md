# GitHub Actions 第4天：安装工具

昨天我提到 GitHub Actions 提供了 [Linux，Windows 和 macOS 虚拟环境](https://qiwihui.com/qiwihui-blog-86/)，你可以在其中运行工作流。

但是这些环境上实际安装了什么？ 原来有[很多安装](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/software-installed-on-github-hosted-runners)。

团队试图通过许多不同的平台使我们的运行器（runners）保持最新状态。 因此，你会发现许多不同版本的Python，Ruby，.NET Core等。 但是──仅仅依靠这些各种各样的开发工具──他们不可能绝对安装所有东西。

有时你需要自己安装。而且由于你拥有一台完整的虚拟机，因此对于每项作业执行，你都可以在其上安装任何所需的软件。

<!--more-->
例如，你可能要安装非常好的“[ninja](https://ninja-build.org/)”构建工具。

### Linux

Linux虚拟环境运行Ubuntu，因此你可以使用 [apt](https://en.wikipedia.org/wiki/APT_(Package_Manager)) 安装可能需要的任何其他工具。 默认情况下，你以非 root 用户身份运行，但是可以使用无密码 sudo。这样你就可以：

```yml
run: sudo apt-get install ninja-build
```

### Windows

[Chocolatey](https://chocolatey.org/) 是 Windows 的首选软件包管理器，它已安装并可以在 GitHub Actions 虚拟环境中使用。

```yml
run: choco install ninja
```

### macOS

在 macOS 上，[Homebrew](https://brew.sh/) 是推荐的软件包管理器，可在 GitHub Actions 虚拟环境中使用。无需以 root 用户身份运行 Homebrew ──实际上，这是不合时宜的，因此您可以执行 `brew install`：

```yml
run: brew install ninja
```

### 合在一起

综上所述，如果你想在所有三个平台上安装 ninja，你的工作流程将[如下所示](https://gist.github.com/ethomson/68a7e60b9b5fbe081c8edd65237a2f22)：

<script src="https://gist.github.com/ethomson/68a7e60b9b5fbe081c8edd65237a2f22.js"></script>

原文链接：https://www.edwardthomson.com/blog/github_actions_4_installing_tools.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

