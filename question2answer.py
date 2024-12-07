from const import nlp_entity, nlp_intent, vocab, graph, intent_map, attr_list, rel_list, intent_map_re
from fuzzywuzzy import fuzz

def parse_entity(text):
    k = 2

    doc = nlp_entity(text)
    # 如果没有识别到实体，使用相似度计算
    all_similarities = {}  # 存储每个分词的前k高相似度实体

    # 为了避免实体识别的 label 不是我设定 label 之一，直接用分词相似度进行比较了

    # 对每个分词计算与 vocab 中实体的相似度
    for token in doc:
        similarity_scores = []
        for entity in vocab:
            similarity = fuzz.ratio(token.text, entity)  # 使用 fuzzywuzzy 计算相似度
            similarity_scores.append((entity, similarity))  # 保存实体和相似度的元组

        # 排序，获取相似度最高的前k个实体
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_three = similarity_scores[:k]  # 选取前k高的实体
        # print(token)
        # print(top_three)
        all_similarities[token.text] = top_three  # 存储分词和对应的前k个实体

    # 针对所有分词的实体，计算整体句子的相似度
    best_entity = None
    highest_sentence_similarity = 0

    for token, top_entities in all_similarities.items():
        for entity, entity_similarity in top_entities:
            # 计算该实体与整个句子的相似度
            sentence_similarity = fuzz.ratio(text, entity)
            # print(token, entity, sentence_similarity)
            if entity_similarity > 30 and \
                (sentence_similarity > highest_sentence_similarity or \
                sentence_similarity == highest_sentence_similarity and len(entity) > len(best_entity)):
                highest_sentence_similarity = sentence_similarity
                best_entity = entity
    # print(f"最终选择的实体是: {best_entity}，类别是: {nlp(best_entity).ents[0].label_}")
    if best_entity == None: return None, None
    return best_entity, nlp_entity(best_entity).ents[0].label_

def parse_question_intent(text):
    doc = nlp_intent(text)
    tokens = [token.text for token in doc]

    intent_attr = []
    intent_rel = []

    for keyword, attr in intent_map.items():
        if keyword in tokens:
            if attr in attr_list:  # 如果是属性
                intent_attr.append(attr)
            elif attr in rel_list:  # 如果是关系
                intent_rel.append(attr)
    
    intent_attr = list(set(intent_attr))
    intent_rel = list(set(intent_rel))

    return intent_attr, intent_rel

def q2a(text):
    entity = parse_entity(text)
    # print(entity)
    if entity[0] == None: return '没有找到相关信息喵，我会加油的！'
    intent_attr, intent_rel = parse_question_intent(text)
    # print(intent_attr)
    answer = ''
    query = """
    MATCH (n:{label})
    WHERE n.name_cn = '{name_cn}'
    RETURN n
    """.replace('{label}', entity[1]).replace('{name_cn}', entity[0])
    result = graph.run(query)
    node = result.data()[0]['n']
    for attr in intent_attr:
        answer = answer + f"{entity[0]}的{intent_map_re[attr]}：{node[attr]}\n"
    
    query = """
        MATCH (p:{label} {name_cn: '{name_cn}'})-[r:{relationship_type}]->(m)
        RETURN m LIMIT 3
    """.replace('{label}', entity[1]).replace('{name_cn}', entity[0])
    query_bak = query

    for rel in intent_rel:
        query = query_bak.replace('{relationship_type}', rel)
        result = graph.run(query)
        rets = []
        for ret in result.data():
            ret = ret['m']
            t = ret.get('name_cn', ret.get('name'))
            if t != '': rets.append(t)
        if rets != []: answer = answer + f"{entity[0]}的{intent_map_re[rel]}：{'，'.join(rets)}等\n"
    
    if answer == '': return '没有找到相关信息喵，我会加油的！'
    answer = answer + "以上，(∠・ω< )⌒☆ 。"
    return answer

    
if __name__ == '__main__':
    text = "冬马和纱出现在什么作品里啊，由谁配音"
    text = "白色相簿2的评分是多少啊，相关作品有哪些，工作人员有谁，有哪些角色？"
    text = '介绍一下ZUN，并列举他的作品？'
    text = '介绍一下古明地恋'
    text = '名侦探柯南是什么类型的作品，角色有哪些？'
    text = '谢谢你，谱酱！'
    # ret = parse_entity(text)
    # print(*ret)
    q2a(text)