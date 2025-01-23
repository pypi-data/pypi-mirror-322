import os
import logging

import json
import pandas as pd

from data_process_utils.log_utils import *

logging.info("加载配置文件")
sys_dlr = os.path.join(os.path.dirname(os.path.abspath(__file__)).split("mindgpt_dataloop_common_tools")[0],
                       "mindgpt_dataloop_common_tools")
# print(sys_dlr)
config_dict = read_json(os.path.join(sys_dlr, "conf", "log_config.conf"))


# "<|kvs|>": "[unused2]",
# "<|kve|>": "[unused3]",
# "<|api_start|>": "[unused4]",
# "<|api_end|>": "[unused5]",
# "<|eoa|>": "[unused6]",
# "=>": "[unused7]"
def clean_pattern(str_item):
    str_item = str_item.replace("[unused2]", "[")
    str_item = str_item.replace("[unused3]", " ")

    str_item = str_item.replace("[unused7]", "]")
    str_item = str_item.replace("[unused4]", " ")
    str_item = str_item.replace("[unused6]", " ")

    str_item = str_item.replace("[unused5]", " ")
    return str_item


def clean_api_pattern(pattern_list):
    api_pattern_list = []
    for item in pattern_list:
        item = clean_pattern(item)
        if item.count("APINAME") > 1:
            # case:  [APINAME]AUTOSearch [CATEGORY]汽车 [QUERY]理想L9简介 [TAG]理想L9&简介   [APINAME]AUTOSearch [CATEGORY]汽车 [QUERY]理想ONE简介 [TAG]理想ONE&简介
            api_list = item.strip().split("[APINAME]")
            for api_item in api_list:
                # 多api处理
                api_item = format_api_label_multi(api_item)
                if api_item != {}:
                    api_pattern_list.append(api_item)
        else:
            # 单api处理
            item = format_api_label(item)
            if item != {}:
                api_pattern_list.append(item)

    return api_pattern_list


def clean_thought_pattern(pattern_list):
    thought_pattern_list = []
    for item in pattern_list:
        item = clean_pattern(item)
        if item != "<None>":
            item = {"thought": item}
            thought_pattern_list.append(item)

    return thought_pattern_list


def clean_observation_pattern(pattern_list):
    clean_pattern_list = []
    for item in pattern_list:
        observation_sub_list = re.findall("\[unused2\](.*?)\[unused3\]", item.strip())
        # json解析的兼容处理一直感觉没有统一起来
        for osl in observation_sub_list:
            try:
                osl = json.loads(osl)
            except:
                if '""' in osl:
                    osl = osl.replace('""', '"')
                try:
                    osl = json.loads(osl)
                except:
                    osl = {}
            clean_pattern_list.append(osl)
    # re.findall("\[unused0\]thought(.*?)\[unused1\]", llm_input.replace("\n", ""))
    return clean_pattern_list


def format_api_label(str_label):
    tokens, slots = pre_process_input(str_label)

    skill_domain_dict = dict()
    for index in range(min(len(tokens), len(slots))):
        skill_domain_dict[tokens[index]] = slots[index]
    return skill_domain_dict


def format_api_label_multi(str_label):
    if str_label.replace(" ", "") == "":
        return {}
    tokens, slots = pre_process_input("[APINAME]" + str_label)
    skill_domain_dict = dict()
    for index in range(min(len(tokens), len(slots))):
        skill_domain_dict[tokens[index]] = slots[index]
    return skill_domain_dict


def extra_api_thought_observation_13b(str_llm_input):
    str_thought, str_api, str_observation = [], [], []

    # str_llm_input = str_llm_input.replace("[unused0] thought", "[unused0]thought")
    if "[unused0]thought" in str_llm_input:
        str_thought = re.findall("\[unused0\]\s*thought(.*?)\[unused1\]", str_llm_input.replace("\n", ""))
        str_thought = clean_thought_pattern(str_thought)

    # str_llm_input = str_llm_input.replace("[unused0] api", "[unused0]api")
    if "[unused0]api" in str_llm_input:
        str_api = re.findall("\[unused0\]\s*api(.*?)\[unused1\]", str_llm_input.replace(" ", "").replace("\n", ""))
        str_api = clean_api_pattern(str_api)

    # str_llm_input = str_llm_input.replace("[unused0] observation", "[unused0]observation")
    if "[unused0]observation" in str_llm_input:
        str_observation = re.findall("\[unused0\]\s*observation(.*?)\[unused1\]", str_llm_input.replace("\n", ""))
        str_observation = clean_observation_pattern(str_observation)

    return str_thought, str_api, str_observation


