---
title: "GitHub Actions 第1天：CI/CD 触发器"
description: "GitHub Actions 第1天：CI/CD 触发器"
tags: 
- 技术
- 翻译
- tips
- github actions
top: 84
date: 20/03/2020, 18:52:25
author: qiwihui
update: 20/03/2020, 21:48:23
categories: 
---

GitHub Actions是一个独立的系统：它提供了 CI/CD 构建功能──能够构建和测试 Pull Request 并合并到你的master分支中──但它不只限于构建系统。 它已经集成到GitHub中，并且 [只要你的项目库中发生任何事件](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows)（例如正在创建发行版或正在评论问题），都可以触发并运行工作流。

我将在这个月更多地讨论那些项目库自动化方案，但是你要知道，这种灵活性将有助于理解如何进行 CI/CD 构建设置。 GitHub Actions 允许你定义一个 *触发器* 来控制工作流程的运行时间。每当你的项目库中发生与该触发器匹配的操作时，工作流运行都会进入排队队列中准备。

<!--more-->

对于 CI/CD 工作流，我喜欢使用 [push](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows#push-event-push) 和 [pull_request](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-event-pull_request) 触发器，并将其范围限定在我感兴趣的分支上。例如：

```yml
on:
  push:
    branches:
    - master
  pull_request:
    branches:
    - master
```

这个触发器将在对master分支进行任何更改时运行你的工作流──（即使它的名字是 `push` 触发器，也将在你运行 `git push` 或将 pull request 合并到 master 分支时运行）。对于针对master分支打开的任何 pull request，工作流也将运行，并且将在 pull request 中向你显示验证。

![image](https://user-images.githubusercontent.com/3297411/77157504-749cbd80-6adc-11ea-8fd5-17d745208029.png)

如果你熟悉YAML语法，就可能会注意到分支采用数组。 因此，你可以轻松地设置工作流在多个分支中运行，这在你维护单独的发布轨道追踪时非常有用。 例如：

```yml
on:
  push:
    branches:
    - master
    - 'releases/**'
  pull_request:
    branches:
    - master
    - 'releases/**'
```

每当对 `master` 分支或名称 [以 `releases/` 开头的分支](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#onpushpull_requestbranchestags) 打开 pull request 时，将运行你的工作流。

通过 `push` 和 `pull_request` 触发器，可以轻松设置 CI/CD 样式的工作流程来验证 pull request，并使用 GitHub Actions 合并到你的 master 分支中。

原文链接：https://www.edwardthomson.com/blog/github_actions_1_cicd_triggers.html


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

