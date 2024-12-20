import os
import jsonlines

raw_path = './data/raw_data'
reduced_path = './data/reduced_data'

echo_flag = False    # 是否输出文件生成相关提示
subject_head = 5000  # 取前多少行 subject
recover_flag = False # 是否覆盖

# subject
file = 'subject.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for lino, line in enumerate(reader):
            if lino >= subject_head: break
            writer.write(line)
    if echo_flag: print(f'{file} 已处理。')

subject_id_set = set()

with jsonlines.open(output_path) as reader:
    for line in reader:
        if 'id' in line: 
            sid = int(line['id'])
            subject_id_set.add(sid)

print(f'subject_id size: {len(subject_id_set)}')

# subject-subject
file = 'subject-relations.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

subject_relation_size = 0

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
    with open(output_path, 'r', encoding='utf-8') as file:
        subject_relation_size =  sum(1 for _ in file)
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for line in reader:
            if 'subject_id' in line and 'related_subject_id' in line:
                sid = int(line['subject_id'])
                rsid = int(line['related_subject_id'])
                if sid in subject_id_set and rsid in subject_id_set: 
                    writer.write(line)
                    subject_relation_size += 1
    if echo_flag: print(f'{file} 已处理。')

print(f'subject_relation size: {subject_relation_size}')

# subject-character
file = 'subject-characters.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

subject_character_relation_size = 0

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
    with open(output_path, 'r', encoding='utf-8') as file:
        subject_character_relation_size =  sum(1 for _ in file)
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for line in reader:
            if 'subject_id' in line:
                sid = int(line['subject_id'])
                if sid in subject_id_set: 
                    writer.write(line)
                    subject_character_relation_size += 1
    if echo_flag: print(f'{file} 已处理。')

print(f'subject_character_relation size: {subject_character_relation_size}')

character_id_set = set()

with jsonlines.open(output_path) as reader:
    for line in reader:
        if 'character_id' in line: 
            cid = int(line['character_id'])
            character_id_set.add(cid)

print(f'character_id size: {len(character_id_set)}')

# character
file = 'character.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for line in reader:
            if 'id' in line:
                cid = int(line['id'])
                if cid in character_id_set: 
                    writer.write(line)
    if echo_flag: print(f'{file} 已处理。')

# subject-person
file = 'subject-persons.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

subject_person_relation_size = 0

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
    with open(output_path, 'r', encoding='utf-8') as file:
        subject_person_relation_size =  sum(1 for _ in file)
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for line in reader:
            if 'subject_id' in line:
                sid = int(line['subject_id'])
                if sid in subject_id_set: 
                    writer.write(line)
                    subject_person_relation_size += 1
    if echo_flag: print(f'{file} 已处理。')

print(f'subject_person_relation size: {subject_person_relation_size}')

person_id_set = set()

with jsonlines.open(output_path) as reader:
    for line in reader:
        if 'person_id' in line:
            pid = int(line['person_id']) 
            person_id_set.add(pid)

print(f'person_id size: {len(person_id_set)}')

# person
file = 'person.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for line in reader:
            if 'id' in line:
                pid = int(line['id'])
                if pid in person_id_set: 
                    writer.write(line)
    if echo_flag: print(f'{file} 已处理。')

# person-character
file = 'person-characters.jsonlines'

input_path = os.path.join(raw_path, file)
output_path = os.path.join(reduced_path, file)

person_character_relation_size = 0

if os.path.exists(output_path) and not recover_flag:
    if echo_flag: print(f"{file} 已存在。")
    with open(output_path, 'r', encoding='utf-8') as file:
        person_character_relation_size =  sum(1 for _ in file)
else:    
    with jsonlines.open(input_path) as reader, jsonlines.open(output_path, mode='w') as writer:
        for line in reader:
            if 'person_id' in line and 'subject_id' in line and 'character_id' in line:
                pid = int(line['person_id'])
                sid = int(line['subject_id'])
                cid = int(line['character_id'])
                if pid in person_id_set and sid in subject_id_set and cid in character_id_set: 
                    writer.write(line)
                    person_character_relation_size += 1
    if echo_flag: print(f'{file} 已处理。')

print(f'person_character_relation size: {person_character_relation_size}')

# tag
file = 'subject.jsonlines'

input_path = os.path.join(reduced_path, file)

tag_set = set()
subject_tag_relation_size = 0

with jsonlines.open(input_path) as reader:
    for line in reader:
        if 'tags' in line:
            tags = line['tags']
            # print(tags)
            for dic in tags:
                tag = dic['name']
                tag_set.add(tag)
                subject_tag_relation_size += 1

print(f'tag size: {len(tag_set)}')
print(f'subject_tag_relation size: {subject_tag_relation_size}')

# summary
print(f'Node size: {len(subject_id_set) + len(character_id_set) + len(person_id_set) + len(tag_set)}')
print(f'Relation size: {subject_relation_size + subject_character_relation_size + subject_person_relation_size + person_character_relation_size + subject_tag_relation_size}')