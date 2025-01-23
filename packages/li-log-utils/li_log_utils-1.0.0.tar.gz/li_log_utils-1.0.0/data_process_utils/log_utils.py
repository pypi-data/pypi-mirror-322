import csv

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


# ===========================
# 读文件
# ===========================
def read_excel_sheet(file_name, sheet_name):
    df = pd.read_excel(file_name, sheet_name, keep_default_na=False)
    list_data = np.array(df).tolist()
    objs = []
    field_names = list(df.columns)
    for fields in list_data:
        obj = {}
        for i in range(len(field_names)):
            obj[field_names[i]] = fields[i]
        objs.append(obj)
    return objs


def read_pd_csv(file_name, use_cols=None):
    if use_cols is None:
        df = pd.read_csv(file_name, keep_default_na=False, engine='python', encoding='utf-8')
    else:
        df = pd.read_csv(file_name, usecols=use_cols, keep_default_na=False, engine='python', encoding='utf-8')
    list_data = df.values.tolist()
    objs = []
    field_names = list(df.columns)
    for fields in list_data:
        obj = {}
        for i in range(len(field_names)):
            obj[field_names[i]] = fields[i]
        objs.append(obj)
    return objs


def read_json(path: str) -> Dict:
    with open(path, "r", encoding="utf-8-sig") as fi:
        return json.load(fi)


def read_lines(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8-sig") as fi:
        lines = fi.readlines()
    return [line.rstrip('\n') for line in lines]


def read_jsonl(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8-sig") as fi:
        lines = fi.readlines()
        lines = [line.strip('\n') for line in lines]
        try:
            lines = [json.loads(line) for line in lines]
        except:
            print("jsonl解析异常")
            lines = []
    return lines


def save_csv(head_list, obj, path, sep=",", sort_columns=None, unique_columns=None):
    data = pd.DataFrame(obj, columns=head_list)
    if sort_columns is not None:
        data = pd.DataFrame(obj, columns=head_list)
        # 按时间排序
        data = data.sort_values(by=sort_columns, ascending=[True]*len(sort_columns))

    if unique_columns is not None:
        # 保留最后一条
        data = data.drop_duplicates(subset=unique_columns, keep='last')
    data_dict_list = data.to_dict(orient='records')
    # 使用 with open 语句打开文件，并使用 csv.DictWriter 写入数据
    with open(path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=head_list)
        writer.writeheader()
        for row in data_dict_list:
            writer.writerow(row)
    # data.to_csv(path, sep=sep, header=head_list, index=False, encoding="utf-8-sig")


def save_json(obj: Any, path: str) -> str:
    with open(path, 'w', encoding="utf-8-sig") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2))
    return path


def save_jsonl(obj: Any, path: str) -> str:
    with open(path, 'w', encoding="utf-8-sig") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2))
    return path


def save_lines(obj, path):
    with open(path, 'w', encoding="utf-8-sig") as f:
        f.writelines(obj)
    return path


# ===========================
# 处理字符串
# ===========================
def is_contain_chinese(strs):
    """
    判断字符串中是否包含中文字符
    """
    p = re.compile("[\u4e00-\u9fa5]")
    res_p = re.findall(p, strs)
    if len(res_p) == 0:
        return False
    else:
        return True


def deep_update(dict1, dict2):
    for key, value in dict2.items():
        if isinstance(value, dict):
            dict1[key] = deep_update(dict1.get(key, {}), value)
        else:
            dict1[key] = dict1.get(key, 0) + value
    return dict1


def convert_df_to_dict_list(df):
    list_data = df.values.tolist()
    objs = []
    field_names = list(df.columns)
    for fields in list_data:
        obj = {}
        for i in range(len(field_names)):
            obj[field_names[i]] = fields[i]
        objs.append(obj)
    return objs


# ============================
# 处理日期函数
# is_time_in_range 和 is_time_between_range 需要合并
# ============================
def is_time_in_range(input_time_str, start_time_str):
    """
    判断当前时间是否在特定时间范围
    :param input_time_str:
    :param start_time_str:
    :return:
    """
    # 定义时间的格式
    time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串转换为datetime对象
    input_time = datetime.strptime(input_time_str, time_format)
    start_time = datetime.strptime(start_time_str, time_format)

    # 比较时间
    if start_time <= input_time:
        return True
    else:
        return False


def is_time_between_range(input_time_str, start_time_str, end_time_str=None):
    """
    判断当前时间是否在特定时间范围
    :param input_time_str: 待判断的时间
    :param start_time_str: 时间范围-起始时间
    :param end_time_str:   时间范围-结束时间
    :return: 待判断的时间是否在时间范围内
    """
    # 定义时间的格式
    time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串转换为datetime对象
    input_time = datetime.strptime(input_time_str, time_format)
    start_time = datetime.strptime(start_time_str, time_format)

    if end_time_str is not None:
        end_time = datetime.strptime(end_time_str, time_format)
        if start_time <= input_time <= end_time:
            return True
        else:
            return False
    else:
        # 比较时间
        if start_time <= input_time:
            return True
        else:
            return False


def get_data_list(start_date, end_date):
    """
    :param start_date: 起始日期
    :param end_date:   结束日期
    :return: 返回起始日期和结束日期之间的所有dt日期数据
    """
    # 将字符串转换为日期对象
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # 生成日期范围
    date_range = [(start_date + relativedelta(days=x)) for x in range((end_date - start_date).days + 1)]

    # 打印所有日期
    date_list = []
    for date in date_range:
        date_list.append(date.strftime('%Y-%m-%d'))
    return date_list


if __name__ == '__main__':
    pass
    # 测试范围
    # print(is_time_in_range("2024-09-30 11:12:30", "2024-09-30 22:00:00"))
    # print(is_time_in_range("2024-09-30 23:12:30", "2024-09-30 22:00:00"))
    # exit()

