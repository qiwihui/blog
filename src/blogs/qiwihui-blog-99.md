# GitHub Actions 第16天：共享数据的条件

昨天，我们研究了如何在工作流步骤之一中[设置自定义数据](https://qiwihui.com/qiwihui-blog-98/)，以便在后续步骤中使用。我们通过向[env上下文](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/contexts-and-expression-syntax-for-github-actions#contexts)添加数据来做到这一点，它是一个你可以读写的属性包。

但是你不必将自己局限于仅在你的步骤中使用 `env` 上下文。你还可以在工作流本身中使用 `env` 上下文，并根据在先前步骤中设置的数据来[设置条件](https://qiwihui.com/qiwihui-blog-96/)。

例如，你可能有一个每天要运行的工作流，并且你希望对该工作流在星期一的运行方式进行较小的修改。你可以使用 [`schedule` 触发器](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#onschedule)每天运行工作流程。你可以复制该工作流程，并添加只希望在星期一运行的特殊更改。但是，呵呵，维持两个相似但只有一点点不同的工作流程是一个严重的难题。

<!--more-->

取而代之的是，你可以查看星期几并在此基础上设置一个环境变量──在这里，我将使用bash语法运行 `date` 命令以打印缩写的星期几，并将其放入我的 `echo` 语句中，将 `DAY_OF_WEEK` 在我们的 `env` 上下文中设置变量 。然后，我将其 `env.DAY_OF_WEEK` 作为后续步骤的条件。

<script src="https://gist.github.com/ethomson/c241fcd622172139ccaae0ab8088c75c.js"></script>

使用此配置，我将每天在世界标准时间05:00运行工作流。与今天一样，在星期一，将运行仅星期一的步骤。

![image](https://user-images.githubusercontent.com/3297411/77852191-d8776280-720f-11ea-99f0-a50f64ceabd6.png)

但是在本周的剩余时间里，该步骤将被跳过。

![image](https://user-images.githubusercontent.com/3297411/77852197-dca38000-720f-11ea-8aa0-9ccfab150f3a.png)

这是另一个很好的例子，说明GitHub Actions如何为你提供简单的原语，你可以将它们组合在一起以创建功能强大的工作流。

原文链接：https://www.edwardthomson.com/blog/github_actions_16_conditionals_with_shared_data.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

