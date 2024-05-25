# GitHub Actions 第3天：跨平台构建

GitHub Actions 的优点之一是它不仅支持在 Linux 主机上或在容器中运行构建。GitHub 当然提供了Linux虚拟机，但是它们也提供了[运行 Windows 和 macOS](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/virtual-environments-for-github-hosted-runners) 的虚拟机。

macOS 虚拟环境尤其重要，因为即使作为开发人员，也不能在虚拟机上运行 macOS，除非你在 Apple 硬件上运行它。因此，如果你要构建跨平台应用程序，则可能会限制你在本地构建和测试自己的应用程序的方式。

<!--more-->

要指定主机类型，请使用作业的 `runs-on` 参数进行指示。 例如，`runs-on: macos-latest` 将在 macOS 上运行，`runs-on: windows-latest` 将毫不奇怪在 Windows 上运行。 因此，如果要通过在 Linux，macOS 和 Windows 三个平台上运行 `make` 来构建应用程序：，则可以将每个平台指定为一个单独的作业。 这是一个[例子](https://gist.github.com/ethomson/54e3832bcb391edb752169b370716854)：

<script src="https://gist.github.com/ethomson/54e3832bcb391edb752169b370716854.js"></script>

但这重复了很多……如果你阅读了昨天有关 [矩阵工作流](https://qiwihui.com/qiwihui-blog-85/) 的文章，你可能还记得我说过矩阵扩展实际上只是简单的变量替换。好吧，即使在运行参数中也是如此。

这意味着你可以使用矩阵来建立跨平台构建，其中只需几行[工作流定义](https://gist.github.com/ethomson/ee209ef3bad14996d43d0ccf22563bd1)即可：

<script src="https://gist.github.com/ethomson/ee209ef3bad14996d43d0ccf22563bd1.js"></script>

因此，你可以选择：可以使用要在其上运行的虚拟环境指定每个单独的作业，或者，如果有共同的步骤，则可以使用矩阵来运行。

原文链接：https://www.edwardthomson.com/blog/github_actions_3_crossplatform_builds.html


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

