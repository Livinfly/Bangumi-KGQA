from enum import Enum
import yaml

class PersonType(Enum):
    个人 = 1
    公司 = 2
    组合 = 3

class CharacterRole(Enum):
    角色 = 1
    机体 = 2
    组织 = 3
    标志 = 4


neo4j_const = {
    "uri": "bolt://localhost:7687",
    "usr": "neo4j",
    "pwd": "bgmbgm!!!",
}

with open("./data/subject_platforms.yml", "r", encoding="utf-8") as p, \
    open("./data/subject_relations.yml", "r", encoding="utf-8") as r, \
    open("./data/subject_staffs.yml", "r", encoding="utf-8") as s:
    platform_const = yaml.safe_load(p)['platforms']
    relation_const = yaml.safe_load(r)
    staff_const = yaml.safe_load(s)

if __name__ == '__main__':
    print('Check const')
    print(platform_const.keys())
    # print(relation_const)
    # print(staff_const)