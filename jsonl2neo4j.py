'''
Entity:
- subject         # 5000
  - subject_id
  - type    # + platform
  - name    # 中文名 name_cn
  - name_cn
  - infobox # type_cn
  - summary # 简介
  - date
  - score
  - rank
- person          # 13336
  - person_id
  - name
  - career
  - infobox # 简体中文名 name_cn
  - summary # 简介
- character       # 23205
  - character_id
  - name
  - role
  - infobox # 简体中文名
  - summary # 简介
- tag                # 10566
  - name

Relations:
- subject-subject    # 6028
  - RELATES_TO
- subject-character  # 33012 x 2
  - BELONGS_TO
  - HAS_CHARACTER
- subject-person     # 92771 x 2
  - PARTICIPATED_IN
  - HAS_PARTICIPANT
- person-character   # 8818
  - ACTED_AS
  - PORTRAYED_BY
- subject-tag        # 43912
  - HAS_TAG
  - TAGGED_IN
# Node size: 52107
# Relation size: 184541
'''

import os
import json, jsonlines, py2neo
from wiki_parser import call_parse2, get_attr_val
from const import platform_const, relation_const, staff_const, neo4j_const, PersonType, CharacterRole, CharacterType
from py2neo import Graph, Node, Relationship
from tqdm import tqdm

# neo4j
uri, usr, psw = neo4j_const.values()
graph = Graph(uri, auth=(usr, psw))

# 设定唯一性限制，不满足是抛出异常
# 由于 py2neo 不再维护，在 neo4j 版本较新时，会报错

# graph.schema.create_uniqueness_constraint("Subject", "subject_id")
# graph.schema.create_uniqueness_constraint("Person", "person_id")
# graph.schema.create_uniqueness_constraint("Character", "character_id")
# graph.schema.create_uniqueness_constraint("Tag", "name")

# 清空
graph.delete_all()

raw_path = './data/reduced_data/'

# Subject, Tag, subject-tag
jsonlines_file = 'subject.jsonlines'

attrs = ('id', 'type', 'type_cn', 'name', 'name_cn', 'summary', 'date', 'score', 'rank')

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='Subject'):
        # if lino >= 10: break
        attr_val = {}
        for item in line.items():
            k, v = item
            if k in attrs:
                if k == 'id': k = 'subject_id'
                attr_val.update({k : v})
        
        infobox = line['infobox']
        infobox_parsed = call_parse2(infobox)

        # type-platform -> type_cn
        type_, platform_ = line['type'], line['platform']
        attr_val['type_cn'] = platform_const.get(type_, {}).get(platform_, {}).get('type_cn', '其他')

        if infobox_parsed:
            if 'error' in infobox_parsed:
                print(f"Line {lino}: ")
                print("Error:", infobox_parsed['error'])
            else:
                # print("Wiki result:", infobox_parsed['result'])
                infobox_attr_val = get_attr_val(infobox_parsed['result'])
                # name_cn
                attr_val['name_cn'] = attr_val.get('name_cn', infobox_attr_val.get('中文名', attr_val['name']))
                # attr_val.update(infobox_attr_val)

        Subject_node = Node('Subject', **attr_val)
        graph.create(Subject_node)

        for tag_dict in line['tags']:
            Tag_node = Node('Tag', name=tag_dict['name'])
            graph.merge(Tag_node, 'Tag', 'name') # 不重复插入
            ST_relation = Relationship(Subject_node, 'HAS_TAG', Tag_node)
            graph.create(ST_relation)
            TS_relation = Relationship(Tag_node, 'TAGGED_IN', Subject_node)
            graph.create(TS_relation)


# Person
jsonlines_file = 'person.jsonlines'

# career is a list, Better -> career as Node
attrs = ('id', 'type', 'name', 'name_cn', 'summary', 'career')

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='Person'):
        # if lino >= 10: break
        attr_val = {}
        for item in line.items():
            k, v = item
            if k in attrs:
                if k == 'id': k = 'person_id'
                if k == 'type': v = PersonType(v).name
                attr_val.update({k : v})
        
        infobox = line['infobox']
        infobox_parsed = call_parse2(infobox)

        if infobox_parsed:
            if 'error' in infobox_parsed:
                print(f"Line {lino}: ")
                print("Error:", infobox_parsed['error'])
            else:
                # print("Wiki result:", infobox_parsed['result'])
                infobox_attr_val = get_attr_val(infobox_parsed['result'])
                # name_cn
                attr_val['name_cn'] = attr_val.get('name_cn', infobox_attr_val.get('简体中文名', attr_val['name']))
                # attr_val.update(infobox_attr_val)

        Person_node = Node('Person', **attr_val)
        graph.create(Person_node)

