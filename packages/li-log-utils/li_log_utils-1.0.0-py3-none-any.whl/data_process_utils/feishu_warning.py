# -*- coding:utf-8 -*-
import sys

import requests
import json
import argparse


def get_daily_request(send_text, send_url=None, eval_task="test"):
    eval_result_list = []
    headers = {'Content-Type': 'application/json'}
    if send_url is None or send_url == "":
        return '请配置url'

    request_data = {
        "eval_task": eval_task,
        "msg_type": "text",
        "content": {"text": str(send_text)}
    }
    response = requests.request("POST", send_url, headers=headers, json=request_data)
    try:
        response_data = json.loads(response.text)
        eval_result_list.append(response_data)
    except Exception as e:
        print("ERROR while eval_run:{},task".format(e, request_data['eval_task']))

    return eval_result_list


if __name__ == "__main__":

    # warning_text = "我在debug"
    # task_name = "test"
    # url = "https://open.feishu.cn/open-apis/bot/v2/hook/e88a9592-27d8-4e85-a224-3b8ec2a8b49e"
    # res = get_daily_request(warning_text, url)

    parse = argparse.ArgumentParser("information")
    parse.add_argument("--warning_text", default="报警！汪汪汪！！！", type=str)
    parse.add_argument("--eval_task", default="test", type=str)
    parse.add_argument("--send_url", default="", type=str)
    args = parse.parse_args()

    warning_text = args.warning_text
    url = args.send_url
    task_name = args.eval_task
    # print(warning_text)
    # print(url)
    # print(task_name)
    res = get_daily_request(warning_text, url, task_name)