def extra_api_thought_observation_1b(str_llm_input):
    """
    1b function call升级后 兼容api/thought/obs 提取字段
    :param str_llm_input: model_1b_input
    """
    str_api, str_thought, str_observation = [], [], []
    if str_llm_input != '':
        str_llm_input = json.loads(str_llm_input)

    if isinstance(str_llm_input, list):
        str_llm_input = {"tools": str_llm_input}  # 新字段
    elif isinstance(str_llm_input, dict) and "tools" in str_llm_input:
        pass  # 符合预期旧字段
    else:
        if str_llm_input is None or str_llm_input == "":
            return [], [], []
        else:
            print("pls check: [1b 字段解析]", str_llm_input)
            return [], [], []

    if isinstance(str_llm_input["tools"], list):
        for tool in str_llm_input['tools']:
            # APINAME
            if 'function' in tool and 'name' in tool['function']:
                name_value = tool['function']['name']

                tool['function']['APINAME'] = name_value
                del tool['function']['name']

            function_data = tool['function']

            if 'arguments' in function_data and function_data['arguments'] != '':
                arguments = json.loads(function_data['arguments'])
                if 'category' in arguments:
                    arguments['CATEGORY'] = arguments['category'].upper()
                    del arguments['category']
                if 'tag' in arguments:
                    arguments['TAG'] = arguments['tag'].upper()
                    del arguments['tag']
                if 'query' in arguments:
                    arguments['QUERY'] = arguments['query'].upper()
                    del arguments['query']
                if tool["function"].get("APINAME", "UNK") != "UNK":
                    arguments["APINAME"] = tool["function"]["APINAME"]
                function_data['arguments'] = arguments
            else:
                if tool["function"].get("APINAME", "UNK") != "UNK":
                    function_data['arguments'] = {"APINAME": tool["function"]["APINAME"]}

        functions = [tool["function"] for tool in str_llm_input["tools"]]
        for func in functions:
            str_api.append(func["arguments"])
            str_thought.append({"thought": func['thought']})
    else:
        return [], [], []

    return str_thought, str_api, str_observation


# ======================== function Call 升级 =============================
def clean_functioncall_pattern(pattern_list, str_type):
    # 因为涉及到多步function 所以层级关系保持一致

    if str_type == "api_thought":
        thought_list, api_list = [], []
        for item in pattern_list:
            json_item = json.loads(item)[0]
            thought_list.append(json_item.get("thought", ""))
            pattern_api = {"apiname": json_item.get("name", {})}
            pattern_api.update(json_item.get("arguments", {}))
            pattern_api = {key.upper(): value for key, value in pattern_api.items()}
            api_list.append(pattern_api)

        return thought_list, api_list

    elif str_type == "obs":
        obs_list = []
        for item in pattern_list:
            json_item = json.loads(item)[0]
            obs_list.append(json_item)
        return obs_list


def extra_api_thought_observation_13b_functioncall(str_llm_input):
    str_thought, str_api, str_observation = [], [], []

    if "[truncated]" in str_llm_input:
        return str_thought, str_api, str_observation

    # API/thought解析
    str_api_thought = re.findall("\[unused0\]\s*assistant\s*```\s*function_call(.*?)```\s*\[unused1\]", str_llm_input.replace("\n", ""))
    str_thought, str_api = clean_functioncall_pattern(str_api_thought, "api_thought")

    # Obs解析
    str_observation = re.findall("\[unused0\]\s*user\s*```\s*function_call_result(.*?)```\s*\[unused1\]", str_llm_input.replace("\n", ""))
    str_observation = clean_functioncall_pattern(str_observation, "obs")

    return str_thought, str_api, str_observation


def extra_api_thought_observation_1b_functioncall(str_llm_input):
    """
    1b function call升级后 兼容api/thought/obs 提取字段
    :param str_llm_input: model_1b_input
    """
    str_api, str_thought, str_observation = [], [], []
    if str_llm_input != '':
        str_llm_input = json.loads(str_llm_input)

    if isinstance(str_llm_input, list):
        str_llm_input = {"tools": str_llm_input}  # 新字段
    elif isinstance(str_llm_input, dict) and "tools" in str_llm_input:
        pass  # 符合预期旧字段
    else:
        if str_llm_input is None or str_llm_input == "":
            return [], [], []
        else:
            print("pls check: [1b 字段解析]", str_llm_input)
            return [], [], []

    if isinstance(str_llm_input["tools"], list):
        for tool in str_llm_input['tools']:
            # APINAME
            if 'function' in tool and 'name' in tool['function']:
                name_value = tool['function']['name']

                tool['function']['APINAME'] = name_value
                del tool['function']['name']

            function_data = tool['function']

            if 'arguments' in function_data and function_data['arguments'] != '':
                arguments = json.loads(function_data['arguments'])
                if 'category' in arguments:
                    arguments['CATEGORY'] = arguments['category'].upper()
                    del arguments['category']
                if 'tag' in arguments:
                    arguments['TAG'] = arguments['tag'].upper()
                    del arguments['tag']
                if 'query' in arguments:
                    arguments['QUERY'] = arguments['query'].upper()
                    del arguments['query']
                if tool["function"].get("APINAME", "UNK") != "UNK":
                    arguments["APINAME"] = tool["function"]["APINAME"]
                function_data['arguments'] = arguments
            else:
                if tool["function"].get("APINAME", "UNK") != "UNK":
                    function_data['arguments'] = {"APINAME": tool["function"]["APINAME"]}

        functions = [tool["function"] for tool in str_llm_input["tools"]]
        for func in functions:
            str_api.append(func["arguments"])
            str_thought.append({"thought": func['thought']})
    else:
        return [], [], []

    return str_thought, str_api, str_observation
