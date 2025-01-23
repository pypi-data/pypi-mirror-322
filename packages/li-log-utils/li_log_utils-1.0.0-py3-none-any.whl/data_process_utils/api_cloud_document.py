import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import argparse
from pandas import Timestamp
from data_process_utils.log_utils import *

import json

# 出现如下列名会禁止写入 欢迎添加新的内容
forbidden_strings = [
    "是否为多轮首轮\n首轮标1，非首轮标0\n单轮标1",
    "session结果",
    "query结果",
    "备注",
    "是否澄清（需要澄清标1）",
    "负反馈标1 正反馈标2",
    "录音实际内容",
    "语音一级标签",
    "语音二级标签",
    "问题严重类型",
    "高频/低频",
    "必现/偶现",
    "外部声源"
]

# 数字转列 1=A，3=C，10=J，49=AW
def number_to_column(result):
    if isinstance(result, str):
        result = json.loads(result)
        column_count = result["data"]["sheet"]["grid_properties"]["column_count"]  # int 列
        row_count = result["data"]["sheet"]["grid_properties"]["row_count"]  # row_count 行
    else:
        column_count = result
    if column_count <= 0:
        raise ValueError("输入的数字必须大于0")

    result = ""
    while column_count > 0:
        column_count -= 1  # 因为Excel列是从1开始的，而我们的转换是从0开始的（26进制）
        remainder = column_count % 26
        result = chr(remainder + ord('A')) + result  # 将余数转换为字母并添加到结果字符串的前面
        column_count //= 26  # 进行整数除法以获取下一个更高位的值
    return result, row_count

#列字母转数字
def column_letter_to_number(letter_str):
    result = 0
    for i, letter in enumerate(reversed(letter_str)):
        value = ord(letter) - ord('A') + 1
        result += value * (26 ** i)
    return result


# 输出格式与read_pd_csv出输出格式一致，type->[{}]
def convert_to_list_of_dicts(result: str) -> list:

    result = json.loads(result)
    result = result["data"]["valueRange"]["values"]
    keys = result[0]
    formatted_result = [dict(zip(keys, row)) for row in result[1:]]
    return formatted_result

def contains_forbidden_string(result: dict, forbidden_strings: list) -> bool:
    """
    因为关系到是否会重复写入的问题，所以这块会检查入参的类型，虽然一般情况来说是字符串，但是不代表以后接口的结果不会变成其他格式 所以做了3种类型的兼容
    递归地检查对象（字典或列表）是否包含禁止的字符串。

    :param result: 要检查的对象（字典或列表、字符串）
    :param forbidden_strings: 禁止的字符串列表
    :return: 如果包含禁止的字符串，则返回 True；否则返回 False
    """
    if isinstance(result, dict):
        # 如果是字典，递归检查每个键值对
        for key, value in result.items():
            if isinstance(key, str) and any(forbidden_string in key for forbidden_string in forbidden_strings):
                return True
            if contains_forbidden_string(value, forbidden_strings):
                return True
    elif isinstance(result, list):
        # 如果是列表，递归检查每个元素
        for item in result:
            if contains_forbidden_string(item, forbidden_strings):
                return True
    elif isinstance(result, str):
        # 如果是字符串，检查是否包含禁止的字符串
        return any(forbidden_string in result for forbidden_string in forbidden_strings)
    # 对于其他类型不进行检查，直接给Ture
    return True

def num_to_base26(n):
    if n == 0:
        return "A"
    digits = []
    while n > 0:
        n, remainder = divmod(n - 1, 26)  # -1 because we want 'A' to be 1, 'Z' to be 26
        digits.append(chr(ord('A') + remainder))
    return ''.join(reversed(digits))

# 获取sheet_id
def post_sheet_name(sheets_list: list, sheet_name: str) -> str:
    """
    传入目标sheet_name，例如:主唤醒/免唤醒/ss2数据1/ss3数据1/ss2数据1.2
    :param sheets_list: 目标表的所有sheet_id
    :param sheet_name: 目标表的目标sheet名字
    :return sheet_id 例如 ZE2eTQ
    """
    for sheet in sheets_list:
        if sheet['title'] == sheet_name:
            sheet_id = sheet['sheet_id']
            return sheet_id
    raise ValueError(f"没有找到目标sheet表名: {sheet_name}")


# 获取tenant_access_token
def get_tenant_access_token() -> str:
    app_id = "cli_a54ae9ccb3b0500e"
    app_secret = "Th1kYjidPtLjfLRBWX0YVb4CV0dNJKfh"
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_Data = json.loads(response.text)
    tenant_access_token = json_Data['tenant_access_token']

    return tenant_access_token


# 一次性获取目标表的列名与内容
def get_document_content(tenant_access_token: str, sheet_id: str, token: str, range_str="A:BZ") -> str:
    """
    该接口返回数据的最大限制为 10 MB
    该接口不支持获取跨表引用和数组公式的计算结果。
    官方文档 https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/reading-a-single-range
    :param tenant_access_token: 验证应用身份的访问凭证
    :param sheet_id: 目标表的其中一个sheet的id
    :param token: 目标表的token，例如https://li.feishu.cn/sheets/SZvDs0xD8hdInSt7675caHiCnYe?sheet=9klzqi，这个表的token就是SZvDs0xD8hdInSt7675caHiCnYe
    :return
    """
    print(tenant_access_token, sheet_id, token)
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{token}/values/{sheet_id}!{range}?valueRenderOption=ToString"

    headers = {
        'Authorization': f'Bearer {tenant_access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.text

# 多次获取目标表的列名与内容
def get_document_content_again(tenant_access_token: str, sheet_id: str, token: str, row_count: int, range_str="A:BZ") -> str:
    start_col, end_col = range_str.split(':')
    letter_list = [start_col, end_col]
    column_numbers = [column_letter_to_number(letter) for letter in letter_list]
    n = column_numbers[1]
    range_list, formatted_result_list, pairs = [], [], []
    data_len = ""
    for i in range(1, n + 1):
        range_list.append(num_to_base26(i))
    for range1 in range_list:
        url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{token}/values/{sheet_id}!{range1}1:{range1}{row_count}?valueRenderOption=ToString"

        headers = {
            'Authorization': f'Bearer {tenant_access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            res_content = json.loads(response.content.decode('UTF-8'))
            if res_content.get("code", -1) == 0:
                print(range1, '读成功')
            else:
                print("出错了")
                exit()
        result = json.loads(response.text)
        result = result["data"]["valueRange"]["values"]
        #  在这里可以打印每列的值与列字母
        # print(len(result),range1)
        keys = result[0]
        formatted_result = [dict(zip(keys, row)) for row in result[1:]]
        formatted_result_list.append(formatted_result)
    merged_list = []
    for dicts in zip(*formatted_result_list):
        merged_dict = {}
        for d in dicts:
            merged_dict.update(d)
        merged_list.append(merged_dict)
    return merged_list

# 查询当前sheet中的列与行
def get_rows_and_columns(tenant_access_token: str, token: str, sheet_id: str) -> str:
    """
    参考官方文档 https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/:spreadsheet_token/sheets/:sheet_id
    :param token: 目标表的token，例如https://li.feishu.cn/sheets/SZvDs0xD8hdInSt7675caHiCnYe?sheet=9klzqi，这个表的token就是SZvDs0xD8hdInSt7675caHiCnYe
    :param sheet_id: 目标表的其中一个sheet的id
    :return
    """

    url = f'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{token}/sheets/{sheet_id}'
    headers = {
        'Authorization': f'Bearer {tenant_access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.text

def get_wiki_token(access_token, node_token, obj_type="wiki") -> str:
    url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?obj_type={obj_type}&token={node_token}"


    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.text

# 获取当前知识库页面的表格信息列表
def get_wiki_file(access_token: str, space_id_in_response: str, feishu_file_name: str) -> str:
    response_dic = json.loads(space_id_in_response)
    space_id = response_dic["data"]["node"]["space_id"]
    origin_node_token = response_dic["data"]["node"]["origin_node_token"]

    url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes?page_size=50&parent_node_token={origin_node_token}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    max_attempts = 4  # 最大尝试次数
    attempts = 0  # 当前尝试次数
    found_obj_token = False  # 是否找到文件
    page_token = None  # 分页令牌 出现在第一次调用返回的接口中

    while not found_obj_token and attempts < max_attempts:
        # 如果存在page_token，则将其添加到URL中
        url = f"{url}&page_token={page_token}" if page_token else url
        response = requests.get(url, headers=headers)
        # 检查请求是否成功
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.text}")
            return response.status_code

        response_dic = json.loads(response.text)
        for item in response_dic['data']['items']:
            if item['title'] == feishu_file_name:
                print(f"找到目标title: {item['title']}")
                obj_token = item['obj_token']
                print(f"obj_token: {obj_token}")
                found_obj_token = obj_token
                break

        # 如果没有找到目标，并且存在下一个页面的token，则继续请求
        if not found_obj_token and "page_token" in response_dic["data"]:
            page_token = response_dic["data"]["page_token"]

        attempts += 1
        if attempts == 4:
            print(f"尝试了4次，每次50条文档表格信息都没有找到 {feishu_file_name}")
    return found_obj_token


# 创建表格 文件夹需手动创建
def create_spreadsheet(tenant_access_token: str, spreadsheet_name: str, folder_token: str) -> str:
    """
    参考官方文档 https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet/create?appId=cli_a54ae9ccb3b0500e
    :param tenant_access_token: 验证应用身份的访问凭证
    :param spreadsheet_name: 表名
    :param folder_token: 文件夹token 例如 https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf中的GBSSfE0fel6X1xdE3ENcl02Nnqf
    :return
    """
    token = get_spreadsheet_token(tenant_access_token, spreadsheet_name, folder_token)
    if token:
        return f"表格{spreadsheet_name}已将创建，无需重新创建"
    url = f'https://open.feishu.cn/open-apis/sheets/v3/spreadsheets'

    data = {
        "title": spreadsheet_name,
        "folder_token": folder_token
    }

    headers = {
        'Authorization': f'Bearer {tenant_access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


# 创建sheet
def create_sheet(tenant_access_token: str, sheet_name: str, token: str) -> str:
    """
    参考官方文档 https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/operate-sheets
    :param tenant_access_token:
    :param sheet_name: 目标sheet名称
    :param token: 目标表的token，例如https://li.feishu.cn/sheets/SZvDs0xD8hdInSt7675caHiCnYe?sheet=9klzqi，这个表的token就是SZvDs0xD8hdInSt7675caHiCnYe
    :return {"code":0,"data":{"replies":[{"addSheet":{"properties":{"index":1,"sheetId":"44Otyw","title":"我是贝利亚123"}}}]},"msg":"success"}
    """
    sheets = get_sheet_id(tenant_access_token, token)
    for sheet in sheets:
        if sheet['title'] == sheet_name:
            return f"已经有{sheet_name}这张表了"

    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{token}/sheets_batch_update"

    data = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": sheet_name,
                        "index": 1
                    }
                }
            }
        ]
    }

    headers = {
        'Authorization': f'Bearer {tenant_access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


# 插入多条数据
def post_document(tenant_access_token: str, pd: dict, spreadsheet_name: str, folder_token: str, sheet_name: str,
                  column_list: list = None, ) -> str:
    """
    参考官方文档 https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/write-data-to-multiple-ranges
    :param tenant_access_token: 验证应用身份的访问凭证
    :param pd: 所需数据 格式：列表套字典
    :param spreadsheet_name: 表名
    :param folder_token: 文件夹token 例如 https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf中的GBSSfE0fel6X1xdE3ENcl02Nnqf
    :param sheet_name: sheet名字
    :param column_list 列名
    :return
    """
    token = get_spreadsheet_token(tenant_access_token, spreadsheet_name, folder_token)
    if token is None:
        create_spreadsheet(tenant_access_token, spreadsheet_name, folder_token)
        token = get_spreadsheet_token(tenant_access_token, spreadsheet_name, folder_token)
    create_sheet(tenant_access_token, sheet_name, token)
    sheets_list = get_sheet_id(tenant_access_token, token)
    sheet_id = post_sheet_name(sheets_list, sheet_name)
    result = get_document_content(tenant_access_token, sheet_id, token)
    result = contains_forbidden_string(result, forbidden_strings)
    if result:
        return f"表格已被标注过，禁止重新写入: 表格名是{spreadsheet_name}--->sheet名是{sheet_name}"

    if column_list == None:
        column_list = list(pd[0].keys())

    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{token}/values_batch_update/"
    Authorization_value = "Bearer " + tenant_access_token

    headers = {
        'Authorization': Authorization_value,
        'Content-Type': 'application/json'
    }
    data = {"valueRanges": [
        {
            "range": sheet_id,
            "values": [column_list]}
    ]}
    #
    # value_ranges = data["valueRanges"]
    # values_list = value_ranges[0]["values"]
    # for i in pd:
    #     value_data = list(i.values())
    #     value_data = [
    #         str(item) if isinstance(item, (Timestamp, bool)) else item
    #         for item in value_data
    #     ]
    #     values_list.append(value_data)
    #     # break
    # data["valueRanges"][0]["values"] = values_list
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response.text

# 追加数据
def append_data(tenant_access_token: str, pd: dict, spreadsheet_name: str, folder_token: str, sheet_name: str) -> str:
    """
    官方文档 https://open.feishu.cn/document/server-docs/docs/sheets-v3/data-operation/append-data
    :param tenant_access_token: 验证应用身份的访问凭证
    :param pd: 所需数据 格式：列表套字典
    :param spreadsheet_name: 表名
    :param folder_token: 文件夹token 例如 https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf中的GBSSfE0fel6X1xdE3ENcl02Nnqf
    :param sheet_name: sheet名字
    :return
    """
    print(tenant_access_token,spreadsheet_name,folder_token,sheet_name)
    try:
        token = get_spreadsheet_token(tenant_access_token, spreadsheet_name, folder_token)
        if token is None:
            create_spreadsheet(tenant_access_token, spreadsheet_name, folder_token)
            token = get_spreadsheet_token(tenant_access_token, spreadsheet_name, folder_token)
        create_sheet(tenant_access_token, sheet_name, token)
        sheets_list = get_sheet_id(tenant_access_token, token)
        sheet_id = post_sheet_name(sheets_list, sheet_name)
        result = get_document_content(tenant_access_token, sheet_id, token)
        result = contains_forbidden_string(result, forbidden_strings)
        post_document(tenant_access_token, pd, spreadsheet_name, folder_token, sheet_name)
        if result:
            return f"表格已被标注过，禁止重新写入: 表格名是{spreadsheet_name}--->sheet名是{sheet_name}"

        url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{token}/values_append?insertDataOption=OVERWRITE"
        Authorization_value = "Bearer " + tenant_access_token

        headers = {
            'Authorization': Authorization_value,
            'Content-Type': 'application/json'
        }

        batch_size = 100
        succeed_output, failed_output = 0, 0
        total_len = len(pd)
        start_time = time.time()
        if total_len > 0:
            for start in range(0, total_len, batch_size):
                end = min(start + batch_size, total_len)  # 确保 end 不超过 total_len
                batch_data = pd[start:end]  # 获取当前批次的数据

                values_list = []
                for item in batch_data:
                    value_data = list(item.values())
                    value_data = [
                        str(item) if isinstance(item, (Timestamp, bool)) else item
                        for item in value_data
                    ]
                    values_list.append(value_data)

                data = {"valueRange": {"range": sheet_id, "values": values_list}}
                response = requests.post(url, headers=headers, data=json.dumps(data))

                if response.status_code == 200:
                    res_content = json.loads(response.content.decode('UTF-8'))
                    if res_content.get("code", -1) == 0:
                        succeed_output += (end - start)  # 计算当前批次成功的条数
                        # print(start, end, len(batch_data), len(data["valueRange"]["values"]), "数据写入成功")
                    else:
                        print(f"后处理文件中第 {start} 到 {end - 1} 行出现写入云文档失败的情况，error_msg：{res_content}")
                        failed_output += (end - start)
                else:
                    print(
                        f"后处理文件中第 {start} 到 {end - 1} 行出现写入云文档失败的情况，响应状态码：{response.status_code}")
                    print("失败的数据: ", values_list)  # 直接打印失败数据内容
                    failed_output += (end - start)  # 计算当前批次失败的条数

            end_time = time.time()
            print("耗时：", end_time - start_time)

            print(
                f"飞书写入完毕，在线文档路径为：https://li.feishu.cn/sheets/{token}，sheet名：{sheet_name}，总计：{total_len}条，成功{succeed_output}条，失败{failed_output}条")
        else:
            return "数据量为0，无法写入"

    except Exception as e:
        print(e)


# 获取sheet_id
def get_sheet_id(tenant_access_token: str, token: str) -> list:
    """
    参考官方文档 https://open.feishu.cn/document/server-docs/docs/sheets-v3/spreadsheet-sheet/query?appId=cli_a54ae9ccb3b0500e
    :param tenant_access_token: 验证应用身份的访问凭证
    :param token: 目标表的token，例如https://li.feishu.cn/sheets/SZvDs0xD8hdInSt7675caHiCnYe?sheet=9klzqi，这个表的token就是SZvDs0xD8hdInSt7675caHiCnYe
    :return sheets_list: 目标表的所有sheet的id [e06ef5,ZE2eTQ]
    """
    url = f"https://open.feishu.cn/open-apis/sheets/v3/spreadsheets/{token}/sheets/query"
    Authorization_value = "Bearer " + tenant_access_token
    headers = {
        'Authorization': Authorization_value,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    sheets_list = []
    for sheet in data['data']['sheets']:
        sheets_list.append({
            'sheet_id': sheet['sheet_id'],
            'title': sheet['title']
        })

    return sheets_list


# 获取目标文件夹下表格的token
def get_spreadsheet_token(tenant_access_token: str, spreadsheet_name: str, folder_token: str) -> str:
    """
    本接口仅支持获取当前层级的文件信息，不支持递归获取子文件夹中的文件信息清单
    参考官方文档 https://open.feishu.cn/document/server-docs/docs/drive-v1/folder/list?appId=cli_a54ae9ccb3b0500e
    :param tenant_access_token: 验证应用身份的访问凭证
    :param spreadsheet_name: 表名
    :param folder_token: 文件夹token 例如 https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf中的GBSSfE0fel6X1xdE3ENcl02Nnqf
    :return
        {
            "code": 0,
            "data": {
                "files": [
                    {
                        "created_time": "1734942521",
                        "modified_time": "1734942549",
                        "name": "那我也黑化一下吧",
                        "owner_id": "ou_5323fbfc6b8e767d71df481e9687789e",
                        "parent_token": "GBSSfE0fel6X1xdE3ENcl02Nnqf",
                        "token": "JUP5sxPf0hGezAtYo3OcwEMNnWh",
                        "type": "sheet",
                        "url": "https://li.feishu.cn/sheets/JUP5sxPf0hGezAtYo3OcwEMNnWh"
                    }
        ],
        "has_more": false
    },
    "msg": "success"
}
    """
    if not tenant_access_token:
        raise ValueError("tenant_access_token 为空")

    url = f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={folder_token}"
    Authorization_value = "Bearer " + tenant_access_token
    headers = {
        'Authorization': Authorization_value,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    response_dict = json.loads(response.text)
    files = response_dict.get('data', {}).get('files', [])
    for file in files:
        if file['name'] == spreadsheet_name:
            return file['token']

    return None

# 普通表格读取
def common_read(access_token, feishu_file_name, feishu_folder_token):
    token = get_spreadsheet_token(access_token, feishu_file_name, feishu_folder_token)
    if token is None:
        create_spreadsheet(access_token, feishu_file_name, feishu_folder_token)
        token = get_spreadsheet_token(access_token, feishu_file_name, feishu_folder_token)

    create_sheet(access_token, feishu_sheet_name, token)
    sheets_list = get_sheet_id(access_token, token)
    sheet_id = post_sheet_name(sheets_list, feishu_sheet_name)
    result = get_document_content(access_token, sheet_id, token)
    print(result)

# 知识库表格读取
def knowledge_base_read(access_token, node_token, feishu_file_name):

    wiki_token_response = get_wiki_token(access_token, node_token)
    token = get_wiki_file(access_token, wiki_token_response, feishu_file_name)
    feishu_sheets_list = get_sheet_id(access_token, token)
    feishu_sheet_id = post_sheet_name(feishu_sheets_list, feishu_sheet_name)
    rows_columns_result = get_rows_and_columns(access_token, token, feishu_sheet_id)
    letter_columnpairs, row_count = number_to_column(
        rows_columns_result)  # 因为上一步返回的字典里包含的是数字，咱们需要数字与A B AA AB这种来做对应，因此有了这步
    result_pd = get_document_content_again(access_token, feishu_sheet_id, token, row_count,
                                           range_str=f"A:{letter_columnpairs}")  # range为了限制列数，不要拿多或拿少
    return result_pd

def init_arguments(str_task_name):
    parse = argparse.ArgumentParser(str_task_name)

    # 这里如果execute_sql有值直接取sql的内容
    parse.add_argument("--task_type", type=str, required=True, help="执行任务类型，目前支持read/write/edit三种类型")
    parse.add_argument("--feishu_folder_token", type=str,
                       help="飞书云文档文件所在的目录token， 默认值为'https://li.feishu.cn/drive/folder/CRr1fTUrflaXIBdunN6ckPQwnUb'",
                       default="CRr1fTUrflaXIBdunN6ckPQwnUb")
    parse.add_argument("--feishu_file_name", type=str, required=True, help="飞书云文档的文件名称")
    parse.add_argument("--feishu_sheet_name", type=str, required=True, help="飞书云文档的sheet名称")
    parse.add_argument("--input_path", type=str, default="",
                       help="执行任务类型为write时的源文件路径")
    parse.add_argument("--input_sheet_name", type=str, default="",
                       help="如果input_path为excel格式，该值表示input_path中的sheet_name，可以为空")

    return parse.parse_args()


if __name__ == "__main__":

    access_token = get_tenant_access_token()

    # task_name = "feishu_cloud_document_api"
    # args = init_arguments(task_name)
    # print(args)

    # task_type = args.task_type  # 可选项 write，edit，第一个是写入，第二个是修改
    # feishu_folder_token = args.feishu_folder_token  # 飞书云文档所在文件夹token eg. https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf 中 的GBSSfE0fel6X1xdE3ENcl02Nnqf
    # feishu_file_name = args.feishu_file_name    # 飞书云文档名 eg.20241226线上数据
    # feishu_sheet_name = args.feishu_sheet_name  # 飞书sheet名 eg. "ss2数据1"
    # input_path = args.input_path  # r"/mnt/pfs-guan-ssai/nlu/ota_user_data/car_annote/2025-01-02/2025-01-02_all_session_random_23.csv"
    # input_sheet_name = args.input_sheet_name

    # debug
    task_type = "write"  # 可选项 write，edit，第一个是写入，第二个是修改
    feishu_folder_token = "CRr1fTUrflaXIBdunN6ckPQwnUb"  # 飞书云文档所在文件夹token eg. https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf 中 的GBSSfE0fel6X1xdE3ENcl02Nnqf
    feishu_file_name = "20260101线上数据"    # 飞书云文档名 eg.20241226线上数据
    feishu_sheet_name = "Sheet1"  # 飞书sheet名 eg. "ss2数据1"
    input_path = r"D:\2486837177_112661\Downloads\2025-01-09_all.csv"  # r"/mnt/pfs-guan-ssai/nlu/ota_user_data/car_annote/2025-01-02/2025-01-02_all_session_random_23.csv"
    # input_sheet_name =


    # 直接调用这个接口 一键创建+写入
    if task_type in ['write', 'edit']:
        if input_path == "":
            print("当前任务为写入数据到飞书云文档，但input_path为空")
            exit()
        # 分割文件类型
        file_name, file_extension = os.path.splitext(input_path)
        if file_extension == '.xlsx':
            # 调用读取 Excel 文件的函数，可以稍微看下read_excel_sheet的实现方法与格式
            pd = read_excel_sheet(input_path, input_sheet_name)
            print("excel")
        elif file_extension == '.csv':
            # 调用读取 CSV 文件的函数，可以稍微看下read_pd_csv的实现方法与格式
            pd = read_pd_csv(input_path)
        elif file_extension == '.jsonl':
            # todo bugfix 未验证方法
            pd = read_jsonl(input_path)
        else:
            pd = []
            print("请确认输入文件类型，目前仅支持csv和xlsx")
            exit()
        print(access_token,pd[:2])
        append_data(access_token, pd, feishu_file_name, feishu_folder_token, feishu_sheet_name)

    if task_type in ["common_read", "knowledge_base_read"]:
        if task_type == "common_read":
            # 需要手动传参：access_token, feishu_folder_token, feishu_file_name
            feishu_folder_token = "CRr1fTUrflaXIBdunN6ckPQwnUb"  # 当前文件夹页面的标识,直接从网页上复制
            result_pd =  common_read(access_token, feishu_file_name, feishu_folder_token)

        elif task_type == "knowledge_base_read":
            # 需要手动传参：access_token,node_token，feishu_file_name
            node_token = "QiGIweNWviOTT4k1H9kcvY4Xnrd"  # 当前知识库页面的标识,直接从网页上复制
            result_pd = knowledge_base_read(access_token, node_token, feishu_file_name)
            # 能写入代表格式正确
            # append_data(access_token, result_pd, "20260101线上数据", feishu_folder_token, feishu_sheet_name)

