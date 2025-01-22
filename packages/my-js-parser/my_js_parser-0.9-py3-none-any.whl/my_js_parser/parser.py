# The MIT License
#
# Copyright 2014, 2015 Piotr Dabkowski
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the 'Software'),
# to deal in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

from  lxml import etree
import json 
import quickjs
import re

def extract_all_json(script_text):
    json_list = []  # 存储提取的所有 JSON 对象
    start = -1  # 初始化起始位置
    open_braces = 0  # 追踪大括号的匹配情况
    open_brackets = 0  # 追踪方括号的匹配情况

    # 使用正则表达式匹配所有花括号和方括号
    script_label = re.finditer(r'[\{\}\[\]]', script_text)

    for item in script_label:
        if item.group() == '{':
            # 如果遇到左花括号并且没有其他打开的括号时，记录开始位置
            if open_braces == 0 and open_brackets == 0:
                start = item.start()
            open_braces += 1
        elif item.group() == '}':
            open_braces = open_braces - 1 if open_braces>0 else open_braces
            # 当大括号关闭并且没有其他打开的括号时，提取 JSON
            if open_braces == 0 and open_brackets == 0 and start != -1:
                json_list.append(script_text[start:item.end()])
                start = -1  # 重置 start，准备下一个 JSON 对象

        elif item.group() == '[':
            # 如果遇到左方括号并且没有其他打开的括号时，记录开始位置
            if open_braces == 0 and open_brackets == 0:
                start = item.start()
            open_brackets += 1
        elif item.group() == ']':
            open_brackets = open_brackets- 1 if open_brackets > 0 else open_brackets
            # 当方括号关闭并且没有其他打开的括号时，提取 JSON
            if open_braces == 0 and open_brackets == 0 and start != -1:
                json_list.append(script_text[start:item.end()])
                start = -1  # 重置 start，准备下一个 JSON 对象

    result = []
    if json_list:
        for json_part in json_list:
            try:
                # 尝试直接解析 JSON
                data = json.loads(json_part)
                result.append(data)
            except json.JSONDecodeError:
                try:
                    # 将单引号替换为双引号，确保它是有效的 JSON 格式
                    json_part = json_part.replace("'", '"')
                    data = json.loads(json_part)
                    result.append(data)
                except json.JSONDecodeError:
                    pass
    return result  # 如果找不到 JSON，返回空列表

def update_without_overwriting_empty(result, parsedData):
    for key, value in parsedData.items():
        # 如果值是字典，并且 result[key] 也是字典，则递归更新
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            update_without_overwriting_empty(result[key], value)
        else:
            # 检查是否为空值，避免覆盖已有数据
            if value not in (None, '', [], {}, set()):
                result[key] = value


def parse_html(html_content):
    context = quickjs.Context()
    context.set_memory_limit(10 * 1024 * 1024)  # 10 MB
    context.set_time_limit(15)
    context.eval(
        """
            const window = this;
            const document = {};
            const location = {};
            const navigator = {
              "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            };
            """
    )

    html = etree.HTML(html_content)
    result = {}
    script_list = html.xpath('//script/text()')
    for script_text in script_list:
        try:
            parsedData = json.loads(script_text)
            if parsedData:
                update_without_overwriting_empty(result, parsedData)
        except:
            try:
                context.eval(script_text)
            except:
                pass
    script = """
        Object.entries(window).reduce((acc, [key, val]) => {
        // 如果当前 key 是要跳过的，直接返回 acc


        const valType = typeof val;

        // 如果值是函数，跳过
        if (valType === 'function') {
            return acc;
        }

        try {
            // 1. 检查值是否是对象或数组
            if (val && (valType === 'object' || Array.isArray(val))) {
                JSON.stringify(val); // 测试是否可序列化
                acc[key] = val; // 保留有效数据
            }

            // 2. 检查值是否是 JSON 格式的字符串
            if (valType === 'string' || valType === 'number') {
                const parsedVal = JSON.parse(val); // 尝试解析
                if (parsedVal) {
                    acc[key] = parsedVal; // 保留解析成功的对象或数组
                }
            }
        } catch (e) {
            // 跳过不可序列化的值
        }

        return acc;
    }, {})
    """

    try:
        windowResult = context.eval(script).json()
        js_result = json.loads(windowResult)
        update_without_overwriting_empty(result, js_result)

    except Exception as e:
        pass

    try:
        for item in extract_all_json(script_text):
            if type(item) == dict:
                update_without_overwriting_empty(result, item)
            elif type(item) == list:
                if result.get('list_parse_data_&') == None:
                    result['list_parse_data_&'] = []
                else:
                    pass
                result['list_parse_data_&'].append(item)
    except Exception as e:
        pass
    return result




