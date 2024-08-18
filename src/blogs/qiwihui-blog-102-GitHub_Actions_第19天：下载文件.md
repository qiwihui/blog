# GitHub Actions 第19天：下载文件


昨天，我们研究了如何在工作流运行过程中[上传文件](https://qiwihui.com/qiwihui-blog-101/)，然后手动下载它们。这在许多情况下都非常有用，但是我认为使用文件的更强大的部分是使用工件在不同步骤之间传输文件。

例如：你可能有一个项目，该项目在多个平台上创建二进制文件，将这些二进制文件作为文件上载，然后发布到最后运行作业以将这些不同的二进制文件聚合到一个程序包中。

或者，你可能想散开──拥有一个创建单个文件的作业，然后在不同平台上运行多个作业以测试该文件。

<!--more-->

在这里，我有一个测试我的本机代码的工作流程：首先，我构建本机代码测试运行器，该运行器使用 [clar](https://github.com/clar-test/clar) 单元测试框架，以便它编译一个以 `testapp` 命名的包含我所有单元测试的二进制文件。该二进制文件作为名为的文件上传 `tests`。然后，我将创建一个依赖于第一个`build` 作业的矩阵作业。它将使用最新版本的Ubuntu，Debian，CentOS和Alpine建立一个在容器内执行的矩阵。每个作业将下载 `tests` 构建作业中生成的文件，然后将设置 testapp 为可执行文件（因为文件不保留Unix权限），最后运行测试应用程序。

<script src="https://gist.github.com/ethomson/9add864c916083aaf0c0d3b0bd092351.js"></script>

当我运行它时，构建将产生一个文件，并且当该构建完成时，我的测试作业将全部开始，下载该文件，然后运行它。

![image](https://user-images.githubusercontent.com/3297411/79038436-d64bd580-7c0b-11ea-8984-e28ba788f465.png)

你可以看到，上传文件对于生成构建输出非常有用，你可以在后续构建步骤中下载和使用这些输出。

原文链接：https://www.edwardthomson.com/blog/github_actions_19_downloading_artifacts.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/102)


