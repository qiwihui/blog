---
title: "GitHub Actions 第20天：容器服务"
description: "GitHub Actions 第20天：容器服务"
tags: 
- 技术
- 翻译
- tips
- github actions
top: 103
date: 13/04/2020, 10:57:48
author: qiwihui
update: 13/04/2020, 10:57:48
categories: 
---

很难低估容器在DevOps实践中的重要性。通常，你会将容器部署到生产环境中──因此很自然地开始使用容器进行本地开发，并管理依赖项。我们研究了如何利用它[在容器内部](https://qiwihui.com/qiwihui-blog-88/)进行构建。但是，我们也可以使用[容器服务](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idservices)，将正在运行的容器用作构建和测试工作流程的一部分。

你通常需要运行一些与其他服务（通常是数据库）进行通信的集成测试。你可以通过编写 `docker run` 命令来拉下容器，启动容器并映射必要的端口，从而编写脚本，但这在最佳情况下很烦人。而且，如果你要[在容器中进行构建](https://qiwihui.com/qiwihui-blog-88/)，则自己运行docker会变得非常棘手。

使用容器服务可以使GitHub Actions基础架构为你执行。你只需指定容器和要映射的任何端口，它将在作业开始时启动服务容器，并使该容器可用于作业中的步骤。

```yml
services:
  redis:
    image: 'redis:latest'
    ports:
    - 6379/tcp
```

这将启动 `redis:latest` 容器并将容器中的端口6379映射到虚拟机运行程序上的端口。这等同于运行 `docker run redis:latest -p 6379/tcp`，就像你要运行该命令一样，映射到本地运行程序上的端口不是确定性的。GitHub Actions可在job.services上下文中提供此信息。

你可以查看 `${{ job.services.redis.ports[6379] }}` 以标识本地端口号。（就像运行 `docker run` 一样，你还可以指定容器端口和本地端口，例如 `6379:6379`，将容器端口6379映射到本地端口6379。）

将其放入工作流中，如果我有一个 与Redis对话的 [Node 脚本](https://github.com/actions/example-services/tree/master/redis)，并连接到 `REDIS_HOST` 环境变量所指定的Redis主机的 `REDIS_PORT	 端口，那么我可以创建一个工作流，该工作流启动Redis容器并运行Node脚本。

<script src="https://gist.github.com/ethomson/466de42a3066a4fa646240f5fa20293b.js"></script>

你可以使用服务容器来启动服务，例如 Redis， PostgreSQL 或MySQL甚至是Selenium。服务容器的执行使工作流中的这些容器的执行和交互变得更加容易。

原文链接：https://www.edwardthomson.com/blog/github_actions_20_container_services.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments

