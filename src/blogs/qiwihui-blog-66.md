# word2vec理解思路

本文归纳整理了一些论文和博客对word2vec的理解，以期理解word2vec。

## 概述

### 语言表示：词向量

1. 词的独热表示（One-Hot Representation）

    缺点：

    - 容易受维数灾难的困扰；
    - 不能很好地刻画词与词之间的相似性，任意两个词之间都是孤立的；

2. 词的分布式表示（Distributed Representation）

    1. 基于矩阵的分布表示：比如，GloVe模型；
    2. 基于聚类的分布表示；
    3. 基于神经网络的分布表示，词嵌入；

<!--more-->

### 语言模型

文法语言模型，统计语言模型

核心是上下文的表示以及上下文与目标词之间的关系的建模。

语言模型就是计算一个句子的概率大小的模型。一个句子的打分概率越高，越说明他是更合乎人说出来的自然句子。
常见的统计语言模型有N元文法模型（N-gram Model），最常见的是unigram model、bigram model、trigram model等等。
还有N-pos模型。

### 词嵌入

2001年，Bengio 等人正式提出神经网络语言模型（ Neural Network Language Model ，NNLM），
该模型在学习语言模型的同时，也得到了词向量。所以请注意：**词向量可以认为是神经网络训练语言模型的副产品**。

做法：

1、将one-hot中的vector每一个元素由整形改为浮点型，变为整个实数范围的表示；
2、将原来稀疏的巨大维度压缩 **嵌入** 到一个更小维度的空间。

### 神经网络语言模型与word2vec

#### 神经网络语言模型：

a. Neural Network Language Model ，NNLM
b. Log-Bilinear Language Model， LBL
c. Recurrent Neural Network based Language Model，RNNLM
d. Collobert 和 Weston 在2008 年提出的 C&W 模型
e. Mikolov 等人提出了 CBOW（ Continuous Bagof-Words，连续词袋模型）和 Skip-gram 模型

CBOW和Skip-gram：

- 如果是用一个词语作为输入，来预测它周围的上下文，那这个模型叫做“Skip-gram 模型”；
- 而如果是拿一个词语的上下文作为输入，来预测这个词语本身，则是 “CBOW 模型”。

#### word2vec

实现CBOW和Skip-gram语言模型的工具（正如C&W模型的实现工具是SENNA）。

### CBOW和Skip-gram

1. 原理
2. 加速训练技巧：
    - Negative Sample
    - Hierarchical Softmax

## 应用

文本分类，个性化推荐，广告点击等

## 论文和文章

1. Mikolov 两篇原论文：
    - Distributed Representations of Sentences and Documents
    - Efficient estimation of word representations in vector space
2. Yoav Goldberg 的论文：word2vec Explained- Deriving Mikolov et al.’s Negative-Sampling Word-Embedding Method
3. Xin Rong 的论文：word2vec Parameter Learning Explained
4. 来斯惟的博士论文：《基于神经网络的词和文档语义向量表示方法研究》以及[博客](http://licstar.NET)
5. [word2vec 相比之前的 Word Embedding 方法好在什么地方？](https://www.zhihu.com/question/53011711)
6. Sebastian 的博客：『On word embeddings - Part 2: Approximating the Softmax』
7. 《How to Generate a Good Word Embedding?》,Siwei Lai, Kang Liu, Liheng Xu, Jun Zhao
8. 《面向自然语言处理的分布式表示学习》，邱锡鹏
9. 《Deep Learning 实战之 word2vec》
10. 一些博文：
    - http://www.cnblogs.com/iloveai/p/word2vec.html
    - http://www.hankcs.com/nlp/word2vec.html
    - http://licstar.NET/archives/328
    - https://zhuanlan.zhihu.com/p/22477976
    - http://blog.csdn.Net/itplus/article/details/37969519
    - http://www.tuicool.com/articles/fmuyamf
    - http://licstar.net/archives/620#comment-1542
    - http://blog.csdn.net/ycheng_sjtu/article/details/48520293

## 本文参考

- [word embedding与word2vec: 入门词嵌入前的开胃菜](https://zhuanlan.zhihu.com/p/32590428)
- [秒懂词向量Word2vec的本质](https://zhuanlan.zhihu.com/p/26306795)
- [基于 word2vec 和 CNN 的文本分类 ：综述 & 实践](https://zhuanlan.zhihu.com/p/29076736)
- [word2vec在工业界的应用场景](https://x-algo.cn/index.php/2016/03/12/281/)
- [word2vec有什么应用？ - orangeprince的回答 - 知乎](https://www.zhihu.com/question/25269336/answer/49188284)