# ======================== function Call 升级 =============================


def pre_process_input(str_text):
    """
    格式化数据处理 将[xx] xx [xx] xx 格式的数据 提取出来
    :param str_text:
    :return:
    """
    input_ = str_text.replace(" ", "")
    tokens = re.findall(r'\[((?:.|\n)*?)\]', input_)

    for x in tokens:
        x = "[" + x + "]"
        input_ = input_.replace(x, " ")
    input_ = input_.strip()
    slots = input_.split(" ")
    return tokens, slots


def format_topic_t5_label(str_label):
    """
    TopicT5 归档模型 label处理
    :param str_label:
    :return:
    """
    str_label = str_label.replace("[CLASSIFICATION]", "").replace("[CLS]", "")
    tokens, slots = pre_process_input(str_label)

    skill_domain_dict = dict()
    for index in range(min(len(tokens), len(slots))):
        skill_domain_dict[tokens[index]] = slots[index]

    return skill_domain_dict


def append_each_turn_v2(sess, query, ans):
    if ans.strip().lower() not in ['', 'nan']:
        sess.append({
            "user": query, "assistant": ans
        })
    return sess


def convert_input2session(model_input, mode="13b"):
    if "函数调用" in model_input and "[truncated]" in model_input:
        return []

    model_sess = list()

    if mode == "13b":
        pattern = r'\[unused0\]user\s*(.*?)\s*\[unused1\]\s*\[unused0\]assistant\s*(.*?)\s*\[unused1\]'
        re_res = re.findall(pattern, model_input, re.DOTALL)
        for ec in re_res:
            model_sess.append({"user": ec[0], "assistant": ec[1]})
    else:
        # todo 待适配
        return model_sess

    return model_sess


def format_session_context_list_v2(input_log_sess, input_1b, input_13b, input_data_mode=None, output_mode=None):
    """
    mode 用于适配输出的结果
    """
    if '{' in input_log_sess:
        try:
            input_log_sess = json.loads(input_log_sess)
        except:
            # 超长session 被截断 无法解析
            input_log_sess = []
    else:
        input_log_sess = []
    log_sess = []
    for log_item in input_log_sess[::-1]:
        log_sess.append({
            "user": log_item.get("input_text", ""),
            "assistant": log_item.get("output_text", "")
        })

    model_1b_sess = convert_input2session(input_1b, "1b")
    model_13b_sess = convert_input2session(input_13b, "13b")

    if input_data_mode == "1b":
        session_context_list = model_1b_sess
    elif input_data_mode == "13b":
        session_context_list = model_13b_sess
    elif input_data_mode == "sessionContext":
        # 需要倒序 + 字段精简
        session_context_list = log_sess
    else:
        max_len = max(len(log_sess), len(model_1b_sess), len(model_13b_sess))
        if len(log_sess) == max_len:
            session_context_list = log_sess
        elif len(log_sess) == model_1b_sess:
            session_context_list = model_1b_sess
        else:
            session_context_list = model_13b_sess

    if output_mode == "str":
        manu_session_str = ""
        for item in session_context_list:
            manu_session_str += "user:" + item.get("user", "") + "\n"
            manu_session_str += "assistant:" + item.get("assistant", "") + "\n" + "\n"
        return manu_session_str.strip()
    else:
        return json.dumps(session_context_list, ensure_ascii=False)


def format_session_context_json(str_format_session_list):
    manu_session_json = []
    try:
        format_list_str_session_context_list = json.loads(str_format_session_list)
    except:
        format_list_str_session_context_list = []

    for item in format_list_str_session_context_list[::-1]:
        manu_session_json.append({
            "user": item.get("input_text", ""),
            "assistant": item.get("output_text", "")
        })

    return manu_session_json


