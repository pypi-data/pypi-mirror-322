# -*- coding: utf-8 -*-
# @Time    : 2022-07-22 18:20
# @Author  : zbmain

__all__ = ['view_df', 'warning_ignored', 'set_seed', 'delay']

import time

from . import pd_util

view_df = pd_util.view_df
pandas_set = pd_util.setting


def delay(second: int):
    time.sleep(second)

    def wrapper(func):
        def inner(*args, **kwargs):
            ret = func(*args, **kwargs)
            return ret

        return inner

    return wrapper


import warnings


def warning_ignored():
    """关闭一些警告(不推荐)"""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)


def set_seed(seed: int = 1990):
    import numpy, random
    random.seed(seed)
    numpy.random.seed(seed)
    try:
        import tensorflow
        tensorflow.random.set_seed(seed)
        tensorflow.set_random_seed(seed)
    except:
        pass

    try:
        import torch
        torch.manual_seed(seed)  # cpu
        torch.cuda.manual_seed(seed)  # gpu
        torch.cuda.manual_seed_all(seed)  # all gpu
    except:
        pass
