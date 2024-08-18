# Cocoapods 和 Carthage 使用笔记


## Carthage 和 CoaoaPods 的区别

`CoaoaPods` 是一套整体解决方案，我们在 `Podfile` 中指定好我们需要的第三方库。然后 `CocoaPods` 就会进行下载，集成，然后修改或者创建我们项目的 `workspace` 文件，这一系列整体操作。

相比之下，`Carthage` 就要轻量很多，它也会一个叫做 `Cartfile` 描述文件，但 `Carthage` 不会对我们的项目结构进行任何修改，更不多创建 `workspace`。它只是根据我们描述文件中配置的第三方库，将他们下载到本地，然后使用 `xcodebuild` 构建成 `framework` 文件。然后由我们自己将这些库集成到项目中。`Carthage` 使用的是一种**非侵入性**的哲学。

另外 `Carthage` 除了非侵入性，它还是去中心化的，它的包管理不像 `CocoaPods` 那样，有一个中心服务器(cocoapods.org)，来管理各个包的元信息，而是依赖于每个第三方库自己的源地址，比如 Github。

<!--more-->

## Cocoapods

### 安装

1. （可选）使用 <del>taobao</del> ruby-china 源替换默认 gem 源: `gem source blabla..`

    ```bash
    $ gem sources -l
    *** CURRENT SOURCES ***
    
    https://rubygems.org/

    $ gem sources --remove https://rubygems.org/
    https://ruby.taobao.org/ removed from sources

    $ gem source -a https://gems.ruby-china.com/
    https://gems.ruby-china.com/ added to sources

    $ gem source -c
    *** Removed specs cache ***

    $ gem source -u
    source cache successfully updated

    $ gem sources -l
    *** CURRENT SOURCES ***
    
    https://gems.ruby-china.com/
    ```

2. `sudo gem install cocoapods`
3. （可选）切换 pod 源

    ```bash
    $ pod repo

    master
    - Type: git (master)
    - URL:  https://github.com/CocoaPods/Specs.git
    - Path: /Users/qiwihui/.cocoapods/repos/master
    
    $ pod repo remove master
    
    $ pod repo add master https://git.coding.net/CocoaPods/Specs.git
    
    $ pod repo update
    
    $ pod setup
    ```
    
    或者
    
    ```bash
    $ git clone https://git.coding.net/CocoaPods/Specs.git ~/.cocoapods/repos/master
    $ pod repo update
    ```
    
    切换回官方镜像
    
    ```bash
    $ pod repo remove master
    
    $ pod repo add master https://github.com/CocoaPods/Specs.git
    
    $ pod repo update
    Updating spec repo `master`
      $ /usr/local/bin/git -C /Users/qiwihui/.cocoapods/repos/master fetch origin --progress
      remote: Enumerating objects: 511, done.        
      remote: Counting objects: 100% (511/511), done.        
      remote: Compressing objects: 100% (134/134), done.        
      remote: Total 820 (delta 399), reused 449 (delta 367), pack-reused 309        
      Receiving objects: 100% (820/820), 99.24 KiB | 401.00 KiB/s, done.
      Resolving deltas: 100% (501/501), completed with 194 local objects.
      From https://github.com/CocoaPods/Specs
         5b04790953c..e3ba7ee3a29  master     -> origin/master
      $ /usr/local/bin/git -C /Users/qiwihui/.cocoapods/repos/master rev-parse --abbrev-ref HEAD
      master
      $ /usr/local/bin/git -C /Users/qiwihui/.cocoapods/repos/master reset --hard origin/master
      HEAD is now at e3ba7ee3a29 [Add] IOS_OC_BASIC 6.3
    
    CocoaPods 1.6.0.beta.2 is available.
    To update use: `sudo gem install cocoapods --pre`
    [!] This is a test version we'd love you to try.
    
    For more information, see https://blog.cocoapods.org and the CHANGELOG for this version at https://github.com/CocoaPods/CocoaPods/releases/tag/1.6.0.beta.2
    ```

4. 如果Podfile文件中有

    ```
    source 'https://github.com/CocoaPods/Specs.git'
    ```

    也需要把它换成repo的源，否则依然是使用GitHub源

### 基础用法

0. `cd <project_folder>`
1. `pod init`
2. 编辑 Podfile, example

    ```
    # 平台，必需
    platform :ios, '9.0'
    # 隐藏警告
    inhibit_all_warnings!

    target 'AlamofireDemo' do
        # Using Swift and want to use dynamic frameworks
        use_frameworks!

        # 项目 Pods
        pod 'Alamofire', '~> 4.5'

        target 'AlamofireDemoTests' do
            inherit! :search_paths
            # 测试 Pods
        end

    end
    ```
    
    版本支持：
        - `>`, `>=`, `<`, `<=`
        - `~>`: **up to** next major | minor | patch
        - `:path` 本地绝对路径
        - `:git` git项目地址，还可使用 `:branch`, `:tag`, `:commit`

