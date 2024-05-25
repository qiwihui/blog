---
title: "GitHub Actions 第14天：矩阵条件"
description: "GitHub Actions 第14天：矩阵条件"
tags: 
- 技术
- 翻译
- tips
- github actions
top: 97
date: 27/03/2020, 23:50:47
author: qiwihui
update: 27/03/2020, 23:52:37
categories: 
---

GitHub Actions 具有许多强大的组件，但是当你开始一起使用它们时，事情就开始变得真正强大。例如：矩阵工作流使你可以轻松地将简单的工作流扩展到多个不同的作业。通过条件执行，你可以限制作业中步骤的执行。

这两个功能很自然地结合在一起──当你跨不同的操作系统，平台或语言版本构建矩阵时，可能只需要在该矩阵的一个子集上运行一些步骤。例如：在Linux上运行时，可能需要安装其他编译器，或者对于不同的操作系统，可能需要安装稍有不同的依赖项。

我可以结合一些以前的概念来为我的一个项目（C语言中的系统库）构建工作流。它将使用[跨平台](https://qiwihui.com/qiwihui-blog-86/)和[工具安装](https://qiwihui.com/qiwihui-blog-87/)的[矩阵工作流](https://qiwihui.com/qiwihui-blog-85/)来执行CI的构建和测试步骤。

<!--more-->

目标是安装Ninja构建系统，然后使用CMake创建构建脚本以利用这一优势──CMake和Ninja可以很好地协同工作，以生成快速，跨平台的本机构建。最后，我们将使用 `cmake` 进行构建，并使用 `ctest` 进行测试。

<script src="https://gist.github.com/ethomson/79c787cecee5c23f2c791500d6644583.js"></script>

运行此命令时，条件将确保仅对特定平台运行适当的“安装依赖项”步骤。其他平台的其他步骤将被跳过。

![image](https://user-images.githubusercontent.com/3297411/77774001-58bd8c80-7085-11ea-8a82-90115b7ba69f.png)

现在，我们开始了解如何将GitHub Actions的简单片段组合到更复杂，功能更强大的工作流程中。

原文链接：https://www.edwardthomson.com/blog/github_actions_14_conditionals_with_a_matrix.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

