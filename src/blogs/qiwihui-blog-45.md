# 在iOS-Swift项目中集成CppJieba分词


在垃圾短信过滤应用 `SMSFilters` 中，需要使用 `Jieba` 分词库来対短信进行分词，然后使用 `TF-IDF` 来进行处理` 分词库是 C++ 写的，这就意味着需要在Swift中集成 C++ 库。
在官方文档 "[Using Swift with Cocoa and Objective-C](https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/BuildingCocoaApps/index.html)" 中，Apple只是介绍了怎么将 Swift 代码跟 Objective-C 代码做整合，但是没有提C++，后来在官方文档中看到了这样一段话：

> You cannot import C++ code directly into Swift. Instead, create an Objective-C or C wrapper for C++ code.

也就是不能直接导入 C++ 代码，但是可以使用 Objective-C 或者 C 对 C++ 进行封装。所以项目中使用 Objective-C 做封装，然后在 Swift 中调用，下面就是这个过程的实践，Demo 代码见 [SwiftJiebaDemo](https://github.com/qiwihui/SwiftJiebaDemo)。

<!--more-->

## 整合过程

分成三步：
1. 引入C++文件；
2. 用 Objective-C 封装；
3. 在 Swift 中 调用 Objective-C；

### 引入C++文件

Demo中使用的是"结巴"中文分词的 C++ 版本 [yanyiwu/cppjieba](https://github.com/yanyiwu/cppjieba)。将其中的 `include/cppjieba` 和依赖 `limonp` 合并，并加入 `dict` 中的 `hmm_model` 和 `jiaba.dict` 作为基础数据，并暴露 `JiebaInit` 和  `JiebaCut` 接口：

```C++
//
//  Segmentor.cpp
//  iosjieba
//
//  Created by yanyiwu on 14/12/24.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#include "Segmentor.h"
#include <iostream>

using namespace cppjieba;

cppjieba::MixSegment * globalSegmentor;

void JiebaInit(const string& dictPath, const string& hmmPath, const string& userDictPath)
{
    if(globalSegmentor == NULL) {
        globalSegmentor = new MixSegment(dictPath, hmmPath, userDictPath);
    }
    cout << __FILE__ << __LINE__ << endl;
}

void JiebaCut(const string& sentence, vector<string>& words)
{
    assert(globalSegmentor);
    globalSegmentor->Cut(sentence, words);
    cout << __FILE__ << __LINE__ << endl;
    cout << words << endl;
}
```

以及

```C++
//
//  Segmentor.h
//  iosjieba
//
//  Created by yanyiwu on 14/12/24.
//  Copyright (c) 2014年 yanyiwu. All rights reserved.
//

#ifndef __iosjieba__Segmentor__
#define __iosjieba__Segmentor__

#include <stdio.h>

#include "cppjieba/MixSegment.hpp"
#include <string>
#include <vector>

extern cppjieba::MixSegment * globalSegmentor;

void JiebaInit(const std::string& dictPath, const std::string& hmmPath, const std::string& userDictPath);

void JiebaCut(const std::string& sentence, std::vector<std::string>& words);

#endif /* defined(__iosjieba__Segmentor__) */
```

目录如下：

```bash
$ tree iosjieba
iosjieba
├── Segmentor.cpp
├── Segmentor.h
├── cppjieba
│   ├── DictTrie.hpp
│   ├── FullSegment.hpp
│   ├── HMMModel.hpp
│   ├── HMMSegment.hpp
│   ├── Jieba.hpp
│   ├── KeywordExtractor.hpp
│   ├── MPSegment.hpp
│   ├── MixSegment.hpp
│   ├── PosTagger.hpp
│   ├── PreFilter.hpp
│   ├── QuerySegment.hpp
│   ├── SegmentBase.hpp
│   ├── SegmentTagged.hpp
│   ├── TextRankExtractor.hpp
│   ├── Trie.hpp
│   ├── Unicode.hpp
│   └── limonp
│       ├── ArgvContext.hpp
│       ├── BlockingQueue.hpp
│       ├── BoundedBlockingQueue.hpp
│       ├── BoundedQueue.hpp
│       ├── Closure.hpp
│       ├── Colors.hpp
│       ├── Condition.hpp
│       ├── Config.hpp
│       ├── FileLock.hpp
│       ├── ForcePublic.hpp
│       ├── LocalVector.hpp
│       ├── Logging.hpp
│       ├── Md5.hpp
│       ├── MutexLock.hpp
│       ├── NonCopyable.hpp
│       ├── StdExtension.hpp
│       ├── StringUtil.hpp
│       ├── Thread.hpp
│       └── ThreadPool.hpp
└── iosjieba.bundle
    └── dict
        ├── hmm_model.utf8
        ├── jieba.dict.small.utf8
        └── user.dict.utf8
