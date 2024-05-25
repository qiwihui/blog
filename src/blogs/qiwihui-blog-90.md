# GitHub Actions 第7天：入门工作流程

如果你仅创建了一个或两个GitHub Actions工作流，则可能对如何起步不太关注，但是GitHub Actions团队关注如何起步，他们努力工作，以使你能尽可能轻松地开始使用Actions。

在创建新工作流程时，GitHub首先要考虑的是存储库中的代码类型。GitHub Actions使用成熟的[语言工具](https://github.com/github/linguist)来了解你的存储库包含哪种代码。这是为GitHub许多其他部分提供支持的工具，其中包括存储库主页上的语言统计栏。
<!--more-->

![image](https://user-images.githubusercontent.com/3297411/77240850-d0269280-6c25-11ea-8b6b-759de7111087.png)

对于这个拥有大量JavaScript的存储库，GitHub Actions将选择两个可能的工作流程──运行 `npm run build` 和 `npm test` 的Node.js CI/CD工作流程（这对应用程序有用），以及执行相同构建和测试运行的打包工作流程，然后将程序包发布到GitHub Packages中。

![image](https://user-images.githubusercontent.com/3297411/77240893-3ad7ce00-6c26-11ea-8335-ce18b0802ca4.png)

GitHub Actions不仅具有构建和测试项目的能力，还有工作流可以帮助你开始将应用程序部署到云中，无论是AWS，Azure还是Google Cloud。

![image](https://user-images.githubusercontent.com/3297411/77240898-504cf800-6c26-11ea-82b1-20faf590faf6.png)

而且，当然，尽管和语言学家一样好，它也不是完美的。许多人在同一存储库中混合了不同的项目，因此你还可以扩展整个启动程序工作流列表。

![image](https://user-images.githubusercontent.com/3297411/77240908-75da0180-6c26-11ea-9612-42b3c634aeb6.png)

如果你想帮助改善入门工作流程──无论是对现有工作流程进行更改，还是添加全新的语言，都可以在[GitHub上](https://github.com/actions/starter-workflows)进行提交。

原文链接：https://www.edwardthomson.com/blog/github_actions_7_starter_workflows.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

