---
title: "一个关于数学概率的问题"
description: "一个关于数学概率的问题"
tags: 
- 技术
- 数学
top: 32
date: 10/09/2018, 13:48:11
author: qiwihui
update: 31/01/2019, 16:09:41
categories: 技术
---

## 题目--百万英雄

你参加一个游戏，在你面前有4张1000万支票，其中一张是真的。游戏开始，你选了一张，之后主持人在剩下
的3张里，选择一个展示出来，验证后发现是假的。

问题：请分情况理性分析，此时，你的参赛权的价格

- 情况一：不允许修改之前的选择
- 情况二：有重新选择的权利

回答：请用下面两种方法分别作答

- 方式1（理论推导）：请给出理论推导和计算过程，情况二需说明如何行使权力；
- 方式2（编程模拟）：使用程序准确客观地模拟上述两种情况下，选手平均获得的奖金，得到参赛权的价格。

<!--more-->
## 解答

方式1（理论推导）

情况1: 不能重新选择时获奖的概率是1/4
情况2: 可以重新选择时是3/8
理由：

1. 不能重新选择时，你的选择不受主持人选择的影响，故为 1/4；
2. 可以重新选择时，会受主持人的影响，是后验概率；第一步选择时，有四种可选，有 `1/4` 选择真实的，`3/4` 选择错误的，主持人的选择在剩下的三个中排除了一个错误的，剩两个。选择真实后重选，再次选中的概率为0，故为 `1/4 * 0 = 0`；选择假的后重选，选中概率为1/2，故为 `3/4 * 1/2 = 3/8`；总的选中真的概率为 `0 + 3/8 = 3/8`。

方式2（编程模拟）:

```python
import random


class Hero:
    """英雄
    """

    def __init__(self):
        self.num = None

    def pick(self, nums):
        self.num = random.choice(nums)


class Host:
    """主持人
    """
    def __init__(self):
        self.num = None

    def pick(self, nums, bnum):
        """主持人
        """
        self.num = random.choice(nums)
        while bnum == self.num:
            self.num = random.choice(nums)

class MH:
    """游戏过程
    """
    def __init__(self):
        self.nums = [0, 1, 2, 3]
        self.host = Host()
        self.hero = Hero()
        self.bnum = random.randint(0, 3)

    def reward(self):
        """奖励
        """
        if self.hero.num == self.bnum:
            return 100
        else:
            return 0

    def play_without_regret(self):
        """不允许修改之前的选择
        """
        self.hero.pick(self.nums)
        self.nums.remove(self.hero.num)
        self.host.pick(self.nums, self.bnum)
        return self.reward()

    def play_with_regret(self):
        """有重新选择的权利
        """
        self.hero.pick(self.nums)
        self.nums.remove(self.hero.num)
        self.host.pick(self.nums, self.bnum)
        self.nums.remove(self.host.num)
        self.hero.pick(self.nums)
        return self.reward()

sum1 = 0
sum2 = 0
# 模拟10000次
times = 10000
for i in range(times):
    sum1 += MH().play_without_regret()
    sum2 += MH().play_with_regret()
avg1 = sum1/float(times)
avg2 = sum2/float(times)
print(avg1)
print(avg2)

```

结果：

```bash
>> python bh.py
24.81
37.12
```

与理论计算一致

## 引申

三门问题（Monty Hall Problem）
电影《决胜21点》

### Comments

