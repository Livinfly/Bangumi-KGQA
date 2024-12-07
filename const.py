from enum import Enum
import json, yaml
import spacy
from py2neo import Graph, Node, Relationship

class PersonType(Enum):
    个人 = 1
    公司 = 2
    组合 = 3

class CharacterRole(Enum):
    角色 = 1
    机体 = 2
    组织 = 3
    标志 = 4

class CharacterType(Enum):
    主角 = 1
    配角 = 2
    客串 = 3

neo4j_const = {
    "uri": "bolt://localhost:7687",
    "usr": "neo4j",
    "pwd": "bgmbgm!!!",
}

uri, usr, psw = neo4j_const.values()
graph = Graph(uri, auth=(usr, psw))

with open("./data/subject_platforms.yml", "r", encoding="utf-8") as p, \
    open("./data/subject_relations.yml", "r", encoding="utf-8") as r, \
    open("./data/subject_staffs.yml", "r", encoding="utf-8") as s:
    platform_const = yaml.safe_load(p)['platforms']
    relation_const = yaml.safe_load(r)['relations']
    staff_const = yaml.safe_load(s)['staffs']

with open('./QA_data/new_patterns.json', 'r', encoding='utf-8') as np, \
    open('./QA_data/add_new_patterns.json', 'r', encoding='utf-8') as anp, \
    open('./QA_data/vocab.json', 'r', encoding='utf-8') as vocab:
    new_patterns = json.load(np)
    add_new_patterns = json.load(anp)
    vocab = json.load(vocab)

attr_list = ['summary', 'name', 'type_cn', 'score', 'rank', 'career', 'date']

rel_list = ['RELATES_TO', 'BELONGS_TO', 'HAS_CHARACTER', 'ACTED_AS', 
            'HAS_TAG', 'PORTRAYED_BY', 'PARTICIPATED_IN', 'HAS_PARTICIPANT',
            ]

intent_map = {
    '介绍': 'summary',
    '简介': 'summary',
    '故事': 'summary',
    '概要': 'summary',
    '梗概': 'summary',
    '原名': 'name',
    '类别': 'type_cn',
    '发布': 'date',
    '日期': 'date',
    '时间': 'date',
    '什么时候': 'date',
    '评分': 'score',
    '怎么样': 'score',
    '排名': 'rank',
    '职业': 'career',
    '做什么': 'career',

    '相关作品': 'RELATES_TO',
    '出现': 'BELONGS_TO',
    '角色': 'HAS_CHARACTER',
    '作品': 'PARTICIPATED_IN',
    '有哪些人参与': 'HAS_PARTICIPANT',
    '扮演': 'ACTED_AS',
    '配音': 'ACTED_AS',
    '由谁扮演': 'PORTRAYED_BY',
    '由谁配音': 'PORTRAYED_BY',
    '什么类型': 'HAS_TAG',
}
intent_map_re = {
    'summary': '简介',
    'name': '原名',
    'type_cn': '类别',
    'date': '发布日期',
    'score': '评分',
    'rank': '排名',
    'career': '职业',

    'RELATES_TO': '相关作品',
    'BELONGS_TO': '出现',
    'HAS_CHARACTER': '角色',
    'PARTICIPATED_IN': '作品',
    'HAS_PARTICIPANT': '工作人员',
    'ACTED_AS': '扮演',
    'PORTRAYED_BY': '扮演者',
    'HAS_TAG': '类型',
}

# zh_core_web_sm zh_core_web_trf
nlp_entity = spacy.load('zh_core_web_sm')
nlp_entity.tokenizer.pkuseg_update_user_dict(vocab)
ruler = nlp_entity.add_pipe('entity_ruler', config={"overwrite_ents": True}, last=False)
ruler.add_patterns(add_new_patterns)

nlp_intent = spacy.load('zh_core_web_sm')
nlp_intent.tokenizer.pkuseg_update_user_dict(intent_map.keys())

if __name__ == '__main__':
    print('Check const')
    print(platform_const.keys())
    # print(relation_const)
    # print(staff_const)