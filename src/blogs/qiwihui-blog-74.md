---
title: "HMM理解思路"
description: "HMM理解思路"
tags: 
- 机器学习
top: 74
date: 03/06/2019, 17:39:05
author: qiwihui
update: 04/06/2019, 11:34:17
categories: 
---

HMM
====

本文整理简单整理一下HMM的理解思路。

<!--more-->

## 模型

### 马尔科夫性与马尔科夫链

性质：
    - 有限历史假设
    - 时间不变性

### 隐马尔科夫模型

1. 模型定义：
    1、初始状态概率向量 $\pi=(\pi_i)$，其中 $\pi_{i}=P(i_{1}=q_{i}), \quad i=1,2, \cdots, N$
    2、状态转移概率矩阵 $A=\left[a_{i j}\right]_{N \times N}$，其中 $a_{i j}=P\left(i_{t+1}=q_{j} | i_{t}=q_{i}\right), \quad i=1,2, \cdots, N ; j=1,2, \cdots, N$
    3、观测概率矩阵 $B=\left[b_{j}(k)\right]_{N \times M}$，其中 $b_{j}(k)=P\left(o_{t}=v_{k} | i_{t}=q_{j}\right), \quad k=1,2, \cdots, M ; j=1,2, \cdots, N$
    4、观测序列 $O=(o_{1}, o_{2}, \cdots, o_{T})$，状态序列 $I=(i_{1}, i_{2}, \cdots, i_{T})$
    5、状态集合 $Q=\left\{q_{1}, q_{2}, \cdots, q_{N}\right\}$，观测集合 $V=\left\{v_{1}, v_{2}, \cdots, v_{M}\right\}$

2. 模型三元组 $\lambda=(A, B, \pi)$

    状态转移概率矩阵A与初始状态概率向量确定了隐藏的马尔科夫链，生成不可观测的序列。观测概率矩阵B确定了如何从状态生成规则，与状态序列综合确定了如何产生观测序列。

3. 模型基本假设：

    - 齐次马尔科夫性假设：设隐马尔科夫链在任意时刻t的状态只依赖于其前一时刻的状态，与其他时刻的状态及观测无关，也与时刻t无关。
    - 观测独立性假设：假设任意时刻的观测只依赖于该时刻的马尔科夫链的状态，与其他观测和状态无关。

4. 例子：
    - [感冒预测](https://en.wikipedia.org/wiki/Viterbi_algorithm#Example)，[中文](https://applenob.github.io/hmm.html#%E4%B8%80%E4%B8%AA%E5%85%B3%E4%BA%8E%E6%84%9F%E5%86%92%E7%9A%84%E5%AE%9E%E4%BE%8B)
    - [掷骰子](https://www.zhihu.com/question/20962240/answer/33438846)
    - [天气模型](https://www.zhihu.com/question/20962240/answer/64187492)
    - [偷换骰子大法](https://www.zhihu.com/question/20962240/answer/33561657)

## 三个问题

### 概率计算问题（评估）

给定模型 $\lambda=(A, B, \pi)$ 和观测序列 $O=o_{1}, o_{2}, \ldots, o_{T}$，计算在模型 $\pi$ 下观测序列 $O$ 出现的概率 $P(O | \lambda)$。
    - 穷举搜索，`O(TN^T)`
    - 前向算法，`O(N^2T)`
    - 后向算法

### 预测问题（解码）

已知观测序列 $O=o_{1}, o_{2}, \ldots, o_{T}$ 和模型 $\lambda=(A, B, \pi)$，求给定观测序列条件概率 $P(I|O)$ 最大的状态序列 $I=\left(i_{1}, i_{2}, \ldots, i_{T}\right)$，即给定观测序列，求最有可能的对应的状态序列。
    - 穷举搜索
    - 近似计算
    - 维特比（Viterbi）算法：动态规划

### 学习问题

已知观测序列 $O=o_{1}, o_{2}, \ldots, o_{T}$，估计模型 $\lambda=(A, B, \pi)$，使 $P(O | \lambda)$ 最大。
    - 监督算法：利用极大似然估计
    - 非监督算法：Baum-Welch算法（EM算法在HMM中的具体实现）

## 应用

语音识别，中文分词，手写识别

## 参考

1. 《统计学习方法》，李航
2. [隐马尔科夫模型（HMM）及其Python实现](https://applenob.github.io/hmm.html)


### Comments