def get_api_thought_observation(str_domain,
                                str_model_1b_output,
                                str_model_13b_input,
                                str_knowledge_search_result=None):
    """
    根据链路提取出1b/13b对应链路的关键信息
    :param str_domain: query落域
    :param str_model_1b_output: 1b输出
    :param str_model_13b_input: 16b输入
    :param str_knowledge_search_result:  可选
    # :param gpt_domain: 可选
    :return:
    """
    # config_dict = log_config_conf()
    gpt_domain = config_dict.get("gpt_domain", [])

    # 字段兼容
    if str_knowledge_search_result is None:
        str_knowledge_search_result = ""

    if str_domain in gpt_domain:
        # API Observation Thought
        if "{" in str_model_1b_output:
            thought_1b, api_1b, observation_1b = extra_api_thought_observation_1b(str_model_1b_output)
        else:
            thought_1b, api_1b, observation_1b = extra_api_thought_observation_13b(str_model_1b_output)
        thought_13b, api_13b, observation_13b = extra_api_thought_observation_13b(str_model_13b_input)

        if str_domain == "gpt_paintingmaster":
            api = api_1b
            thought = thought_1b
            observation = []
        else:
            if "charasearch" in str(api_1b).lower() or \
                    ("none" in str(api_1b).lower() and str_knowledge_search_result != ""):
                api = api_1b
                thought = thought_1b
                observation = str_knowledge_search_result  # 业务原因是由于人设有部分是通过知识库匹配的
            elif "mathqa" in str(api_1b).lower() or "todrequest" in str(api_1b).lower():
                api = api_1b
                thought = thought_1b
                observation = []
            elif ('autosearch' in str(api_1b).lower() or 'autosearch' in str(api_13b).lower()) \
                    or ("qasearch" in str(api_1b).lower() or "qasearch" in str(api_13b).lower()) \
                    or "mediasearch" in str(api_1b).lower() or "mediasearch" in str(api_13b).lower():
                api = api_13b
                thought = thought_13b
                observation = observation_13b
            else:
                api = api_13b
                thought = thought_13b
                observation = observation_13b
    else:
        api, observation, thought = [], [], []

    return api, observation, thought


def get_api_thought_observation_functioncall(str_domain,
                                             str_model_1b_output,
                                             str_model_13b_input,
                                             str_knowledge_search_result=None):
    """
    根据链路提取出1b/13b对应链路的关键信息
    :param str_domain: query落域
    :param str_model_1b_output: 1b输出
    :param str_model_13b_input: 16b输入
    :param str_knowledge_search_result:  可选
    :param gpt_domain: 可选
    :return:
    """
    # config_dict = log_config_conf()
    gpt_domain = config_dict.get("gpt_domain", [])

    # 字段兼容
    if str_knowledge_search_result is None:
        str_knowledge_search_result = ""

    if str_domain in gpt_domain:
        # API Observation Thought
        if "{" in str_model_1b_output:
            thought_1b, api_1b, observation_1b = extra_api_thought_observation_1b(str_model_1b_output)
        else:
            thought_1b, api_1b, observation_1b = extra_api_thought_observation_13b(str_model_1b_output)

        thought_13b, api_13b, observation_13b = extra_api_thought_observation_13b_functioncall(str_model_13b_input)

        if str_domain == "gpt_visionqa":
            api = [{"APINAMME": "visionqa"}]
            thought = ""
            observation = []
        elif str_domain == "gpt_paintingmaster":
            api = api_1b
            thought = thought_1b
            observation = []
        else:
            if "[truncated]" in str_model_13b_input:
                api = api_1b
                thought = thought_1b
                observation = []   # 异常数据
            elif "charasearch" in str(api_1b).lower() or \
                    ("none" in str(api_1b).lower() and str_knowledge_search_result != ""):
                api = api_1b
                thought = thought_1b
                observation = str_knowledge_search_result  # 业务原因是由于人设有部分是通过知识库匹配的
            elif "mathqa" in str(api_1b).lower() or "todrequest" in str(api_1b).lower():
                api = api_1b
                thought = thought_1b
                observation = []
            elif ('autosearch' in str(api_1b).lower() or 'autosearch' in str(api_13b).lower()) \
                    or ("qasearch" in str(api_1b).lower() or "qasearch" in str(api_13b).lower()) \
                    or "mediasearch" in str(api_1b).lower() or "mediasearch" in str(api_13b).lower():
                api = api_13b
                thought = thought_13b
                observation = observation_13b
            else:
                api = api_13b
                thought = thought_13b
                observation = observation_13b
    else:
        api, observation, thought = [], [], []

    return api, observation, thought


