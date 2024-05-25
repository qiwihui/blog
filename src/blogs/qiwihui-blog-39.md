# Elasticsearch cheat sheet

### 1

`curl -X<REST Verb> <Node>:<Port>/<Index>/<Type>/<ID>`

```
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": { "match_all": {} },
  "_source": ["account_number", "balance"],
  "sort": { "balance": { "order": "desc" } }
}'
```

`bool must`: 所有的查询都必须为真
`bool should`: 只要有一个查询匹配
`bool must_not`: 查询列表中的的所有查询都必须都不为真


### 2. 执行过滤器

`_score`: 指定的搜索查询匹配程度的一个相对度量。得分越高，文档越相关，得分越低文档的相关度越低。
Elasticsearch中的所有的查询都会触发相关度得分的计算。对于那些我们不需要相关度得分的场景下，Elasticsearch以过滤器的形式提供了另一种查询功能。

过滤器在概念上类似于查询，但是它们有非常快的执行速度，这种快的执行速度主要有以下两个原因：
  - 过滤器不会计算相关度的得分，所以它们在计算上更快一些
  - 过滤器可以被缓存到内存中，这使得在重复的搜索查询上，其要比相应的查询快出许多。

通常情况下，要决定是使用过滤器还是使用查询，你就需要问自己是否需要相关度得分。如果相关度是不重要的，使用过滤器，否则使用查询。

```bash
curl -XPOST 'localhost:9200/bank/_search?pretty' -d '
{
  "query": {
    "filtered": {
      "query": { "match_all": {} },
      "filter": {
        "range": {
          "balance": {
            "gte": 20000,
            "lte": 30000
          }
        }
      }
    }
  }
}'
```

### 3

doc['my_field'].value和_source.my_field之间的不同:
  - 首先，使用doc关键字，会使相应的字段加载到内存，执行速度更快但是更耗费内存；
  - 第二，doc[...]符号 仅允许简单的值字段，只在基于字段的非分析或者单个项上有意义；
  - _source加载、分析source，然后仅仅返回相关部分的json。

### 参考

- [elasticsearch guide chinese](https://endymecy.gitbooks.io/elasticsearch-guide-chinese/)
- https://gist.github.com/ruanbekker/e8a09604b14f37e8d2f743a87b930f93
- https://gist.github.com/stephen-puiszis/212b8a8b37f67c670422