3. `pod install`
4. **Always** 打开项目下 *.xcworkspace 文件作为项目入口

### pod install 和 pod update 区别

- `pod install [package_name]`: 安装特定版本的 pods
- `pod update [package_name]`: 升级 pods 到最新版本

## Carthage

### 安装

```bash
brew install carthage
```

### 使用

1. 编辑 `Cartfile`，比如 `SwiftyJSON`

    ```bash
    github "SwiftyJSON/SwiftyJSON"
    ```

2. carthage update [--platform ios]

    ```bash
    $ carthage update
    *** Fetching SwiftyJSON
    *** Checking out SwiftyJSON at "4.2.0"
    *** xcodebuild output can be found in /var/folders/kl/g94q0k_571vdjtcwzzcv20s40000gn/T/carthage-xcodebuild.nN22hg.log
    *** Building scheme "SwiftyJSON iOS" in SwiftyJSON.xcworkspace
    *** Building scheme "SwiftyJSON watchOS" in SwiftyJSON.xcworkspace
    *** Building scheme "SwiftyJSON tvOS" in SwiftyJSON.xcworkspace
    *** Building scheme "SwiftyJSON macOS" in SwiftyJSON.xcworkspace
    ```

3. `Carthage` 目录下：
    - Build(编译出来的.framework二进制代码库)
    - Checkouts(源码)
    
    ```bash
    $ tree -L 3 Carthage/
    Carthage/
    ├── Build
    │   ├── Mac
    │   │   ├── SwiftyJSON.framework
    │   │   └── SwiftyJSON.framework.dSYM
    │   ├── iOS
    │   │   ├── 22BD4B6C-0B26-35E1-AF5F-8FB6AEBFD2FD.bcsymbolmap
    │   │   ├── C862E8A1-24ED-398A-A8E9-A7384E34EDB1.bcsymbolmap
    │   │   ├── SwiftyJSON.framework
    │   │   └── SwiftyJSON.framework.dSYM
    │   ├── tvOS
    │   │   ├── 1ADB9C1F-36CA-3386-BF07-6EE29B5F8081.bcsymbolmap
    │   │   ├── SwiftyJSON.framework
    │   │   └── SwiftyJSON.framework.dSYM
    │   └── watchOS
    │       ├── A8A151AB-D15E-3A0B-8A17-BF1A39EC6AB4.bcsymbolmap
    │       ├── EA427A42-6D21-3FF4-919F-5E50BF8A5D7B.bcsymbolmap
    │       ├── SwiftyJSON.framework
    │       └── SwiftyJSON.framework.dSYM
    └── Checkouts
        └── SwiftyJSON
            ├── CHANGELOG.md
            ├── Example
            ├── LICENSE
            ├── Package.swift
            ├── README.md
            ├── Source
            ├── SwiftyJSON.podspec
            ├── SwiftyJSON.xcodeproj
            ├── SwiftyJSON.xcworkspace
            ├── Tests
            └── scripts
    ```

3. 添加生成的文件： 项目 "General" -> "Linked Frameworks and Libraries" -> 将 `Carthage/Build/iOS` 中的 `.framework` 文件添加到项目中
4. "Build Phases" -> "+" -> "New Run Script Phase"
    - /bin/sh
    - /usr/local/bin/carthage copy-frameworks
    - "Input Files": $(SRCROOT)/Carthage/Build/iOS/SwiftyJSON.framework
    - "Output Files": $(BUILT_PRODUCTS_DIR)/$(FRAMEWORKS_FOLDER_PATH)/SwiftyJSON.framework
    
    添加这个 Run Script 的作用是为了让运行时能够找到这个动态库。
    还可以将 Carthage 所集成的第三方库生成的符号文件添加到项目中，这样我们在调试的时候，就可以步入第三方库内部的代码：`Build Phrases` -> `New Copy Files Phrase`，将 Carthage/Build/iOS 目录中的 `SwiftyJSON.framework.dSYM` 符号文件拖动进来

## 参考

- [解决Cocoapods贼慢问题](https://www.jianshu.com/p/f024ca2267e3)
- [Carthage 包管理工具，另一种敏捷轻快的 iOS & MAC 开发体验](http://swiftcafe.io/2015/10/25/swift-daily-carthage-package)

[View on GitHub](https://github.com/qiwihui/blog/issues/44)