def get_task_label(data_item, str_error_status=None, str_safe_status=None):
    # 车端task_label
    # # 异常流量（暂时不让他们影响其他逻辑判断）
    # if str_error_status is None:
    #     data_status, error_type = get_log_exception_status(data_item, "phone")
    #     if data_status is False:
    #         task_label += "异常流量待确认:" + error_type + ";"
    # else:
    #     if str_error_status != "":
    #         task_label += "异常流量待确认:" + str_error_status + ";"

    str_domain = data_item.get("domain", "").lower()
    if str_safe_status is None:
        str_input_safe_detect_info = data_item.get("input_safe_detect_info", "")
        str_input_safe_labels = data_item.get("input_safe_labels", "")
        str_safe_status = get_safe_label(str_domain, str_input_safe_detect_info, str_input_safe_labels)

    if str_safe_status != "":
        task_label = str_safe_status
        return task_label

    str_domain_li = data_item.get("domain_li", "")
    str_model_1b_output = data_item.get("model_1b_output", "")
    str_model_13b_input = data_item.get("model_13b_input", "")

    chara_hit1 = str_domain == "gpt_chat" and "chara" in str_model_1b_output.lower()
    chara_hit2 = str_domain == 'chat' and str_domain_li == 'chat'
    chara_hit3 = str_domain == 'gpt_chat' and 'none' in str_model_1b_output.lower() and str_domain_li == 'chat'
    chara_hit4 = str_domain == "gpt_chat" and "禁止声称自己没有人类的情感" in str_model_13b_input

    if chara_hit1 or chara_hit3 or chara_hit4:
        task_label = '大模型-理想同学人设'
        return task_label
    if chara_hit2:
        task_label = '闲聊-理想同学人设'
        return task_label

    translate_hit = str_domain == "gpt_chat" and str_domain_li == 'translation'
    if translate_hit:
        task_label = '大模型-翻译'
        return task_label

    elif str_domain in config_dict["gpt_domain"]:
        if str_domain == "gpt_paintingmaster":
            task_label = "绘画大师"
        elif str_domain == "gpt_visionqa":
            task_label = "OV"
        elif str_domain == "gpt_autoqa":
            task_label = "汽车问答-RAG"
        else:
            # print("API")  # 字段
            list_api = data_item.get("API", "")
            str_content = data_item.get("content", "")
            str_slot_li = data_item.get("slot_li", "")
            str_content = str_slot_li if str_content == "" else str_content
            if len(list_api) == 0:
                if (str_model_1b_output == "" and str_model_13b_input == "") and str_content != "":
                    task_label = ""
                    if "qasearch" in str_content.lower():
                        if "价值观" in str_content.lower():
                            task_label += '安全'
                        elif "涉政" in str_content.lower():
                            task_label += '安全'
                        elif "舆情" in str_content.lower():
                            task_label += '安全'
                        else:
                            task_label = "链路字段待确认;"
                            task_label += '通用问答-RAG'
                    else:
                        task_label = "链路字段待确认;"
                        if "charasearch" in str_content.lower():
                            task_label += '大模型-理想同学人设'
                        elif "mediasearch" in str_content.lower():
                            task_label += '娱乐助手-RAG'
                        elif "autosearch" in str_content.lower():
                            task_label += '汽车问答-RAG'
                        elif "mathqa" in str_content.lower():
                            task_label += "大模型-数学"
                        elif "politicsearch" in str_content.lower():
                            task_label += '安全-一般涉政'
                        else:
                            task_label += "其他APINAME"
                else:
                    task_label = "通用问答-非RAG"
            else:
                if "charasearch" in str(list_api).lower():
                    task_label = '大模型-理想同学人设'
                elif "mediasearch" in str(list_api).lower():
                    task_label = "娱乐助手-RAG"
                elif "autosearch" in str(list_api).lower():
                    task_label = "汽车问答-RAG"
                elif "qasearch" in str(list_api).lower():
                    if list_api[0].get("CATEGORY", "") in ["国家", "城市", "景点", "出游美食", "旅游", "城市景点推荐", "交通出行"]:
                        task_label = "出游助手-RAG"
                    elif list_api[0].get("CATEGORY", "") in ["体育", "新闻", "音乐", "影视"]:
                        task_label = "娱乐助手-RAG"
                    else:
                        task_label = "通用问答-RAG"
                elif "meituansearch" in str(list_api).lower():
                    task_label = "出游助手-RAG"
                elif "mathqa" in str(list_api).lower():
                    task_label = "大模型-数学"
                elif "todrequest" in str(list_api).lower():
                    task_label = "通用问答-TodRequest"
                elif "politicsearch" in str(list_api).lower():
                    task_label = "安全-一般涉政"
                else:
                    if str_model_13b_input != "":
                        if len(list_api) == 0:
                            task_label = "通用问答-非RAG"
                        elif "comparenumber" in str(list_api).lower():
                            task_label = "通用问答-RAG"
                        elif "reject" in str(list_api).lower() \
                                or "visionqa" in str(list_api).lower() \
                                or "aipainting" in str(list_api).lower():
                            task_label = "通用问答-非RAG"
                        elif "count_string" in str(list_api).lower() \
                                or "get_string_length" in str(list_api).lower() \
                                or "reverse_string" in str(list_api).lower():
                            task_label = "自建code"
                        else:
                            # 未收录的 APINAME
                            print("未收录的 APINAME:", list_api)
                            task_label = "APINAME链路字段待确认，暂未在已知范围里; 通用问答-非RAG"
                    else:
                        task_label = "通用问答-13b-empty"
    else:
        if str_domain == "taskmaster":
            task_label = "任务大师"
        elif str_domain == "in_car_assistant":
            task_label = "汽车问答-服务专家"
        elif str_domain in ["", "null"]:
            task_label = "拒识"
        elif str_domain in config_dict.get("aispeech_domain", []):
            task_label = "三方-思必驰"
        elif str_domain in config_dict.get("free_domain", []):
            task_label = "自由对话"
        elif str_domain in config_dict.get("accessibility_domain", []):
            task_label = "可见即可说"
        else:
            if "," in str_domain:
                task_label = "多任务"
            else:
                print("domain链路字段待确认，暂未在已知范围里", str_domain)
                task_label = f"domain链路字段待确认，暂未在已知范围里{str_domain}"

    return task_label


