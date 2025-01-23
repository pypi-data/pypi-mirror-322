# -*- coding: utf-8 -*-
# @Time    : 2022-09-13 11:39
# @Author  : zbmain


# devices
class devices():
    import torch
    torch = torch.device(torch.cuda.is_available() and 'cuda' or 'cpu')
    '''torch方式'''
    tensorflow = 'GPU:0'
    '''tensorflow方式'''


def get_gpus_info():
    import torch
    info = []
    try:
        for gpu_id in range(torch.cuda.device_count()):
            torch.cuda.set_device(gpu_id)
            free_memory, total_memory = torch.cuda.mem_get_info()
            info.append((torch.cuda.get_device_name(), free_memory / (1024 ** 2), total_memory / (1024 ** 2)))
    except Exception as e:
        print('device not found!')
    return info


def task_maximum(task_usage_size: int, unit:str = "MB", reserve_size:int = 1024):
    task_num = 0
    info = get_gpus_info()
    if info:
        total_free_memory = sum([_[1]-reserve_size for _ in info])
        task_num = int(total_free_memory // task_usage_size)
    return task_num
