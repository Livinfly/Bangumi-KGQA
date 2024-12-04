'''
Entity:
- subject_id
- person_id
- character_id
- tag

Relations:
- subject-subject
- subject-character
- subject-person
- person-character
'''

import os
import json, jsonlines, py2neo
from wiki_parser import call_parse2, get_attr_val
from const import SubjectType

raw_path = './data/raw/'

# subject
jsonlines_file = 'subject.jsonlines'

with jsonlines.open(os.path.join(raw_path, jsonlines_file)) as jsonl:
    for lino, line in enumerate(jsonl):
        if lino > 0: break

        attr_val = {}

        # attr_val.update({k: v for k, v in line.items() if k != 'infobox' or v != ''})
        for item in line.items():
            k, v = item
            if k == 'infobox' or v == '': continue
            if k == 'id': attr_val.update({'subject_id': v})
            elif k == 'type': attr_val.update(item)
            elif k == 'name': attr_val.update(item)
            elif k == 'name_cn': attr_val.update(item)
            elif k == 'platform': attr_val.update(item)
        
        # print(attr_val)
        # print()
        infobox = line['infobox']
        infobox_parsed = call_parse2(infobox)

        if infobox_parsed:
            if 'error' in infobox_parsed:
                print(f"Line {lino}: ")
                print("Error:", infobox_parsed['error'])
            else:
                # print("Wiki result:", infobox_parsed['result'])
                attr_val.update((get_attr_val(infobox_parsed['result'])))
        print(attr_val)
        