# todo 待确认
def get_car_task_label_service(str_domain, input_safe_detect_info, input_safe_labels):
    # livis 专属干预服务判断链路
    if str_domain in ["system"] or str_domain in config_dict["gpt_domain"]:
        if str(input_safe_detect_info) != "SDS_SAFE":
            task_label = "干预服务-安全"
            return task_label

    if input_safe_labels != "" and input_safe_labels != "安全":
        task_label = "干预服务"
        return task_label

    return ""


def get_knowledge_detail_from_knowledge_search_result(str_knowledge_search_result):
    # ===== start ===== 对knowledge_search_result进行解析 ==========
    if "{" in str_knowledge_search_result:
        try:
            knowledge_search_result = json.loads(str_knowledge_search_result)
        except:
            try:
                knowledge_search_result = eval(str_knowledge_search_result)
            except:
                print("knowledge_search_result解析异常, 被截断, 无法json.loads")
                knowledge_search_result = []
    else:
        knowledge_search_result = []

    knowledge_search_list = []
    for ksr_item in knowledge_search_result:
        try:
            if "knowledge_search_data" in ksr_item:
                # 旧版 knowledge_search_data
                knowledge_search_list += ksr_item.get("knowledge_search_data", {}).get("bot_data", [])
            elif "media_search_datas" in ksr_item:
                # media_search_data
                knowledge_search_list += ksr_item.get("media_search_datas", [])
            elif "data" in ksr_item:
                # function_call 格式
                for sub_ksr_item in ksr_item["data"]:
                    knowledge_search_list += sub_ksr_item.get("bot_data", [])
            else:
                knowledge_search_list += []
        except:
            knowledge_search_list += []

    knowledge_list = []
    for item in knowledge_search_list:
        if item.get("content", "[unk]") != "[unk]":
            content = item["content"]
            knowledge_list.append(content)
    # ===== end ===== 对knowledge_search_result进行解析 ===============

    return knowledge_list


def get_knowledge_detail_from_observation(str_observation):
    # ===== start ===== 对obs 进行解析 ===============
    obs_knowledge_list = []
    for item in str_observation:
        if isinstance(item, Dict):
            if "search_query" in str(str_observation):
                for sub_item in item["content"]:
                    if isinstance(sub_item, Dict):
                        for subsub_item in sub_item["search_result"]:
                            obs_knowledge_list.append(subsub_item["content"])
                    else:
                        print()

            elif "content" in str(str_observation):
                obs_knowledge_list += item["content"]
            else:
                print()
        else:
            for sub_item in item:
                obs_knowledge_list += sub_item
    # ===== end ===== 对obs 进行解析 ===============
    return obs_knowledge_list


def get_knowledge_detail(str_knowledge_search_result,
                         str_observation,
                         rid=None, type=None):
    """
    从搜索结果中格式化处理 knowledge/media搜索结果
    :param rid: 用于debug
    :param type: 数据导出类型
    :param str_knowledge_search_result:
    :param str_observation:
    :return:
    """
    knowledge_list = get_knowledge_detail_from_knowledge_search_result(str_knowledge_search_result)
    obs_knowledge_list = get_knowledge_detail_from_observation(str_observation)

    # 判断用obs的结果 还是 用knowledge_search_result的结果
    if type == "from_knowledge":
        knowledge_replace_list = knowledge_list
    elif type == "from_obs":
        knowledge_replace_list = obs_knowledge_list
    else:
        if len(obs_knowledge_list) == 0 and len(knowledge_list) == 0:
            return ""
        elif len(obs_knowledge_list) == 0 and len(knowledge_list) != 0:
            knowledge_replace_list = obs_knowledge_list
        else:
            knowledge_replace_list = knowledge_list

    knowledge_str = ""
    for kl_idx, kl in enumerate(knowledge_replace_list):
        knowledge_str += "obs" + str(kl_idx + 1) + " " + kl + "\n\n"

    if len(knowledge_replace_list) > 50 and len(knowledge_str) > 32000:
        print(rid, "knowledge_replace_list解析数据异常", len(knowledge_replace_list))
        knowledge_str = ""

    return knowledge_str