# Character
jsonlines_file = 'character.jsonlines'

attrs = ('id', 'role', 'name', 'name_cn', 'summary')

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='Character'):
        # if lino >= 10: break
        attr_val = {}
        for item in line.items():
            k, v = item
            if k in attrs:
                if k == 'id': k = 'character_id'
                if k == 'role': v = CharacterRole(v).name
                attr_val.update({k : v})
        
        infobox = line['infobox']
        infobox_parsed = call_parse2(infobox)

        if infobox_parsed:
            if 'error' in infobox_parsed:
                print(f"Line {lino}: ")
                print("Error:", infobox_parsed['error'])
            else:
                # print("Wiki result:", infobox_parsed['result'])
                infobox_attr_val = get_attr_val(infobox_parsed['result'])
                # name_cn
                attr_val['name_cn'] = attr_val.get('name_cn', infobox_attr_val.get('简体中文名', attr_val['name']))
                # attr_val.update(infobox_attr_val)

        Character_node = Node('Character', **attr_val)
        graph.create(Character_node)

# Subject-relations
jsonlines_file = 'subject-relations.jsonlines'

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='subject-relations'):
        # if lino >= 10: break
        sid, rsid = line['subject_id'], line['related_subject_id']
        # 保证是唯一的
        s_node = graph.nodes.match("Subject", subject_id=sid).first()
        rs_node = graph.nodes.match("Subject", subject_id=rsid).first()
        relation_ = line['relation_type']
        relation = relation_const.get(s_node['type'], {}).get(relation_, {}).get('cn', '其他')
        if s_node and rs_node:
            SS_relation = Relationship(s_node, 'RELATES_TO', rs_node, relation=relation)
            graph.create(SS_relation)
        else:
            print('S/S miss node.')

# Subject-Person
jsonlines_file = 'subject-persons.jsonlines'

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='subject-persons'):
        # if lino >= 10: break
        pid, sid = line['person_id'], line['subject_id']
        # 保证是唯一的
        p_node = graph.nodes.match("Person", person_id=pid).first()
        s_node = graph.nodes.match("Subject", subject_id=sid).first()
        position_ = line['position']
        position = staff_const.get(s_node['type'], {}).get(position_, {}).get('cn', '其他')
        if p_node and s_node:
            PS_relation = Relationship(p_node, 'PARTICIPATED_IN', s_node, position=position)
            graph.create(PS_relation)
            SP_relation = Relationship(s_node, 'HAS_PARTICIPANT', p_node, position=position)
            graph.create(SP_relation)
        else:
            print('P/S miss node.')

# Subject-Character
jsonlines_file = 'subject-characters.jsonlines'

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='subject-character'):
        # if lino >= 10: break
        cid, sid = line['character_id'], line['subject_id']
        # 保证是唯一的
        c_node = graph.nodes.match("Character", character_id=cid).first()
        s_node = graph.nodes.match("Subject", subject_id=sid).first()
        type = CharacterType(line['type']).name
        # order (type, order) ASC
        attr_val = {'type': type, 'order': line['order']}
        if c_node and s_node:
            CS_relation = Relationship(c_node, 'BELONGS_TO', s_node, **attr_val)
            graph.create(CS_relation)
            SC_relation = Relationship(s_node, 'HAS_CHARACTER', c_node, **attr_val)
            graph.create(SC_relation)
        else:
            print('C/S miss node.')

# Person-Character
jsonlines_file = 'person-characters.jsonlines'

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='person-character'):
        # if lino >= 10: break
        pid, cid = line['person_id'], line['character_id']
        sid = line['subject_id']
        # 保证是唯一的
        p_node = graph.nodes.match("Person", person_id=pid).first()
        c_node = graph.nodes.match("Character", character_id=cid).first()
        if p_node and c_node:
            PC_relation = Relationship(p_node, 'ACTED_AS', c_node, subject_id=sid)
            graph.create(PC_relation)
            CP_relation = Relationship(c_node, 'PORTRAYED_BY', p_node, subject_id=sid)
            graph.create(CP_relation)
        else:
            print('P/C miss node.')