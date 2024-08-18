# 如何阅读苹果开发文档


![coding-woman-5](https://user-images.githubusercontent.com/3297411/51306754-16f48780-1a79-11e9-9959-b6f94a4cae45.jpg)

原文：[How to read Apple’s developer documentation](https://www.hackingwithswift.com/articles/167/how-to-read-apples-developer-documentation)

对于很多人来说，这篇文章听起来很奇怪，因为我们已经习惯了 Apple 的 API 文档的工作方式，因此我们精神上已经经过调整以快速找到我们想要的东西。

但这是一个有趣的事实：去年我最热门的文章请求之一是帮助人们真正阅读 Apple 的代码文档。您如何找到您需要的 iOS API，如何浏览所有材料以找到您真正想要的内容，以及您如何深入了解为什么事情按照他们的方式工作？

所以，如果你曾经寻求帮助来理解 Apple 的开发者文档，首先我要让你知道你并不孤单 - 许多人都在努力解决这个问题。但其次，我希望这篇文章会有所帮助：我会尽力解释它的结构，它有什么好处（以及不好的地方），以及如何使用它。

更重要的是，我将向您展示经验丰富的开发人员寻找额外信息的位置，这些信息通常比Apple的在线文档更有价值。

<!--more-->

## “这是什么？” vs “你怎么用它？”

任何书面的 API 文档通常采用以下五种形式之一：

1. 接口代码，显示了什么是方法名称和参数，属性名称和类型，以及类似的，带有一些描述它应该做什么的文本。
2. API 的文本描述了它应该做什么以及一般指导用例。
3. 广泛使用的有用的 API 示例代码。
4. 如何使用 API 代码段。
5. 解决常见问题的简单教程：如何做 X，如何做 Y，以及如何做 Z 等等。

粗略地说，苹果公司第一点做了很多，其次是第二点和第三点，第四点很少，第五点几乎没有。

所以，如果你正在寻找“如何用 Y 做 X ”的具体例子，你最好从我的 [Swift 知识库](https://www.hackingwithswift.com/example-code)开始 - 这正是它的用途。

了解 Apple 的文档解决的问题，可以帮助您从中获得最大收益。它并不是一个结构化的教程，它不会向您介绍一系列概念来帮助您实现目标，而是作为 Apple 支持的数千个 API 的参考指南。

## 寻找一个类

Apple的在线文档位于 https://developer.apple.com/documentation/ ，虽然您能在 Xcode 中使用本地副本，但我会说大多数人使用在线版本只是因为他们可以更容易地找到内容。

绝大多数 Apple 的文档都描述了接口，而这正是大多数时候你会看到的。我想使用一个实际的例子，所以请先在您的网络浏览器中打开https://developer.apple.com/documentation/ ，这是所有Apple开发者文档的主页。

![apple-developer-documentation](https://user-images.githubusercontent.com/3297411/51331392-9f444e00-1ab4-11e9-94df-48407c8102c3.png)

您会看到所有 Apple 的 API 分为 `App Frameworks` 或 `Graphics and Games` 等类别，您已经看到了一件重要的事情：所有深蓝色文本都是可点击的，并会带您进入特定框架的API文档。是的，它使用相同的字体和大小，没有下划线，说实话，深蓝色链接和黑色文本之间没有太大区别，但你仍然需要留意这些链接 - 有很多他们，你会用它们来深入挖掘主题。

现在请从 `App Frameworks` 类别中选择 `UIKit`，您将看到它的功能（为iOS创建用户界面）的简要概述，标有“`重要`”（`Important`）的大黄色框，然后是类别列表。那些黄色的盒子确实值得关注：虽然它们经常被使用，它们几乎总能阻止你犯下根本错误，这些错误导致出现奇怪的问题。

![uikit-overview](https://user-images.githubusercontent.com/3297411/51331416-aa977980-1ab4-11e9-886a-9dc54dae0189.png)

此页面上重要的是共同描述 `UIKit` 的类别列表。这是人们经常迷路的地方：他们想要了解像 `UIImage` 这样的东西，所以他们必须仔细查看该列表以找到它可能出现的合适位置。

![uikit-topics](https://user-images.githubusercontent.com/3297411/51331432-b4b97800-1ab4-11e9-8d70-de35c34d58d4.png)

在这种情况下，您可能会查看“资源管理”（`Resource Management`），因为它的副标题“管理存储在主可执行文件之外的图像，字符串，故事板和 nib 文件”听起来很有希望。但是，您会感到失望 - 您需要向下滚动到 “图像和 PDF”（`Images and PDF`）部分才能找到 `UIImage`。

这就是为什么我谈过的大多数人只是使用自己喜欢的搜索引擎。他们输入他们关心的类，并且 - 只要它有“UI”，“SK”或类似的前缀 - 它可能是第一个结果。

不要误会我的意思：我知道这种做法并不理想。但是面对搜索一个类或者去 https://developer.apple.com/documentation/ ，选择一个框架，选择一个类别，然后选择一个类，第一个就是更快。

重要提示：无论您选择哪种方法，最终都会在同一个地方，所以只做最适合您的方法。现在，请找到并选择 `UIImage`。

## 阅读类的接口

一旦选择了您关心的类，该页面就有四个主要组件：概述，版本摘要，接口和关系。

![uiimage-overview](https://user-images.githubusercontent.com/3297411/51334152-32cc4d80-1aba-11e9-9748-3ffdab35aafc.png)

概述是“API的文本描述，描述了它应该做什么以及一般指导用例”，我之前提到过 - 我要求你选择 `UIImage`，因为它是文本描述何时运行良好的一个很好的例子。

当它是我第一次使用的类时，特别是如果它刚刚推出时，我通常会阅读概述文本。但是对于其他一切 - 我之前至少使用过一次的任何类 - 我跳过它并尝试找到我所得到的具体细节。请记住，Apple 文档确实不是一种学习工具：当您考虑到特定目的时，它最有效。

如果您不总是为所选 Apple 平台的最新版本开发，则版本摘要 - 页面右侧的侧栏 - 非常重要。在这种情况下，您将看到 `iOS 2.0 +`，`tvOS 9.0+` 和 `watchOS 2.0+`，它告诉我们何时 `UIImage` 类首次在这三个操作系统上可用，并且它仍然可用 - 如果它已被弃用（不再可用）你会看到像 `iOS 2.0-9.0` 这样的东西。

此页面上的实际内容 - 以及作为 Apple 框架中特定类的主页的所有页面 - 都列在“主题”标题下。这将列出该类支持的所有属性和方法，再次分解为使用类别：“获取图像数据”，“获取图像大小和比例”等。

![uiimage-topics](https://user-images.githubusercontent.com/3297411/51334198-44adf080-1aba-11e9-8d86-2eac5e0191d2.png)

如果您选择的类具有任何自定义初始化方法，则始终会首先显示它们。 `UIImage` 有很多自定义初始化方法，你会看到它们都被列为签名 - 只是描述它所期望的参数的部分。所以，你会看到这样的代码：

```swift
init?(named: String)
init(imageLiteralResourceName: String)
```

**提示：**如果您看到 `Objective-C` 代码，请确保将语言更改为 `Swift`。您可以在页面的右上角执行此操作，也可以在重要的 iOS 测试版引入更改时启用 API 更改选项。

![switch-swift](https://user-images.githubusercontent.com/3297411/51334211-4aa3d180-1aba-11e9-8d34-33f922b01733.png)

记住，初始化方法写成 `init?` 而不是 `init` 的是容易出错的 - 它们返回一个可选项，以便在初始化失败时它们可以返回 `nil`。

在初始化器的正下方，您有时会看到一些用于创建类的高度专业化实例的方法。这些不是 Swift 意义上的初始化器，但它们确实创建了类的实例。对于 `UIImage`，你会看到这样的事情：

```swift
class func animatedImageNamed(String, duration: TimeInterval) -> UIImage?
```

`class func` 部分意味着你将使用 `UIImage.animatedImageNamed()` 方式调用。

在初始化程序之后，事情变得有点不那么有条理：你会发现属性方法和枚举自由混合在一起。虽然您可以滚动查找您要查找的内容，但我可以认为大多数人只需要 `Cmd + F` 在页面上查找文字就可以了！

有三点需要注意：

- 嵌套类型 - 类，结构和枚举 - 与属性和方法一起列出，这需要一点时间习惯。例如，`UIImage` 包含嵌套的枚举 `ResizingMode`。
- 任何带有直线穿过的东西都是不推荐使用的。这意味着 Apple 打算在某些时候将其删除，因此您不应将其用于将来的代码，并建议开始重写任何现有代码。（在实践中，大多数API长期以来都被“弃用” - 许多许多年。）
- 一些非常复杂的类 - 例如，`UIViewController` - 会将额外的文档页面与其方法和属性混合在一起。查找它们旁边的页面图标，以及一个简单的英文标题，如“相对于安全区域定位内容”（`Positioning Content Relative to the Safe Area`）。

在页面的底部你会找到 `Relationships`，它告诉你它继承了哪个类（在这种情况下它直接来自 `NSObject`），以及它符合的所有协议。当您查看 Swift 类型时，本节更有用，其中协议关系更复杂。

## 阅读属性或方法页面

您已经选择了一个框架和类，现在是时候查看特定的属性或方法了。查找并选择此方法：

```swift
class func animatedResizableImageNamed(String, capInsets: UIEdgeInsets, resizingMode: UIImage.ResizingMode, duration: TimeInterval) -> UIImage?
```

您应该在 `Creating Specialized Image Objects` 类别中找到它。

![animatedresizableimagenamed-1](https://user-images.githubusercontent.com/3297411/51361359-6f279a00-1b0a-11e9-8126-7c3318d701f0.png)
![animatedresizableimagenamed-2](https://user-images.githubusercontent.com/3297411/51361364-72bb2100-1b0a-11e9-9099-1c3c17356ae9.png)

这不是一个复杂的方法，但它确实展示了这些页面的重要部分：

- Apple 有几种不同的方法来编写方法名称。之前的那个 - 长 `class func animatedResizableImageNamed` - 然后是方法页面标题中显示的形式（`animatedResizableImageNamed(_:capInsets:resizingMode:duration:)`），以及方法页面的声明部分中的形式。
- 正如您在版本摘要中所看到的（在右侧），此方法在 `iOS 6.0` 中引入。因此，虽然主要的 `UIImage` 类从第1天开始就已存在，但这种方法是在几年后推出的。
- 方法声明的各个部分都是可点击的，都是紫色的。但是要小心：如果你单击 `UIImage.ResizingMode`，你将去哪里取决于你是否点击了“UIImage”或“ResizingMode”。 （提示：您通常需要单击右侧的那个。）
- 您将看到每个参数含义和返回值的简要说明。
- “讨论”（`Discussion`）部分详细介绍了此方法的具体使用说明。这几乎总是 - 每个页面中最有用的部分，因为在这里您可以看到“不要调用此方法”或“小心......”
- 你可能会找到一个 `See Also` 部分，但这有点受欢迎 - 这里只是我们在上一页的方法列表。

现在，`UIImage` 是一个老类，并没有太大变化，因此它的文档处于良好状态。但是一些较新的 API - 以及许多没有像 `UIKit` 那样被喜欢的旧 API - 仍然记录不足。例如，来自 `SceneKit` 的 `SCNAnimation` 或来自 `UIKit` 的 `UITextDragPreviewRenderer`：两者都是在 iOS 11 中引入的，并且在它们发布18个月后仍然包含“无可用概述（No overview available）”作为其文档。

当你看到“没有可用的概述（No overview available）”时，你会失望，但不要放弃：让我告诉你接下来要做什么......

## 查看代码

尽管 Apple 的在线文档相当不错，但您经常会遇到“无可用概述（No overview available）”，或者您发现没有足够的信息来回答您的问题。

[康威定律（Conway's law）](https://en.wikipedia.org/wiki/Conway%27s_law)指出，设计系统的组织受制于设计，这些设计是这些组织的通信结构的副本。“也就是说，如果你以某种方式工作，你将以类似的方式设计事物。

Apple 在我们行业中的独特地位使他们以一种相当不寻常的方式工作 - 几乎可以肯定它与您自己公司的工作方式完全不同。是的，他们有 API 审核讨论，他们试图讨论API应该如何用两种语言看待，是的，他们有专门的团队来制作文档和示例代码。

但是他们获取示例代码的门槛非常高：通常需要一些非常好的东西才能拿出来，并且通过多层检查来处理法律问题。因此，虽然我可以在一小时内输入一个项目并立即将其发布为文章，但 Apple 需要花费更长的时间才能完成同样的工作 - 他们非常认真地对待他们的形象，而且非常正确。如果你曾经想过为什么文章很少出现在官方 Swift 博客上，现在你知道了！

现在，我说这一切的原因是 Apple 有一个快速使用的捷径：他们的工程师在他们的代码中留下评论的门槛似乎显着降低，这意味着你经常会在 Xcode 中找到有价值的信息。这些评论就像细小的金子（gold dust）一样：它们直接来自 Apple 的开发者，而不是他们的开发者出版（developer publications）团队，而且我对 devpubs 非常热爱，很高兴直接听到来自源头的声音。

还记得我提到过 SceneKit 的 `SCNAnimation` 在 Apple 的开发者网站上没有记录吗？好吧，让我们来看看Xcode可以向我们展示的内容：按 `Cmd + O` 打开“快速打开（Open Quickly）”菜单，确保右侧的 Swift 图标为彩色而不是空心，然后键入“SCNAnimation”。

您将看到列出的一些选项，但您正在寻找 `SCNAnimation.h` 中定义的选项。如果您不确定，选择 `YourClassName.h` 文件是您最好的选择。

无论如何，如果你打开 `SCNAnimation.h` Xcode 将显示生成的 SCNAnimation 头文件版本。它的生成是因为原始版本是Objective-C，因此 Xcode 为 Swift 进行了实时翻译 - 这就是 `Swift Quickly` 框中的彩色 Swift 徽标的含义。

现在，如果你按 `Cmd + F` 并搜索“class SCNAnimation”，你会发现：

```swift
/**
 SCNAnimation represents an animation that targets a specific key path.
 */
@available(iOS 11.0, *)
open class SCNAnimation : NSObject, SCNAnimationProtocol, NSCopying, NSSecureCoding {  
    /*!
     Initializers
     */

    /**
     Loads and returns an animation loaded from the specified URL.

     @param animationUrl The url to load.
     */
    public /*not inherited*/ init(contentsOf animationUrl: URL)
```

这只是一个开始。 是的，该类及其所有内部都有文档，包括用法说明，默认值等。 所有这一切都应该在在线文档中，但无论出于什么原因它仍然没有，所以要准备好查找代码作为一个有用的补充。

## 最后的提示

此时，您应该能够查找在线文档以获取您喜欢的任何代码，并查找头文件注释以获取额外的使用说明。

但是，在准备好面对全部 Apple 文档之前，还有两件事需要了解。

首先，您经常会遇到标记为“已归档（archived”）”，“遗留（“legacy”）”或“已退休（“retired）”的文档 - 即使对于相对较新的事物也是如此。当它真的老了，你会看到诸如“这篇文章可能不代表当前发展的最佳实践”之类的消息。下载和其他资源的链接可能不再有效。“

尽管 Apple 是世界上最大的公司之一，但 Apple 的工程和 devpubs 团队几乎没有人员 - 他们不可能在保留所有内容的同时覆盖新的 API。因此，当你看到“存档”文档或类似文件时，请运用你的判断：如果它在某个版本的 Swift 中至少你知道它最近是模糊的，但即使不是，你仍然可能会发现那里有很多有价值的信息。

其次，Apple 拥有一些特别有价值的出色文档。这些都列在 https://developer.apple.com 的页脚中，但主要是[人机界面指南](https://developer.apple.com/design/human-interface-guidelines/)。这将引导您完整地为 Apple 平台设计应用程序的所有部分，包括说明关键点的图片，并提供大量具体建议。即使这个文档是构建 iOS 应用程序时最重要的一个，但很少有开发人员似乎已经阅读过它！

## 接下来做什么？

我之前曾写过[关于 Apple 文档的问题](https://www.hackingwithswift.com/articles/42/apple-can-we-please-talk-about-your-documentation) - 我担心那里没有鼓励，但至少如果你在努力，它可能会让你觉得不那么孤单。

幸运的是，我有很多可能更有用的材料：

- 我的[Swift知识库（Swift Knowledge Base）](https://www.hackingwithswift.com/example-code)包含针对 Swift 和 iOS 开发人员的600多个问答，技巧和技术点 - 它可以帮助您更快地解决问题。
- 我的[Swift术语表（Glossary of Common Swift Terms）](https://www.hackingwithswift.com/glossary)在 Swift 开发中定义了100多个常用术语，所有术语都在一页上。
- [我有一本全书使用项目教授 Swift 和 iOS](https://www.hackingwithswift.com/read)，它专门用于在逻辑流程中引入概念。

您认为阅读Apple文档最有效的方法是什么？ 在Twitter上发送你的提示：[@twostraws](https://twitter.com/twostraws)。


[View on GitHub](https://github.com/qiwihui/blog/issues/46)


