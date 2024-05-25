# GitHub Actions 第5天：在容器中构建

昨天我讨论了如何 [在GitHub Actions虚拟环境上安装工具和依赖项](https://qiwihui.com/qiwihui-blog-87/)。 但是，如果你需要更多控制权怎么办？ 或者，如果你根本不想在 Ubuntu 上运行，该怎么办？ 这是容器发光的地方。

通过创建一个包含所有需要的开发工具以及项目依赖项的容器，你不必操心在工作流运行开始时就对那些设置和安装步骤进行管理。

此外，你还将获得基于容器的开发的优势：你可以在用于CI构建的同一个容器中进行本地构建，因此你可以高度自信地确保 GitHub Actions 中的构建与构建时所看到的与本地匹配。

语法非常简单明了──我不需要自己运行任何 `docker pull` 或 `docker run` 命令。 GitHub Actions 为我解决了这个问题。要获取源代码并在 `node：current` 容器中运行测试，请执行以下操作：

<!--more-->

<script src="https://gist.github.com/ethomson/d56f1804295ee1a4779a0d013ec4572b.js"></script>

当我运行此工作流时，GitHub Actions 将从 DockerHub 下载我指定的容器，启动它，然后直接在该容器中执行我指定的运行步骤。

> 请注意，在容器内运行时，仍然需要指定运行对象。这是因为 Linux 和 Windows 都支持容器──因此，如果你要运行基于 Linux 的容器，则需要 `runs-on: ubuntu-latest`。 如果要使用基于Windows的容器，请确保设置 `runs-on: windows-latest`。

容器还可以帮助扩展构建矩阵：如果要跨多个 Linux 发行版构建和测试工具，则甚至可以在矩阵中设置容器作业。（因为 [矩阵工作流实际上只是可变的替代](https://www.edwardthomson.com/blog/github_actions_2_matrixes.html)。）

例如，要在 Debian，Ubuntu 和 CentOS 的旧版和最新版本上构建：

<script src="https://gist.github.com/ethomson/46a2db40d5c1d320fcc79886320f375e.js"></script>

因此，无论你是要直接在我们提供的虚拟环境中还是在你指定的容器中构建，你都可以灵活地选择工作流的运行位置。

原文链接：https://www.edwardthomson.com/blog/github_actions_5_building_in_containers.html


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

