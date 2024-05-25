# GitHub Actions 第2天：矩阵工作流

拥有 CI/CD 系统的最大优势之一是，它使你可以高效地构建和测试多种配置。在推送之前，你在机器上进行构建和测试当然是必要的，但这几乎是不够的。毕竟，你可能只安装了一个版本的节点。但是，在各种平台上构建将使你充满信心和洞察力，使你的更改可以在你支持的整个生态系统中发挥作用。

<!--more-->

[Mozilla Tinderbox](https://www.jwz.org/blog/2011/08/weaponized-tinderbox/) 是最早引入跨多个配置构建概念的 CI 系统之一。这是革命性的──当我使用 [AbiWord](https://www.abisource.com/) 时，我负责了 Tinderbox 的设置。我们有一个充满机器的实验室，以便我们可以测试 Motif 构建和 GTK 构建，并可以针对不同的依赖项进行测试（这是在从可怕的 libc5 到 libc6 迁移的时候），甚至是不同的 C ++ 编译器。

那时，我的工作很大一部分是维护这个装有昂贵计算机的实验室。因此，我最喜欢的 GitHub Actions 特性之一就是矩阵工作流功能也就不足为奇了，它使我能够快速运行多个构建以支持各种配置。

我仍然在编写代码，因此仍然需要使用不同的编译器和不同的依赖项进行构建。但是现在我不需要一个充满机器的实验室，我只需要在 GitHub Actions 中使用矩阵工作流设置即可。

矩阵工作流一开始可能看起来有些让人不知所措，但这实际上只是简单的变量替换。您定义了一组变量，以及应分配给每个变量的一组值。然后，GitHub Actions 将使用这些变量的所有不同扩展来执行工作流。

假设你要测试三个不同的变量，这很快变得非常强大。就我而言，我想用两个不同的 C 编译器（gcc和clang），三个不同的 SSL 后端（OpenSSL，GnuTLS和NSS）以及两个不同的 Kerberos 后端（MIT和Heimdal）进行测试。要测试所有这些不同的组合，那就是2 * 3 * 2 = 12种不同的配置。

但是，我不必定义十二个不同的工作（或更糟的是，必须像在糟糕的过去那样在实验室中设置十二个不同的机器），我只需指定一个包含三个变量的矩阵即可。如果在作业中指定矩阵，则实际上将获得十二个以不同排列运行的作业：

```yml
matrix:
  cc: [gcc, clang]
  curl: [openssl, gnutls, nss]
  kerberos: [libkrb5, heimdal]
```

现在在我的工作中，我可以使用[矩阵上下文](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/contexts-and-expression-syntax-for-github-actions)引用这些变量中的每一个。例如，`${{matrix.cc}}` 将扩展为 cc 变量的当前值。

以下是一个示例工作流，该工作流安装每个依赖项，并运行我的 autoconf 设置，然后运行 make：

<script src="https://gist.github.com/ethomson/5570201b04670fb90c1b0450db19e01a.js"></script>

当你运行此工作流程时，你可以快速查看它如何扩展到12个不同的作业。在工作流运行的左侧，你可以看到它们中的每一个。 这样，简单的工作流程就可以迅速扩展。

在其中一个运行中打开步骤时，你可以看到确实我们能够安装依赖项。 如果打开 `build (clang, openssl, libkrb5)` 任务，实际上正在运行 `clang`（由 `${CC} --version` 显示），libcurl的OpenSSL版本（由 `curl-config` 显示）和 MIT krb5（由 `krb5-config` 显示）。

![image](https://user-images.githubusercontent.com/3297411/77169169-07952200-6af4-11ea-8770-f381ddfaa7eb.png)

因此，你可以看到，你只需使用工作流中的几行矩阵定义就可以构建具有多种配置的强大工作流。

原文链接：https://www.edwardthomson.com/blog/github_actions_2_matrixes.html


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

