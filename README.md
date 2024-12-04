## Bangumi-KGQA

本项目使用 **bangumi** 番组计划的存档静态数据作为数据来源，**neo4j** 图数据库作为存储方式，最终实现基于知识图谱的问答系统，即 **KGQA** 或称 **KBQA** 。



关于 **jsonlines** 的键值含义、结构，见数据来源：[bangumi/Archive: Wiki Data Public Archive](https://github.com/bangumi/Archive)



原数据中 **subject** 约有 500k 条，**person** 约有 70k 条，**character** 约 170k 条，**episode** 约 1370k 条。

因 **neo4j** 的免费额度对节点和关系的限制（节点 200k，关系 400k），为了项目 demo 的顺利运行，对数据进行了阉割，但应当还是能够对后来者想要利用 **bangumi** 进行知识图谱研究的做出点参考。



## 知识图谱/图数据库设计

为了保证 neo4j 免费额度的可用性，只取和前 5k 条 **subject** 相关的 **person** , **character** , **tag** 作为实体，实际上抛弃了 **episode** 。

下面是增加条件限制后的数量：

```yaml
Entity:
- subject         # 5000
  - id
  - type    # ?
  - name
  - name_cn
  - infobox # ?
  - summary # ?
  - date
  - score
  - rank
- person          # 13336
  - id
  - name
  - type
  - career
  - infobox # ?
  - summary # ?
- character       # 23205
  - id
  - name
  - role
  - infobox # ?
  - summary # ?
- tag                # 10566
  - name

Relations:
- subject-subject    # 6028
- subject-character  # 33012
- subject-person     # 92771
- person-character   # 8818
- subject-tag        # 43912

# Node size: 52107
# Relation size: 184541
```

由于关系会建双向边，为了不让关系超出额度，选用前 5k **subject** 比较合适。
