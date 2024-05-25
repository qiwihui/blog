---
title: "GitHub Actions 第12天：有关工作流程的信息"
description: "GitHub Actions 第12天：有关工作流程的信息"
tags: 
- 技术
- 翻译
- tips
- github actions
top: 95
date: 27/03/2020, 16:30:15
author: qiwihui
update: 27/03/2020, 16:41:57
categories: 
---

昨天我们看到GitHub为GitHub Actions工作流运行提供了一些信息，即 `GITHUB_TOKEN`。但这还不是全部。GitHub Actions还为你提供什么其他信息？

其实很多！

GitHub Actions [设置了许多信息“上下文”](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/contexts-and-expression-syntax-for-github-actions#github-context)，其中包含有关你的工作流程运行的数据。例如，github 上下文包含信息，例如你的工作流在其中运行的存储库的名称 `github.repository`，启动工作流的用户 `github.actor`。你可以使用与 [处理矩阵](https://qiwihui.com/qiwihui-blog-85/) 和 [密码](https://qiwihui.com/qiwihui-blog-94/) 相同的双弯括号扩展语法来引用它们。

<!--more-->

<script src="https://gist.github.com/ethomson/ef9e54a1dbef5dfa240833b9b6cc6e7e.js"></script>

![image](https://user-images.githubusercontent.com/3297411/77735916-58ea6780-7046-11ea-851f-1d015a832fce.png)

如果你想在上下文中查看GitHub Actions提供的所有信息，则可以实际使用方便的 `toJson` 函数来输出整个对象：

<script src="https://gist.github.com/ethomson/fd59328c86a28792a13c553784ce54fb.js"></script>

![image](https://user-images.githubusercontent.com/3297411/77735932-6142a280-7046-11ea-80c6-2f1e979b2888.png)

如果这样做，你会注意到GitHub上下文中有很多信息。特别是，`github.event` 对象本身就是一块巨大的json数据。它基本上包含与触发器相对应的 [Webhook 信息](https://developer.github.com/v3/activity/events/types/#pushevent)。

相同的事件信息已保存到磁盘上的 `github.event_path`。因此，你可以通过检查json blob来获取工作流程中的所有信息。幸运的是，非常方便的 [jq](https://stedolan.github.io/jq/) 工具已安装在 runner 上。你可以使用它在命令行上分解json数据。

例如，如果我想获取存储库中的星标数量和fork数量，则可以 `jq` 用来解压缩保存在的json数据 `github.event_path`。

<script src="https://gist.github.com/ethomson/d1756c60ada050a30f86da44bf1e5f29.js"></script>

![image](https://user-images.githubusercontent.com/3297411/77735957-6c95ce00-7046-11ea-9c5d-eeafe7628594.png)

GitHub Actions提供了大量有关存储库，触发运行的操作以及环境的数据，所有这些使你能够创建工作流以构建应用程序，部署应用程序或自动执行存储库中的某些任务。

原文链接：https://www.edwardthomson.com/blog/github_actions_12_information_about_your_workflow.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

