# GitHub Actions 第18天：文件

当你构建执行pull request验证或持续集成构建的工作流时，你通常希望获取该构建输出并保存它，以便以后使用。有时创建一个软件包并将其发布到[GitHub packages](https://qiwihui.com/qiwihui-blog-92/)之类的软件包仓库中是有意义的 。但是有时你只想将其存储为构建输出的一部分，以后可以下载。GitHub Actions允许你将文件上传为工作流的一部分，以供日后下载。

要将文件作为构建的一部分进行上传，可以使用 [`upload-artifact`](https://github.com/actions/upload-artifact) 操作。你可以指定为其创建文件的路径–你可以指定单个文件或文件夹，以及文件的名称。你指定的路径将以你指定的工件名称存档到一个zip文件中。

<!--more-->

例如，我可以构建和测试我的项目，然后创建一个nuget包，最后将该nuget包作为文件上传。

<script src="https://gist.github.com/ethomson/5101813150c57362ee072ee696d60be7.js"></script>

现在，当我的工作流程运行时，我将在该运行的右上角获得一个选项，向我展示我的文件并让我下载它们。

![image](https://user-images.githubusercontent.com/3297411/79037750-64bd5880-7c06-11ea-8267-76a83bafe0ea.png)

将构建输出作为文件上载可以与包仓库一起使用：我喜欢将CI构建包上载到GitHub packages，并从pull request中创建工件。这使我可以选择在本地运行和测试PR验证构建──我可以将它们作为文件下载──而不会影响我的GitHub Packages帐户。如果你希望选择在本地运行，那很好，即使你很少这样做。

原文连接：https://www.edwardthomson.com/blog/github_actions_18_artifacts.html

> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

