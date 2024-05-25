---
title: "GitHub Actions 第15天：在步骤之间共享数据"
description: "GitHub Actions 第15天：在步骤之间共享数据"
tags: 
- 技术
- 翻译
- tips
- github actions
top: 98
date: 29/03/2020, 22:50:28
author: qiwihui
update: 29/03/2020, 22:50:28
categories: 
---

在 GitHub Actions 的任务中，你可以有多个步骤 ，一个接一个地运行。每个步骤可能是调用一个操作（例如，[检出存储库中的代码](https://github.com/actions/checkout)或[安装特定版本的Node.js](https://github.com/actions/setup-node)），也可能是一个 `run`，仅运行你提供的脚本的步骤。

但是通常你希望与之前执行的步骤进行交互，例如，你可能希望运行一个步骤来更新软件的版本号，以使其准备好发布。然后，你可能需要在实际的发布步骤中使用该版本号。

<!--more-->

但是，如何来回获取这些数据？GitHub Actions在其自己的流程中运行你的每个步骤。这意味着你不能只在一个步骤中设置环境变量，然后在另一步骤中引用它。换句话说，这将无法正常工作：

```yml
steps:
  # 这将 **无效**。这两个 `run` 步骤被编写为
  # 作为不同的脚本并由不同的shell运行，因此
  # `FOO` 变量将不会在它们之间持久存在。
  - run: export FOO=bar
  - run: echo $FOO
```

但是，GitHub Actions 确实为你提供了将数据持久保存在执行环境中的工具。你可以通过写入标准输出（即，仅使用echo）来向GitHub Actions编写命令──包括指示 GitHub Actions 在后续运行步骤中[设置环境变量的命令](https://github.com/actions/setup-node)。

在当前shell中设置环境变量之后，可以对GitHub Actions 使用命令 `set-env` ，这将是环境变量被注入到以后的步骤中：

```yml
steps:
  # 这将会在第一个 `run` 脚本中设置 `FOO` 环境变量。
  # 然后指示 GitHub Actions 在随后的运行步骤中使其可用。
  - run: |
      export FOO=bar
      echo "::set-env name=FOO::$FOO"
  - run: echo $FOO
```

现在，实际上可以在后续步骤中获取环境变量 `FOO` 中的数据。

![image](https://user-images.githubusercontent.com/3297411/77851728-322a5d80-720d-11ea-8a61-43a2b1c99549.png)

GitHub Actions将这些步骤作为单独的脚本运行──这意味着在单独的Shell调用中运行并每次都获得原始环境。但是，使用GitHub Actions平台内的开发工具，你可以在调用之间共享数据。

原文链接：https://www.edwardthomson.com/blog/github_actions_15_sharing_data_between_steps.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

