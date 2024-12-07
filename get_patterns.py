from const import graph
import json

# 提前已经在外部用指令将 neo4j 构建好了

# 查询函数
def get_label_bag():
    query = """
    MATCH (n)
    WHERE n.name_cn IS NOT NULL AND n.name_cn <> '' AND n.name_cn =~ '[^[:punct:]，。！？：“”‘’（）【】]+'
    RETURN labels(n) AS label, collect(n.name_cn) AS names
    """
    result = graph.run(query)
    
    # print(result.data())

    # 将结果转换为字典
    label_bag = {}
    for dict in result.data():
        label_bag[dict['label'][0]] = dict['names']
    return label_bag

label_bag = get_label_bag()
# print(label_bag)
print(label_bag.keys())

file_path = "./QA_data/new_patterns.json"

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(label_bag, file, ensure_ascii=False, indent=4)

print(f"数据已写入 {file_path}")

file_path = "./QA_data/add_new_patterns.json"

add_new_patterns = []

for label, patterns in label_bag.items():
    if label == 'Tag': continue
    for pattern in patterns:
        add_new_patterns.append({'label': label, 'pattern': pattern})


with open(file_path, "w", encoding="utf-8") as file:
    json.dump(add_new_patterns, file, ensure_ascii=False, indent=4)
print(f"数据已写入 {file_path}")

file_path = "./QA_data/vocab.json"

vocab = []

for label, names in label_bag.items():
    if label == 'Tag': continue
    vocab.extend(names)

vocab = list(set(vocab))

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(vocab, file, ensure_ascii=False, indent=4)
print(f"数据已写入 {file_path}")