---
title: "学习Django──我犯的初学者错误以及如何避免"
description: "学习Django──我犯的初学者错误以及如何避免"
tags: 
- 翻译
- Python
top: 81
date: 20/01/2020, 15:04:20
author: qiwihui
update: 20/01/2020, 15:39:22
categories: 
---

> 这篇文章是 reddit 上用户 [unknownguy0518](https://www.reddit.com/user/unknownguy0518/) 发表的他在学习Django是所犯的初学者错误，以及他的一些建议。更多具体的内容可以前往对应的 [话题](https://www.reddit.com/r/django/comments/eld87j/learning_django_beginner_mistakes_i_made_that_you/) 查看。

我是 Django Web 框架的新手。我也不是专业的程序员。我没有任何人的帮助，我学到的一切都是通过反复试验而得出的。我犯了无数的错误，当我回首时，我现在笑了。在艰难学习了很多基础知识之后，我成功地创建了一个简单的网站来添加/更新/删除联系人。它已部署在 Heroku（免费服务器）中。我在这里写的内容纯属我个人观点。如果你是初学者，并且热衷于探索 Django 的世界，则应该阅读这篇文章。它可能会帮助你解决问题。

那些想浏览我的网站的人（仍然需要一些工作），它是：<https://djangophonebook.herokuapp.com>

<!--more-->

以下是我在创建自己的网站的过程中面临的主要挑战：

### 官方文档与教程

很多具有 Django 经验或其他编码经验的人都会告诉你阅读官方文档，以了解有关这个出色 Web 框架的更多信息。实际是，并非所有人都喜欢这么高的技术细节。乍一看，任何指定这样的框架内部工作的文档都会吓到新手。毫无疑问，Django 文档是非常详细并且组织得很好，但是我建议你观看一些出色的视频教程，使我们对所有可用功能以及如何在实际项目中实现这些功能有所了解。我亲自浏览了 YouTube上 “[Corey Schafer](https://www.youtube.com/user/schafer5)” 的 Django 教程。这是我在互联网上找到的最好的教程之一。还有很多其他人，但我总是回头去看他的视频。我还发现 YouTube 上 “[CodingEntrepreneurs](https://www.youtube.com/user/CodingEntrepreneurs)” 的“[尝试 Django](https://www.youtube.com/playlist?list=PLEsfXFp6DpzTD1BD1aWNxS2Ep06vIkaeW)” 系列也是一个很好的教程。一旦有了方向感，官方文档就会变得更加有意义。

### Django 版本

现在有很多针对 Django 1.x 版本的教程。尽管我们的项目很想使用相同的版本，但我强烈建议你使用 Django 的最新稳定版本（译者注：翻译时是2020年1月，最新版本为是 2.2.9）。它不仅消除了重写代码，而且还使我们能够使用旧版本可能没有的新功能。

### 使用 Git 和 GitHub

刚开始处理项目时，我忽略了使用 Git 维护版本控制。有一天，当我清除计算机中的一些旧文件夹时，我不小心删除了整个项目文件夹。这时我才意识到使用 Git 跟踪我在项目中所做的更改的重要性时。对于像我这样的新手来说，花了一段时间才弄清楚如何使用它（有时我仍在为它而苦苦挣扎），但它为我省去了很多麻烦。我还使用 GitHub 将所有代码转储为一个开源项目。你应该考虑使用 Git。如果你搞砸了并想恢复到项目的旧版本，它将对你有很大帮助。相信我，重新编写代码真的很令人沮丧。

### 使用 `.gitignore` 文件

如果使用的是 Git，请确保还使用 gitignore 文件。添加你不希望 Git 跟踪的所有文件或文件夹。有一个 GitHub 链接（<https://github.com/github/gitignore>），我参考的是 Python.gitignore 文件，并将所有内容从该文件复制粘贴到我的 gitignore 文件中。尽管某些细节不一定特定于 Django，但我将一切保持不变。它涵盖了我的用例的所有内容。我强烈建议你以此为起点。之后，你可以根据需要修改文件。

### 提升你的前端技能

是的，你将需要它。你将需要至少了解 HTML 的基础，才能在 Django 中创建模板。了解一点 CSS 和 JavaScript 会更好。它可以帮助进一步自定义网站的外观。对于前端，我是一个完全的菜鸟。我知道只有足够的 HTML 可以创建一个准系统模板，而对 CSS 的了解则很少，甚至不考虑自定义我的网站。幸运的是，对于像我这样的人，Bootstrap 可以为我们提供现成的小组件，可以在我的网站上使用。它简化了我的许多前端要求。我的项目完全基于 HTML 和 Bootstrap 构建。

### 使用虚拟环境

为你的项目创建一个单独的虚拟环境是一个好习惯。当你准备部署项目时，这也将派上用场。我艰难地了解了它的重要性。现在，我会首先创建一个虚拟环境，安装所有必需的软件包，然后在我的项目上工作。

### 使用单独的 `settings.py` 文件进行开发和生产

我没有碰到太多的教程来解释为什么在开发和生产过程中使用单独的 `settings.py` 文件是个好主意。单独的文件可减少混乱，并使代码测试效率更高。当你要进行大型项目时，请记住这一点。尽管我从未实现过它，但许多专家推荐它。

### 创建自定义用户模型

大多数教程使用内置的用户模型来存储和处理与用户相关的数据。如果你想将电子邮件ID或手机号码用作登录ID，该怎么办？如果你希望在注册时从用户那里收集自己的某些字段，例如城市，省份，性别等，该怎么办？你可以通过创建自己的自定义用户模型来做到这一点。那时你应该考虑遍历 `AbstractUser` 和 `AbstractBaseUser` 类。我通常参考两个网站── <https://simpleisbetterthancomplex.com/> 和 <https://wsvincent.com/> 来实现此目的。 YouTube 上的 CodingEntrepreneurs（<https://www.youtube.com/watch?v=HshbjK1vDtY>）在其视频之一中还介绍了创建自定义用户模型。我强烈建议你观看它，以了解其真正工作原理，而不仅仅是复制粘贴代码。

### 使用社交登录

当今大多数网站都提供了使用多种社交登录之一（例如，使用 Google 登录，使用 Facebook 登录等）登录或注册的选项。以我的个人经验，浏览我网站的大多数用户都使用了社交登录我提供的登录选项，而不是标准的注册过程。在将其付诸实践之前，在你的项目中实现它非常有意义。 “Django-Allauth” 库是一个非常好的开始，我曾经用它来实现 Google 登录。

### 设计模型

在部署项目之前，考虑一下要存储在数据库中的数据类型始终是一个好主意。哪些字段应该是必填字段，哪些字段可以是可选字段，在用户注册时要捕获的信息，所有这些都必须事先进行仔细考虑。网站上线后，对模型进行任何更改都会证明是一件非常昂贵的事情，因为我犯了这个错误。

### 基于函数的视图（FBV）与基于类的视图（CBV）

对于像我们这样的初学者来说，这始终是一个难题。根据我的经验，我发现基于通用类的视图非常容易编写，所用的代码行数少得多，并且使事情看起来更加整洁。这是我们真正可以看到所有魔术发生的地方，因为 Django 在后端为我们完成了所有繁重的工作。但是，我还发现，使用 CBV 实现任何自定义逻辑不是非常用户友好。我在互联网上也找不到太多有关如何使用和覆盖现有 CBV 方法的资料。这正是基于函数的视图蓬勃发展的地方。它们需要编写更多的代码行，解释起来可能会更复杂，但是当我们必须实现任何自定义逻辑时，它们就可能会显得很强大。了解 CBV 和 FBV 的工作原理确实有帮助。但是对于大多数用例来说，CBV 可以轻松完成工作。这是我创建视图时的首选路径。

### 路由和 URL

除了设计模型之外，在创建项目时规划所有路由也很有意义。清楚了解各种 URL 还可简化编写其相应视图的过程。很重要的一点是我们要确保各个应用程序之间的 URL 保持一致并准备进行 CRUD 操作。当编写 REST API 入口时，它也使事情变得更容易。

### 在生产环境中处理静态文件和媒体文件

很少有教程可以告诉你在尝试部署项目时将面临的一些挑战。我试图在 Heroku 上部署我的应用。当你设置 `DEBUG = False` 时，默认情况下 Django 不支持提供静态文件和媒体文件。对于静态文件，WhiteNoise 库为我完成了这项工作。它的文档也很简单。 Heroku 不存储媒体文件。我们必须使用其他服务，例如 Amazon 的 S3，并使用所有必需的参数相应地更新 `settings.py` 文件。 S3也可以用于提供静态文件，但主要缺点是它不是免费的。结果，我的网站当前无法加载用户选择的任何个人资料图片。我尚未找到替代方法。预先规划好你要如何提供媒体文件，并考虑到所涉及的成本。

### 处理不同用户的权限

这是要考虑的重要点。我面临的挑战之一是弄清楚如何为不同的用户授予或限制对特定 URL 的访问。例如，基于某些条件，用户 A 可能具有对 URL 的只读访问权限，而用户 B 可能具有对同一 URL 的写访问权限。你不希望一个用户访问另一个用户配置文件并对其进行更新。那是你需要确保为访问的 URL 授予适当权限的地方。[Corey Schafer](https://www.youtube.com/user/schafer5) 的教程对此进行了很好的介绍。

### 创建自定义中间件

涉及该主题的教程并不多。我还没有弄清楚如何创建自己的中间件。当我有更多信息时，我将更新此部分。

### 改善网站的安全性

我还没有看到太多的教程来解释 `python manage.py check -–deploy`，以及为什么它对确保我们在网站上线之前具有必要的安全性很重要。在启用网站之前，你应该探索一些东西。网站的安全性和用户数据的安全性必须受到重视。

### 保护你的管理界面

我喜欢 Django 的原因之一是因为它内置了许多安全功能。其中之一就是功能齐全的管理界面。用户访问管理页面后，他/她实际上就可以滥用数据。创建超级用户时，请确保不要使用诸如 `admin` 或 `manager` 之类的通用名称作为登录ID。另外，请确保使用很难猜到的非常强的密码。另外，将管理页面的路径更改为完全不同且难以确定的名称。避免使用默认的 `admin/` 路径。我还遇到了一个名为 `django-admin-honeypot` 的第三方库，该库通过创建类似管理员的页面来欺骗未经授权的用户，但没有执行其他任何操作。此外，它还在表中捕获了这些用户的详细信息，例如其 IP 地址和其他参数，这些表可以在实际的 Admin 界面中访问。然后，你可以决定是否要阻止他们访问你的网站或采取必要的措施。

### 保护秘密密钥和其他关键数据

使你的项目成为开放源代码的挑战之一就是要保护 `SECRET KEY` 和其他个人价值，例如你不希望世界其他地方看到的电子邮件ID和密码。我遵循 [Corey Schafer](https://www.youtube.com/user/schafer5) 在他的 YouTube 视频中提供的建议，并将所有这些重要值保存为环境变量。万一你有意或无意间发现你的秘密密钥，必须立即进行更改。你可以使用 python 自带的 `secrets` 模块（需要 Python 3.6+）来生成强密钥。同样，[Corey Schafer](https://www.youtube.com/user/schafer5) 的教程也涵盖了这一部分。

### 打造响应式网站

很少有教程着重介绍使桌面和移动设备友好的网站。最初创建网站时，它在PC上可以正常显示，但是当我尝试在移动设备上访问它时，我意识到必须重做一些模板。在创建模板时立即考虑到这一点，以后可以节省大量的工作量。我主要使用B ootstrap 作为前端，它着重于创建移动优先项目。

### 编写测试

每个应用程序都会创建一个 `tests.py` 文件。我仍然不知道如何编写测试。我观察到，GitHub上 可用于 Python 或 Django 的许多软件包或库确实进行了大量测试。同样，很少有教程解释如何编写测试。这是我仍在尝试解决的问题。当我有更多信息时，我将更新此部分。

### 使用 REST API

尽管 REST API 本身并不是一个单独的话题，但像我们这样的初学者应该知道，为什么对其进行计划很重要，如何创建 API 以及如何将其与 Angular 或 React 等其他前端集成。以我的经验，在设计视图时同时编写 REST API 确实可以使事情更高效，并且省去了尝试弄清楚权限和其他方面的麻烦。“ Django Rest Framework” 是 REST API 的首选库。我通常会创建一个单独的名为 “api” 的应用，并在此处编写所有其他应用的序列化器和视图。它将所有内容都放在一个地方。尽管我的项目有 API 入口，但我仍然必须创建一些 API。

### 在部署之前设置 `DEBUG = False`

在部署期间保留 `DEBUG = True` 是常见错误，我也犯了。在启用网站之前，请不要忘记在 `settings.py` 文件中将 `DEBUG` 值设置为 `False`。你不希望最终用户在URL引发错误时看到所有异常和其他与编码有关的信息。 [Corey Schafer](https://www.youtube.com/user/schafer5) 很好地解释了如何在他的教程中进行处理。

### 部署项目

对于像我这样的初学者来说，这是另一个真正的麻烦。我应该在哪里部署我的项目（Heroku，PythonAnywhere，DigitalOcean，AWS等）？我应该做什么准备工作？我在生产中使用哪个数据库？我需要什么所有文件来开始部署（例如 requirements.txt，procfile 等）？我应该去免费服务器还是付费服务器？很多事情要考虑。我浏览了 [Corey Schafer](https://www.youtube.com/user/schafer5) 在 YouTube 上的视频，最终将其部署在免费的 Heroku 服务器上。


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)


### Comments
