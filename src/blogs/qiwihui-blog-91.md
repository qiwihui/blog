# GitHub Actions 第8天：处理过时的 issue

存储库中存在过时的issue可能是一个很大的危害。如果你有数年不打算解决的issue，那么就很难找到要关注的重要问题。你永远不会合并的pull request使你看起来好像在忽略该项目。项目中的所有这些杂项都增加了无形的认知负担。

<!--more-->

在服务行业工作的任何人都会理解此问题。这就像一个厨师的 *场面调度连接* 的地方──在他们与他们的配料厨房的设置。

> 如果让你的现场发生故障，变脏和混乱，你会很快发现自己旋转到位并需要备份。我和一位厨师一起工作，他曾经在匆忙中走到排队的肮脏厨师的工作台旁，解释为什么违规的厨师落后了。他将手掌压在切菜板上，切菜板上撒满了胡椒粒，飞溅的酱汁，一些香菜，面包屑以及通常会漂浮在工作台上的漂浮物和抛弃物，如果不时常用潮湿的侧毛巾将其擦掉。“你看到了吗？” 他打了个招呼，抬起他的手掌，这样厨师就可以看到灰尘和碎屑粘在厨师的手掌上。“那就是你现在的脑袋。”
> 
> Anthony Bourdain，厨房机密

当GitHub着手创建Actions平台时，他们希望构建一些对CI/CD工作流程非常有用的东西──构建项目，运行测试并部署它──但这也可以帮助你自动化项目中的常见任务。在这种情况下，请保持存储库的美观和整洁。

[启动程序工作流程](https://qiwihui.com/qiwihui-blog-90/)的底部是关闭陈旧issue和 pull request 的工作流程。

![image](https://user-images.githubusercontent.com/3297411/77284675-3258c380-6d0a-11ea-9be3-0b06abf407f8.png)

它会按计划触发运行，因此在每天UTC午夜：

```yml
on:
  schedule:
  - cron: "0 0 * * *"
```

当它运行时，它将运行[过时的操作](https://github.com/actions/stale)，该操作将查看存储库中的issue和pull request，并找到几个月没有执行任何操作的请求。然后它将在问题中发布一条消息，并添加一个标签，指示该问题是过时的。如果该问题再保持一周的陈旧状态，则将其关闭。

![image](https://user-images.githubusercontent.com/3297411/77284876-b6ab4680-6d0a-11ea-99cf-dd4aa447a612.png)

这样可以确保识别出每一个过时的issue，但同时也给人们足够的时间告诉过时的操作以使issue或pull request保持打开状态──许多这些旧issue和PR毕竟具有价值！

最终，处理过时issue的的工作流程是减少存储库中某些干扰并允许你“工作干净”的简便方法。

原文链接：https://www.edwardthomson.com/blog/github_actions_8_stale_issues_and_pull_requests.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

