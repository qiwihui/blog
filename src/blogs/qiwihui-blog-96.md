---
title: "GitHub Actions 第13天：条件"
description: "GitHub Actions 第13天：条件"
tags: 
- 技术
- 翻译
- tips
- github actions
top: 96
date: 27/03/2020, 22:57:34
author: qiwihui
update: 27/03/2020, 23:01:21
categories: 
---

昨天我们看到，当你运行工作流程时，有许多可用数据。你可以在run步骤中使用这些数据，并将其与构建脚本，部署步骤或存储库自动化一起使用。但是你也可以在工作流本身中使用它。

利用这些数据的一种有用方法是[有条件地使用它来运行工作流步骤](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idif)。

例如，你可能想在执行步骤之前检查工作流在其中运行的存储库的名称。如果你正在开发一个开源项目，这将很有帮助──因为fork你的存储库的人拥有[具有不同权限的令牌](https://qiwihui.com/qiwihui-blog-94/)，因此你可以跳过fork的发布步骤。

<!--more-->

这使fork的存储库仍可以执行连续的集成构建，并确保在运行构建和测试通过时工作流成功，并且不会由于发布步骤上的权限问题而失败。

你可以设置一个条件，以确保你位于正确的存储库上并在CI构建中运行（来自push事件）。

<script src="https://gist.github.com/ethomson/9befd0258967e0a3006295b149792c84.js"></script>

现在，当此工作流在fork中运行时，将跳过“发布文档”步骤。

![image](https://user-images.githubusercontent.com/3297411/77768483-81418880-707d-11ea-8e35-d932d5d032cf.png)

使用条件语句使你可以构建可在分支或分支之间共享的高级工作流，但其中某些步骤是针对特定触发器或环境量身定制的。

原文链接：https://www.edwardthomson.com/blog/github_actions_13_conditionals.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

