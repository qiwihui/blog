# GitHub Actions 第17天：依赖作业

如果你设置了包含多个作业的工作流程（无论是[基于矩阵的工作流程](https://qiwihui.com/qiwihui-blog-85/)还是只是单独定义了作业），这些作业将彼此独立地并行运行。通常，这是理想的。只要有可用的计算机即可执行你的作业。

但是有时你希望能够设置依赖于其他作业的作业。例如，你可能有一些要测试的服务。但是为了节省成本，你只想在实际运行测试时运行那些服务。因此，你可能想要一个启动服务的作业，一个运行测试的工作业，然后是一个停止服务的作业。

要指定作业之间的依赖关系，可以使用 `needs` 关键字指示哪些作业依赖于其他作业的完成。

<!--more-->

<script src="https://gist.github.com/ethomson/1b52ca3b472b10a16972414f96c474fb.js"></script>

现在，这似乎不是一个很好的例子–我们可能不使用单独的作业，而可能只在一个作业中完成了这三个步骤。但是使用作业可以使我们“成长”：实际上，我们可以在一个作业中设置测试基础结构，然后并行运行多个作业以对其进行测试，然后最后运行清理作业。

![image](https://user-images.githubusercontent.com/3297411/79037364-c380d300-7c02-11ea-9bcb-682b6f1bd2b1.png)

这样一来，我们就可以在多个平台上并行运行测试作业，并通过设置将这些作业预定下来，然后停止作业。我们可以通过定义我们的安装作业，然后定义依赖于它的许多作业，然后依赖于这些作业的最终的工作。这通常称为“扇出”和“扇入”。

<script src="https://gist.github.com/ethomson/11febc97d2b41187f5cbb8ddaf9bfdce.js"></script>

通过此工作流程，我们的设置作业将运行，然后将使用矩阵在Windows，macOS和Linux上运行构建和测试作业，最后，我们将关闭启动的那些测试资源。

![image](https://user-images.githubusercontent.com/3297411/79037374-e3b09200-7c02-11ea-8618-5026cfdd9b63.png)

你可以通过相互指定作业来轻松地构建高级工作流， `needs` 以指定工作流的依赖关系图。

原文连接：https://www.edwardthomson.com/blog/github_actions_17_dependent_jobs.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

