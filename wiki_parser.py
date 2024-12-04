import subprocess
import json

def call_parse2(wiki_string):
    # 使用 subprocess 调用 Node.js 脚本
    result = subprocess.run(
        ['node', 'wiki_parser.mjs', wiki_string],  # 传入 wiki 字符串
        capture_output=True,  # 捕获输出
        text=True,  # 以文本格式返回输出
        encoding='utf-8'
    )
    # 如果 Node.js 脚本执行成功
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)  # 将返回的 JSON 字符串解析成字典
        except json.JSONDecodeError:
            print("Failed to parse JSON from Node.js output.")
            return None
    else:
        print("Error in Node.js script:", result.stderr)
        return None

def get_attr_val(wiki_dict):
    ret = {}
    for x in wiki_dict['data']:
        attr, val = x['key'], x['value'] if 'value' in x.keys() else x['values']
        if val not in ('', []): # 过滤空内容
            ret[attr] = val
    return ret

if __name__ == '__main__':
    # 示例：调用函数并打印结果
    wiki_string = """
    {{Infobox animanga/Novel\r\n|中文名= 第一次的亲密接触\r\n|别名={\r\n}\r\n|出版社= 紅色文化、知识出版社\r\n|价格= NT$160\r\n|连载杂志= \r\n|发售日= 1998-09-25\r\n|册数= \r\n|页数= 188\r\n|话数= \r\n|ISBN= 9789577086709\r\n|其他= \r\n|作者= 蔡智恒\r\n|ISBN-10= 9577086705\r\n}}
    """

    result = call_parse2(wiki_string)
    if result:
        if 'error' in result:
            print("Error:", result['error'])
        else:
            print("Wiki result:", result['result'])
            wiki_attr_dict = get_attr_val(result['result'])
            print(wiki_attr_dict)