```

接下来开始在项目中集成。首先创建一个空项目 `iOSJiebaDemo`，将 `iosjieba` 加入项目中。

单页应用             |  SwiftJiebaDemo | 添加 SwiftJiebaDemo
:-------------------------:|:-------------------------:|:-----------------:
![create-single-view-app](https://user-images.githubusercontent.com/3297411/51162445-26d16780-18d1-11e9-9385-123b8b64fbb9.png) | ![swift-jieba-demo-1](https://user-images.githubusercontent.com/3297411/51162258-8713d980-18d0-11e9-9c9e-ffec10c8d2dc.png) | ![swift-jieba-demo-2](https://user-images.githubusercontent.com/3297411/51162266-8f6c1480-18d0-11e9-922e-a5b728e85eb9.png)

添加 iosjieba:

![iosjieba-1](https://user-images.githubusercontent.com/3297411/51162030-ae1ddb80-18cf-11e9-8e2f-8692e2e7f915.png)

见代码： https://github.com/qiwihui/SwiftJiebaDemo/commit/caeb6c2f9fb005a9bc518ee67890814481676807

### C++ 到 Objective-C 封装

这个过程是将 C++ 的接口进行 Objective-C 封装，向 Swift 暴露。这个封装只暴露了 `objcJiebaInit` 和 `objcJiebaCut` 两个接口。

```Objective-C
//
//  iosjiebaWrapper.h
//  SMSFilters
//
//  Created by Qiwihui on 1/14/19.
//  Copyright © 2019 qiwihui. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface JiebaWrapper : NSObject

- (void) objcJiebaInit: (NSString *) dictPath forPath: (NSString *) hmmPath forDictPath: (NSString *) userDictPath;
- (void) objcJiebaCut: (NSString *) sentence toWords: (NSMutableArray *) words;

@end
```

```Objective-C
//
//  iosjiebaWrapper.mm
//  iOSJiebaTest
//
//  Created by Qiwihui on 1/14/19.
//  Copyright © 2019 Qiwihui. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "iosjiebaWrapper.h"
#include "Segmentor.h"

@implementation JiebaWrapper

- (void) objcJiebaInit: (NSString *) dictPath forPath: (NSString *) hmmPath forDictPath: (NSString *) userDictPath {

    const char *cDictPath = [dictPath UTF8String];
    const char *cHmmPath = [hmmPath UTF8String];
    const char *cUserDictPath = [userDictPath UTF8String];
    
    JiebaInit(cDictPath, cHmmPath, cUserDictPath);
    
}

- (void) objcJiebaCut: (NSString *) sentence toWords: (NSMutableArray *) words {
    
    const char* cSentence = [sentence UTF8String];
    
    std::vector<std::string> wordsList;
    for (int i = 0; i < [words count];i++)
    {
        wordsList.push_back(wordsList[i]);
    }
    JiebaCut(cSentence, wordsList);
    
    [words removeAllObjects];
    std::for_each(wordsList.begin(), wordsList.end(), [&words](std::string str) {
        id nsstr = [NSString stringWithUTF8String:str.c_str()];
        [words addObject:nsstr];
    });
}

@end
```

见代码： https://github.com/qiwihui/SwiftJiebaDemo/commit/7d196bb2c33280a4f419be21b47961a521618221

### Objective-C 到 Swift

在 Swift 中调用 Objecttive-C 的接口，这个在官方文档和许多博客中都有详细介绍。

1. 加入 `{project_name}-Bridging-Header.h` 头文件，即 `SwiftJiebaDemo_Bridging_Header_h`，引入之前封装的头文件，并在 `Targets -> Build Settings -> Objective-C Bridging Header` 中设置头文件路径 `SwiftJiebaDemo/SwiftJiebaDemo_Bridging_Header_h`。

```Objective-C
//
//  SwiftJiebaDemo-Bridging-Header.h
//  SwiftJiebaDemo
//
//  Created by Qiwihui on 1/15/19.
//  Copyright © 2019 Qiwihui. All rights reserved.
//