def get_log_exception_status(data_item, data_source):
    """
    参考文档：https://li.feishu.cn/docx/Kmksd7278oFcktxiIXfc3qk1nSd
    :param data_item: 数据dict格式
    :param data_source: 数据字段来源
    :return:

    # 需要分级 有些影响业务/有些不影响
    异常类型1：某字段全为空【单条无法判断】
    异常类型2：校验数据发生日期和上传日期是否一致
    异常类型3：校验数据是否被干预
    异常类型4：校验数据大模型model_13b_input输入是否合法
    异常类型5：校验非拒识/语音静默query的tts是否为空
    异常类型6: 大模型model_13b_input被截断
    异常类型7: knowledge_result/media_result/session_context_list 等json字段无法解析
    """
    # 异常类型2：校验数据发生日期和上传日期是否一致
    if data_source == "car":
        record_id = data_item.get("record_id", "unk")
        if record_id is not None and data_item.get("dt", "unk") not in record_id and 'lixiang' not in record_id:
            return False, f"record_id中日期和实际发生日期不符", 1

    if data_item.get("input_safe_labels", "unk") == "unk":
        print("请确认字段格式，所给数据中不包含干预服务字段")

    # 兼容一下历史版本的数据 input_safe_labels有两种格式 list 和 str
    list_input_safe_labels = eval(data_item["input_safe_labels"]) if "[" in data_item.get("input_safe_labels", "") else [data_item.get("input_safe_labels", "")]
    str_input_safe_labels = list_input_safe_labels[0]

    # 校验数据是否被安全字段/干预字段拦截，大模型输入是否合法
    if data_item.get("input_safe_detect_info", "unk") != "unk":
        # 新版安全校验逻辑：根据input_safe_detect_info 和 input_safe_labels 判断query状态
        if data_item.get("domain", "unk") in ["gpt_chat", "gpt_autoqa"]:
            # 异常类型3：校验数据是否被干预
            if data_item["input_safe_detect_info"] == "" and str_input_safe_labels == "":
                return False, f"落域为gpt_chat/gpt_autoqa，但input_safe_label和input_safe_detect_info字段为空"
            # 异常类型4：校验数据大模型输入是否合法
            elif data_item["input_safe_detect_info"] == "SDS_SAFE" and str_input_safe_labels in ["", "安全"] \
                    and data_item.get("model_13b_input", "") == "":
                if str(data_item.get("domain_li", "")).lower() in ["stock", "mathqa"]:
                    pass
                else:
                    return False, f"落域为gpt_chat/gpt_autoqa，input_safe_detect_info字段为安全, input_safe_label为空或者安全，但model_13b_input字段为空"
            else:
                pass

    elif data_item.get("query_safe_result", "unk") != "unk":
        # 旧版安全校验逻辑：根据query_safe_result 和 input_safe_labels 判断query状态
        dict_query_safe_result = json.loads(data_item["query_safe_result"]) if "{" in data_item["query_safe_result"] else {}
        if data_item.get("domain", "unk") in ["gpt_chat", "gpt_autoqa"]:
            # 异常类型3：校验数据是否被干预
            if str_input_safe_labels == "" and dict_query_safe_result == {}:
                return False, f"落域为gpt_chat/gpt_autoqa，但input_safe_label和query_safe_result字段为空"
            # 异常类型4：校验数据大模型输入是否合法
            elif dict_query_safe_result.get('input_safe_labels') == ["安全"] and str_input_safe_labels in ["安全", ""] \
                    and data_item.get("model_13b_input", "") == "":
                if str(data_item.get("domain_li", "")).lower() in ["stock", "mathqa"]:
                    pass
                else:
                    return False, f"落域为gpt_chat/gpt_autoqa，query_safe_result字段为安全，input_safe_label为空或者安全，但model_13b_input字段为空"
            else:
                pass
    else:
        print("请确认字段格式，所给数据中不包含安全检测字段")
        if data_item.get("domain", "unk") in ["gpt_chat", "gpt_autoqa"] and data_item.get("model_13b_input", "") == "":
            if str(data_item.get("domain_li", "")).lower() in ["stock", "mathqa"]:
                pass
            else:
                return False, f"落域为gpt_chat/gpt_autoqa，所给数据中不包含安全检测/干预字段，且model_13b_input字段为空"

    # 异常类型6: 大模型input 被截断
    if data_item.get("domain", "unk") in ["gpt_chat", "gpt_autoqa"]:
        if "[truncated]" in data_item.get("model_13b_input", ""):
            return False, f"落域为gpt_chat/gpt_autoqa，model_13b_input字段包含[truncated]字段，被截断"

    # 异常类型7: knowledge_result/media_result/session_context_list 等json字段无法解析
    if data_item.get("domain", "unk") in ["gpt_chat", "gpt_autoqa"]:
        if "knowledge_search_result" in data_item and "{" in data_item["knowledge_search_result"]:
            try:
                json.loads(data_item["knowledge_search_result"])
            except:
                return False, f"落域为gpt_chat/gpt_autoqa，knowledge_search_result字段json解析异常"

        if "media_search_result" in data_item and "{" in data_item["media_search_result"]:
            try:
                json.loads(data_item["media_search_result"])
            except:
                return False, f"落域为gpt_chat/gpt_autoqa，media_search_result字段json解析异常"

    if "session_context_list" in data_item and "{" in data_item["session_context_list"]:
        try:
            json.loads(data_item["session_context_list"])
        except:
            return False, f"session_context_list字段json解析异常"

    # 异常类型5：校验非拒识/语音静默query的tts是否为空
    if data_item["domain"] != "" and data_item["tts"] == "":
        # 非拒识query
        if data_item["domain"] == "global" and ("voice" in str(data_item["slot_li"].lower()) or "VOICE" in str(data_item["content"]).lower()):
            # 语音静默
            pass
        else:
            return False, f"落域不为空且落域不含global，slot字段不等于voice时的query，但回复(tts)为空"

    return True, ""


