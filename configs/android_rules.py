import os

import msgpack

from configs.config import *
import yaml
import  asyncio
from net import *

id_configs = {}

for index,file in enumerate(os.listdir(android_configs_path)):
    if file.endswith('.yaml'):
        client_configs = yaml.safe_load(open(os.path.join(android_configs_path, file), 'r'))
        if len(file.split('.')) > 2:
            raise ValueError(f"Invalid file name{file}")
        phone_id = file.split('.')[0]
        id_configs[phone_id] = client_configs


# 检查数量
if phones_number != len(id_configs):
    raise Exception(f'Number of phones in config {phones_number} is not equal to number of config files{len(id_configs)}')






