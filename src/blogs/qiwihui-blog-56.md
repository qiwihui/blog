# 机器学习项目清单


[原文](http://www.ic.unicamp.br/~sandra/pdf/Hands_On_Machine_Learning_with_Scikit_Learn_and_TensorFlow-427-432.pdf)来自于《[Hands-On Machine Learning with Scikit-Learn and TensorFlow](https://book.douban.com/subject/26840215/)》，这是一本系统学习机器学习和深度学习非常不错的入门书籍，理论和实践兼而有之。

此清单可以指导你完成机器学习项目。主要有八个步骤：

1. 将问题框架化并且关注重点。
2. 获取数据。
3. 探索数据以洞悉数据。
4. 准备数据以更好地将基础数据模式暴露给机器学习算法。
5. 探索多种不同的模型并列出最好的那些。
6. 微调模型并将它们组合成一个很好的解决方案。
7. 展示你的解决方案。
8. 启动，监督并维护你的系统。

显然，你应该根据你的需求调整此清单。

<!--more-->
## 将问题框架化并且关注重点

1. 用业务术语定义目标。
2. 你的解决方案将如何使用？
3. 目前的解决方案/解决方法（如果有的话）是什么？
4. 你应该如何解决这个问题（监督/非监督，在线/离线等）？
5. 如何度量模型的表现？
6. 模型的表现是否和业务目标一致？
7. 达到业务目标所需的最低性能是多少？
8. 类似的问题如何解决？是否可以复用经验或工具？
9. 人员是否专业？
10. 你如何动手解决问题？
11. 列出目前你（或者其他人）所做的假设。
12. 如果可能，验证假设。

## 获取数据

注意：尽可能自动化，以便你轻松获取新数据。

1. 列出你需要的数据和数据量。
2. 查找并记录你可以获取该数据的位置。
3. 检查它将占用多少存储空间。
4. 检查法律义务并在必要时获取授权。
5. 获取访问权限。
6. 创建工作目录（拥有足够的存储空间）。
7. 获取数据。
8. 将数据转换为你可以轻松操作的格式（不更改数据本身）。
9. 确保删除或保护敏感信息（比如，匿名）。
10. 检查数据的大小和类型（时间序列，样本，地理信息等）。
11. 抽样出测试集，将它放在一边，以后不需要关注它（没有数据窥探！）。

## 探索数据

注意：尝试从领域专家那获取有关这些步骤的见解。

1. 创建用于探索的数据副本（如有必要，将其取样为可管理的大小）。
2. 创建一个 Jupyter 笔记本来记录你的数据探索。
3. 研究每个属性及其特征：

  - 名称；
  - 类型（分类，整数/浮点数，有界/无界，文本，结构化数据等）；
  - 缺失数据的百分比；
  - 噪声点和它的类型（随机点，异常点，舍入误差等）；
  - 对任务可能有用吗？
  - 分布类型（高斯分布，均匀分布，对数分布等）。

4. 对于监督学习任务，确定目标属性。
5. 可视化数据。
6. 研究属性间的相关性。
7. 研究怎如何手动解决问题。
8. 确定你想要应用的有效的转换。
9. 确定有用的额外数据。
10. 记录你所学到的知识。

## 准备数据

注意：

  - 处理数据副本（保持原始数据集完整）。
  - 为你应用的所有数据转换编写函数，原因有五：
    - 你可以在下次获得新数据集时轻松准备数据
    - 你可以在未来的项目中应用这些转换
    - 用来清洗和准备测试数据集
    - 一旦项目上线你可以用来清洗和准备新的数据集
    - 为了便于将你的准备选择视为超参数

1. 数据清洗：

  - 修正或移除异常值（可选）。
  - 填补缺失值（比如用零，平均值，中位数等）或者删除所在行（或者列）。

2. 特征提取（可选）：
  
  - 丢弃不提供有用信息的属性；

3. 适当的特征工程：
  
  - 连续特征离散化。
  - 分解特征（比如分类，日期/时间等）。
  - 对特征添加有益的转换（比如 log(x)，sqrt(x)，x^2 等）
  - Aggregate features into promising new features. 将一些特征融合为有益的新特征

4. 特征缩放：标准化或者正规化特征。

## 列出有用模型

注意：

  - 如果数据量巨大，你可能需要采样出较小的训练集，以便在合理的时间内训练许多不同的模型（请注意，这会对诸如大型神经网络或随机森林等复杂模型进行处罚）。
  - 再次尝试尽可能自动化这些步骤。

1. 使用标准参数训练许多快速、粗糙的模型（比如线性模型，朴素贝叶斯模型，支持向量机模型，随机森林模型，神经网络等）。
2. 衡量并比较他们的表现。
  
  - 对于每个模型，使用 N 折交叉验证法，并且计算基于 N 折交叉验证的均值与方差。

3. 分析每种算法的最重要变量。
4. 分析模型产生的错误类型。
  
  - 人们用什么数据来避免这些错误？

5. 进行一轮快速的特征提取和特征工程。
6. 对之前的五个步骤进行一两次的快速迭代。
7. 列出前三到五名最有用的模型，由其是产生不同类型错误的模型。

## 微调系统

注意：

  - 这一步你将会使用尽可能多的数据，特别是当你微调结束时。
  - 像之前一样尽可能自动化。

1. 使用交叉验证方法调节超参数

  - 要像调节超参数那样对待数据转换的过程，特别是当你不知如何下手的时候（比如，我应该是用零或中值替换缺失值吗？或者直接丢弃它们？）
  - 除非要探索的超参数值非常少，否则最好使用随机搜索而非网格搜索。如果训练的时间很长，你应该使用贝叶斯优化方法（比如，使用在 [Jasper Snoek，Hugo Larochelle 和 Ryan Adams 的论文](https://arxiv.org/pdf/1206.2944.pdf)中描述的，用高斯处理先验）

2. 尝试集成方法，结合最佳模型通常比单独运行它们更好。
3. 一旦你对最终的模型有自信，请在测试集上测量其性能以估计泛化误差。

> 在测量泛化误差后不要调整模型：你会开始过度拟合测试集的。

## 展示你的解决方案

1. 将你做的工作整理成文档。
2. 制作精美的演示。

  - 确保你首先突出重点。

3. 解释你的解决方案实现业务目标的原因。
4. 不要忘记展示在这过程中你注意到的有趣的点。
  
  - 描述哪些有效，哪些无效。
  -列出你的假设和系统的限制。

5. 确保通过精美的可视化或易于记忆的陈述来传达你的主要发现（例如，“收入中位数是房价的第一预测因子”）。

## 启动

1. 准备好生产解决方案（插入生产数据输入，编写单元测试等）。
2. 编写监控代码以定期检查系统的实时性能，并在信号丢失时触发警报。

  - 谨防模型退化：随着数据的进入，模型往往会“腐烂”。
  - 评估模型可能需要大量的人力（比如，通过众包服务可以解决这个问题）
  - 同时监控输入数据的质量（例如，一个有故障的传感器发送随机数据，或者另外一个团队的输出变得陈旧），这对于在线学习系统尤其重要。

3. 定期在新数据上重新训练模型（尽可能自动化）。


[View on GitHub](https://github.com/qiwihui/blog/issues/56)