#ifndef SwiftJiebaDemo_Bridging_Header_h
#define SwiftJiebaDemo_Bridging_Header_h

#import "iosjiebaWrapper.h"

#endif /* SwiftJiebaDemo_Bridging_Header_h */
```

![bridging-header-2](https://user-images.githubusercontent.com/3297411/51162068-d60d3f00-18cf-11e9-951f-ec5c20e984dc.png)

2. 将使用到 C++ 的 Objective-C 文件修改为 Objective-C++ 文件，即 将 `.m` 改为 `.mm`: `iosjiebaWrapper.m` 改为 ` iosjiebaWrapper.mm`。

见代码：https://github.com/qiwihui/SwiftJiebaDemo/commit/94852b1357b0a0a4b2e8b92384fbdb1b16c80ed8 
### 使用

使用时需要先初始化 `Jiaba`分词，然后再进行分词。

```swift
class Classifier {

    init() {
        let dictPath = Bundle.main.resourcePath!+"/iosjieba.bundle/dict/jieba.dict.small.utf8"
        let hmmPath = Bundle.main.resourcePath!+"/iosjieba.bundle/dict/hmm_model.utf8"
        let userDictPath = Bundle.main.resourcePath!+"/iosjieba.bundle/dict/user.dict.utf8"

        JiebaWrapper().objcJiebaInit(dictPath, forPath: hmmPath, forDictPath: userDictPath);
    }

    func tokenize(_ message:String) -> [String] {
        print("tokenize...")
        let words = NSMutableArray()
        JiebaWrapper().objcJiebaCut(message, toWords: words)
        return words as! [String]
    }
}

```

控制台输出结果：

![result](https://user-images.githubusercontent.com/3297411/51162211-5a5fc200-18d0-11e9-9849-c86d2fbf683d.png)

可以看到，测试用例 `小明硕士毕业于中国科学院计算所，后在日本京都大学深造` 经过分词后为
`〔拼音〕["小明", "硕士", "毕业", "于", "中国科学院", "计算所", "，", "后", "在", "日本", "京都大学", "深造"]`，完成集成。

见代码： https://github.com/qiwihui/SwiftJiebaDemo/commit/bc42e1312dff6a9f7171cc69403136bc8a82204c

## 遇到的问题

由于自己对于编译链接原理不了解，以及是 iOS 开发初学，因此上面的这个过程中遇到了很多问题，耗时两周才解决，故将遇到的一些问题记录于此，以便日后。

0. `"cassert" file not found`

将 `.m` 改为 `.mm` 即可。

1. `compiler not finding <tr1/unordered_map>`

设置 `C++ Standard Library` 为 `LLVM libc++`

![llvm](https://user-images.githubusercontent.com/3297411/51225371-3f02be80-1985-11e9-9705-32de84b5dfad.png)

参考： [mac c++ compiler not finding <tr1/unordered_map>](https://stackoverflow.com/questions/42030598/mac-c-compiler-not-finding-tr1-unordered-map)

2. `warning: include path for stdlibc++ headers not found; pass '-std=libc++' on the command line to use the libc++ standard library instead [-Wstdlibcxx-not-found]`

`Build Setting -> C++ Standard Library -> libstdc++` 修改为 `Build Setting -> C++ Standard Library -> libc++`

3. `use of unresolved identifier`

这个问题在于向项目中加入文件时，`Target Membership` 设置不正确导致。需要将对于使用到的 Target 都勾上。

相关参考： [Understanding The "Use of Unresolved Identifier" Error In Xcode](https://learnappmaking.com/unresolved-identifier-understanding-xcode/)

## 参考

- [SwiftArchitect](https://stackoverflow.com/users/218152/swiftarchitect) 对问题 “Can I have Swift, Objective-C, C and C++ files in the same Xcode project?
” 的[回答](https://stackoverflow.com/a/32546879/3218128)
- [SwiftArchitect](https://stackoverflow.com/users/218152/swiftarchitect) 对问题 "Can I mix Swift with C++? Like the Objective - C .mm files" 的[回答](https://stackoverflow.com/a/32554229/3218128)
- [在Swift代码中整合C++类库](https://blog.voidmain.guru/2014/07/01/integrating-swift-with-c-plus-plus/)

[View on GitHub](https://github.com/qiwihui/blog/issues/45)


