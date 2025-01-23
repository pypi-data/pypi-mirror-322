from api_cloud_document import *
from data_process_utils.llm_utils import *

# input_path = r"D:\2486837177_112661\Downloads\2026-01-01_sample1.csv"
# data = read_pd_csv(input_path)
# head_list = ['dt_new_session_id', 'new_session_id', 'record_id', 'msg_id', 'track_id', 'dt', 'request_time', 'vin',
#              'query', 'asr_finish_query', 'tts', 'domain', 'command', 'content', 'domain_li', 'action_li', 'slot_li',
#              'domains', 'commands', 'contents', 'ota_version', 'vehicle_category', 'semantic_source',
#              'speech_reject_score', 'occupant_face_orientation', 'phone_reject_score', 'semantic_reject_score',
#              'reject_reason', 'multi_status', 'input_safe_detect_info', 'input_safe_labels', 'text_safe',
#              'text_safe_tags', 'raw_query', 'session_context_list', 'knowledge_search_result', 'media_search_result',
#              'model_1b_input', 'model_1b_output', 'model_13b_input', 'model_13b_output', 'response_speakcontent',
#              'response_taskdatas', 'continuous_dialogue', 'multiple_dialogue', 'non_first_wakeup', 'is_fullduplex',
#              'vehicle_model_name', 'voice_pickup_region', 'audio_url', 'file_key', 'bucket_name', 'eto_target', 'API',
#              'Observation', 'Thought']
# data_list = []
# for item in data:
#     # 异常数据检测
#     data_status, error_type, *other_values = get_log_exception_status(item, "car")
#     # print(data_status, error_type, *other_values)
#     str_domain = str(item["domain"].strip())
#     str_model_1b_output = str(item["model_1b_output"])
#     str_model_13b_input = str(item["model_13b_input"])
#     item["API"], item["Observation"], item["Thought"] = get_api_thought_observation_functioncall(str_domain,
#                                                                                                  str_model_1b_output,
#                                                                                                  str_model_13b_input)
# data_list = [list(item.values()) for item in data]
# save_csv(head_list, data_list, r"D:\2486837177_112661\Downloads\2026-01-01\api为空测试.csv")
# range_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
# pairs = []
#
# # 循环遍历列表，按照你的要求创建配对
# # 注意：这里的逻辑是特设的，只为了满足你给出的配对结果
# for i in range(len(range_list) - 1):  # 遍历到倒数第二个元素
#     if i % 2 == 0:  # 每隔一个元素取一个作为配对的第一个元素
#         # 如果是偶数索引，直接配对当前元素和下一个元素
#         pairs.append((range_list[i], range_list[i + 1]))
# # 添加特殊的最后一个配对（这不符合原先的配对逻辑，但按照你的要求添加）
# if len(range_list) % 2 != 0:  # 如果列表长度为奇数
#     pairs.append((range_list[-2], range_list[-1]))
# print(pairs)
# # 打印配对结果
# for pair in pairs:
#     print(pair)
from data_process_utils import append_data
from data_process_utils import read_pd_csv

# debug
task_type = "write"  # 可选项 write，edit，第一个是写入，第二个是修改
feishu_folder_token = "CRr1fTUrflaXIBdunN6ckPQwnUb"  # 飞书云文档所在文件夹token eg. https://li.feishu.cn/drive/folder/GBSSfE0fel6X1xdE3ENcl02Nnqf 中 的GBSSfE0fel6X1xdE3ENcl02Nnqf
feishu_file_name = "20260101线上数据"    # 飞书云文档名 eg.20241226线上数据
feishu_sheet_name = "Sheet1"  # 飞书sheet名 eg. "ss2数据1"
input_path = r"D:\2486837177_112661\Downloads\2025-01-09_all.csv"  # r"/mnt/pfs-guan-ssai/nlu/ota_user_data/car_annote/2025-01-02/2025-01-02_all_session_random_23.csv"

access_token = get_tenant_access_token()
pd = read_pd_csv(input_path)

append_data(access_token, pd, feishu_file_name, feishu_folder_token, feishu_sheet_name)