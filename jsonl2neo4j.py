'''
Entity:
- subject         # 5000
  - subject_id
  - type    # + platform
  - name
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
  - infobox # 简体中文名
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
  - RELATION
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
from const import platform_const, relation_const, staff_const, neo4j_const, PersonType, CharacterRole
from py2neo import Graph, Node, Relationship
from tqdm import tqdm

# neo4j
uri, usr, psw = neo4j_const.values()
graph = Graph(uri, auth=(usr, psw))

# 清空
graph.delete_all()

raw_path = './data/reduced_data/'

# Subject
jsonlines_file = 'subject.jsonlines'

attrs = ('id', 'type_cn', 'name', 'name_cn', 'summary', 'date', 'score', 'rank')

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='subject'):
        if lino >= 0: break
        attr_val = {}
        for item in line.items():
            k, v = item
            if k in attrs:
                if k == 'id': k = 'subject_id'
                attr_val.update({k : v})
        
        infobox = line['infobox']
        infobox_parsed = call_parse2(infobox)

        # type-platform -> type_cn
        type_, platform_ = str(line['type']), str(line['platform'])
        attr_val['type_cn'] = platform_const.get(type_, {}).get(platform_, {}).get('type_cn', '')

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

        subject_node = Node('Subject', **attr_val)
        graph.create(subject_node)

# Person
jsonlines_file = 'person.jsonlines'

# career is a list, Better -> career as Node
attrs = ('id', 'type', 'name', 'name_cn', 'summary', 'career')

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in tqdm(enumerate(jsonl), desc='person'):
        if lino >= 0: break
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
    for lino, line in tqdm(enumerate(jsonl), desc='character'):
        if lino >= 0: break
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

