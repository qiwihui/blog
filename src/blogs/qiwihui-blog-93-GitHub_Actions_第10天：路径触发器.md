# GitHub Actions 第10天：路径触发器


前面我们看到可以限制[基于分支过滤器的](https://qiwihui.com/qiwihui-blog-84/)工作流运行。对于由 `push` 或 `pull_request` 触发的工作流，你可以对其进行限制，以使其仅在推送到特定分支或针对特定分支打开 pull request 时才触发。

你还可以限制这些工作流，以便仅在[推送特定路径](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#onpushpull_requestpaths)时才触发它们。

<!--more-->

如果你在提交某些东西时会运行一些自动化功能，这将非常有用。例如：在我的一个开源项目中，每次将提交合并到master分支中时，我们都会将文档发布到我们的网站上。但是，我们只想在文档实际更改时运行该工作流程。

在这种情况下，我们希望docs在master分支中目录中的任何内容更改时运行。我们可以使用[通配符](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet)作为路径过滤器的一部分：

<script src="https://gist.github.com/ethomson/5244d867cb44c3d855f05094562d6dc2.js"></script>

现在，我们有了一个工作流程，只要我们对文件docs夹中的文件进行新更改并将其合并到master分支中，就可以运行脚本 `publish_docs.sh`。

原文链接：https://www.edwardthomson.com/blog/github_actions_10_path_triggers.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/93)


