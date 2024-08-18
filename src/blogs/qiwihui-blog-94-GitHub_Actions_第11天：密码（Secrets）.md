# GitHub Actions 第11天：密码（Secrets）


昨天我们建立了一个基于[改变路径](https://qiwihui.com/qiwihui-blog-93/)触发的工作流; 它的目标是发布文档。如果仔细看，在工作流程的底部，我们引用了一个变量。看起来有点像我们[引用矩阵变量](https://qiwihui.com/qiwihui-blog-85/)的方式 ，而这里引用了一个密码。

在部署场景中，你通常会需要令牌或密码之类的东西──GitHub Actions支持将这些作为密码保存在存储库中。

要设置密码，请转到“存储库设置”页面，然后选择“密码”。你的密码名称将在你的工作流中用于引用数据，你可以将密码本身放入值中。

<!--more-->

![image](https://user-images.githubusercontent.com/3297411/77734745-39523f80-7044-11ea-8aed-91f6dde277e0.png)

要使用该密码，你可以在工作流中使用上下文 `secrets` 来引用它。如果你有一个密码的名字 `SECRET_KEY`，你可以将其称为 `${{secret.SECRET_KEY}}`。

<script src="https://gist.github.com/ethomson/eb722482cfd7f955f17c3231efe8804a.js"></script>

## `GITHUB_TOKEN`

GitHub Actions会为每次运行的工作流自动在存储库中设置一个密码 `GITHUB_TOKEN`。该令牌使你可以与存储库进行交互，而无需自己创建新令牌或设置密码。

该令牌为你提供了对存储库本身，issue和[GitHub Packages](https://www.edwardthomson.com/blog/github_actions_9_deploy_to_github_packages.html)进行读写的有限访问权限。但是它不能完全访问所有内容──你无法与组织中的其他存储库一起使用，也无法发布到GitHub Pages──因此，对于某些工作流，你可能仍需要设置令牌。

## 密码安全

GitHub试图防止你的密码被窥视。在输出日志中，你定义的所有密码都会被清除，并在输出日志之前用星号替换。

![image](https://user-images.githubusercontent.com/3297411/77734893-7ddddb00-7044-11ea-93af-18ab47df2ffd.png)

这有助于保护你的密码，防止他人窥视，尤其是利用那些导出值的工具。但这当然不是完美的，你应该谨慎保护密码。

## Forks

如果你的项目使用fork来接受来自贡献者的pull request（例如，如果你正在开发一个开源项目），则可能对在工作流程中使用密码有所警惕。

GitHub明确 **禁用** 了对来自fork的工作流提供密码的功能。这意味着，当用户从fork打开对你的项目的pull request时，不会向此工作流提供任何密码。

![image](https://user-images.githubusercontent.com/3297411/77734903-86361600-7044-11ea-8475-410b7380eb83.png)

这有助于防止用户修改工作流程本身──或工作流程调用的任何脚本──试图获取你的密码副本。这些密码根本无法获得。

（`GITHUB_TOKEN`仍然为fork提供了特殊功能，以便它们可以克隆你的存储库（以便构建它），但已将其降级为只读令牌，以防止fork工作流在你的存储库中进行更改。）

原文链接：https://www.edwardthomson.com/blog/github_actions_11_secrets.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


[View on GitHub](https://github.com/qiwihui/blog/issues/94)