def get_safe_label(str_domain, str_input_safe_detect_info, str_input_safe_labels):
    if str_domain in ("gpt_chat", "gpt_autoqa", "gpt_paintingmaster", "taskmaster"):
        if str_input_safe_labels == '' and str_input_safe_detect_info == '':
            return "异常流量，落域为gpt_chat/gpt_autoqa，但input_safe_label和query_safe_result字段为空"

        # 兼容
        if "[" in str_input_safe_labels:
            str_input_safe_labels = eval(str_input_safe_labels)[0]

        if str_input_safe_labels in ('干预服务', 'whitelist'):
            return "干预服务"

        if str_input_safe_labels == '安全':
            return ""

        return "大模型-安全"
    else:
        return ""


if __name__ == '__main__':
    pass
    # # 读取excel文件
    # file_name = "../data/手机日志标注-1208.xlsx"
    # data = read_excel_sheet(file_name, sheet_name="1203-04 vip")
    # # 读取csv文件
    file_name = "../data/实车6.6_大模型 - Sheet1.csv"
    data = read_pd_csv(file_name)
    # 读取jsonl文件
    # file_name = "/mnt/pfs-guan-ssai/nlu/ota_user_data/phone/2024-12-16_phone_data.jsonl"
    # data = read_jsonl(file_name)

    write_session_list = []
    for idx, query_item in enumerate(data):

        model_1b_output = query_item["model_1b_output"]
        model_13b_input = query_item["model_13b_input"]
        domain = query_item["domain"]

        knowledge_search_result = str(query_item.get("knowledge_search_result", ""))
        media_search_result = str(query_item.get("media_search_result", ""))
        if len(media_search_result) > len(knowledge_search_result):
            knowledge_search_result = media_search_result

        if "函数调用" in model_13b_input:
            query_item["API"], query_item["Observation"], query_item["Thought"] = \
                get_api_thought_observation_functioncall(domain, model_1b_output, model_13b_input, knowledge_search_result)
            query_item["knowledge_detail"] = get_knowledge_detail(knowledge_search_result, query_item["Observation"])
        else:
            query_item["API"], query_item["Observation"], query_item["Thought"] = \
                get_api_thought_observation(domain, model_1b_output, model_13b_input, knowledge_search_result)
            query_item["knowledge_detail"] = ""

        task_label = get_task_label(query_item)
        write_session_list.append(task_label)

    # query_item["format_session_list"] = format_session_context_list(rid, session_context_list, model_1b_input, model_13b_input)
    # query_item["str_manu_session"] = format_session_context_str(query_item["format_session_list"])

    # to_json
    # write_session_df.to_json("2024-11-06.filter.add_label.jsonl", orient='records', lines=True, force_ascii=False)

    # to_csv
    # pd.DataFrame(write_session_list, columns=["task_label"]).to_csv("debug.csv", index=False, encoding="utf-8-sig")

