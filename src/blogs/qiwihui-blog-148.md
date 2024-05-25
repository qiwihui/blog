---
title: "CPython Internals 笔记 ── 介绍、开发环境设置"
description: "CPython Internals 笔记 ── 介绍、开发环境设置"
tags: 
- Python
- 读书笔记
- CPythonInternals
top: 148
date: 24/08/2021, 15:23:42
author: qiwihui
update: 25/08/2021, 17:37:31
categories: 
---

# 介绍

这本书将涵盖 CPython 内部实现的主要概念，并学习如何：

- 阅读和浏览源代码
- 从源代码编译 CPython
- 更改 Python 语法并将其编译到你的 CPython 版本中
- 导航并理解诸如列表、字典和生成器的概念的内部工作原理
- 掌握 CPython 的内存管理能力
- 使用并行和并发扩展你的 Python 代码
- 使用新功能修改核心类型
- 运行测试套件
- 分析和基准测试 Python 代码和运行时的性能
- 像专家一样调试 C 和 Python 代码
- 修改或升级 CPython 库的组件并将它们贡献给未来的版本

<!--more-->

## 在线资源

[CPython Internals resources](https://realpython.com/cpython-internals/resources/)

## 代码协议

遵循 [Creative Commons Public Domain (CC0) License](https://creativecommons.org/publicdomain/zero/1.0/)。

> 这书中的代码已经在 Windows 10、macOS 10.15 和 Linux 上使用 Python 3.9.0b1 进行了测试。

# 设置开发环境

CPython 源代码大约 65% 是 Python（测试是重要的部分）、24% C，其余是其他语言的混合。

## 设置 Visual Studio Code

从 [code.visualstudio.com](https://code.visualstudio.com/) 下载 Visual Studio Code，并在本地安装。

推荐的扩展：

- [C/C++(ms-vscode.cpptools)](https://github.com/Microsoft/vscode-cpptools) 提供对 C/C++ 的支持，包括 IntelliSense、调试和代码高亮。
- [Python(ms-python.python)](https://github.com/Microsoft/vscode-python) 为编辑、调试和阅读 Python 代码提供丰富的 Python 支持。
- [Restructured Text (lextudio.restructuredtext)](https://github.com/vscode-restructuredtext/vscode-restructuredtext)  为 reStructuredText（CPython 文档中使用的格式）提供丰富的支持。
- [Task Explorer (spmeesseman.vscode-taskexplorer)](https://github.com/spmeesseman/vscode-taskexplorer) 在资源管理器选项卡内添加“任务资源管理器”面板，可以更容易启动 make 任务。

### 配置任务和启动文件

VS Code 在工作区目录中创建一个文件夹 `.vscode`。 在此文件夹中，你可以创建：

- `tasks.json` 用于执行项目命令的快捷方式
- `launch.json` 用于配置调试器
- 其他特定于插件的文件

在 `.vscode` 目录中创建一个 `tasks.json` 文件，并添加以下内容：

`cpython-book-samples/11/tasks.json`：
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "windows":{
                "command": "PCBuild\build.bat",
                "args": ["-p x64 -c Debug"]
            },
            "linux":{
                "command": "make -j2 -s"
            },
            "osx":{
                "command": "make -j2 -s"
            }
        }
    ]
}
```

使用任务资源管理器插件，你将在 vscode 组中看到你配置的任务列表。

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

