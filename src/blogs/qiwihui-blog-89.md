# GitHub Actions 第6天：快速失败的矩阵工作流


因此，关于 GitHub Actions 的这些帖子甚至还不到一周，我已经写了很多有关 [矩阵工作流](https://qiwihui.com/qiwihui-blog-85/) 的文章。如你还没猜到，我是忠实粉丝。 😍

但是，如果你开始设置第一个矩阵工作流程，那么你需要注意：默认情况下，矩阵工作流程会[快速失败](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idstrategyfail-fast)。这就是说：如果矩阵扩展中的一个作业失败，则其余作业将被取消。

这种行为通常非常有益：如果你正在运行 pull request 验证构建，而矩阵中的构建之一失败，则你可能根本不在乎其余的构建是否成功。任何失败都足以表明存在使你无法合并 PR 的问题。

<!--more-->

但是，当你从头开始创建工作流时，可能需要迭代一下才能使其第一次正常工作。当作业失败是由于工作流设置中存在问题而不是代码本身存在问题时，关闭快速故障行为作为调试工具会很有帮助。

假设你有一个在 Linux 上运行良好的工作流程，并且希望使用矩阵将其扩展到可以在 macOS 和 Windows 上运行。对于简单的工作流程，这可能会正常工作。但是对于更复杂的事情，你可能需要先设置一些依赖项或安装一些工具，然后才能起作用。因此，很可能你的Linux上运行的工作流如果不做一些修改就无法在 macOS 或 Windows 上运行。

那么，当你第一次运行此新矩阵工作流时会发生什么？你的 Linux，macOS 和 Windows 作业将全部启动，并且 macOS 作业或 Windows 作业将失败，其余工作流程将被取消。

想象一下，首先失败的是 Windows 作业。你会看到的：

![image](https://user-images.githubusercontent.com/3297411/77217607-b9693880-6b5e-11ea-91df-11d70a9388f1.png)

好的，因此你决定需要修复 Windows 工作流程。 因此，你可以查看出了什么问题，更新工作流程，然后推送更改以将新构建放入队列。 但是，由于排队和调度不是很确定，因此也许这次 macOS 构建首先完成──失败。 现在，你的 Windows 运行被取消，甚至无法找出它是否有效：

![image](https://user-images.githubusercontent.com/3297411/77217652-0220f180-6b5f-11ea-99bb-0bcf357f6db1.png)

现在，在调试工作流时，可以通过设置 `fail-fast: false` 来关闭此行为：

```yml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
  fail-fast: false
```

现在，工作流不会在第一个失败的作业时被取消。它将允许 Windows 和 macOS 作业运行完成。

![image](https://user-images.githubusercontent.com/3297411/77217688-48765080-6b5f-11ea-9fad-063aecf682f5.png)

关闭 `fail-fast` 将帮助你更轻松地迭代工作流程。准备好在生产中运行时，请务必将其重新打开！这将帮助你节省CI运行时间（和金钱）。

原文链接：https://www.edwardthomson.com/blog/github_actions_6_fail_fast_matrix_workflows.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/89)


