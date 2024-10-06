from configs import *
from net import *
from utils import logger
import time
import msgpack
from net import start_thread
from model import *
import pandas as pd

socket_port = 4563
#启动server
start_thread()


# 检查手机连接是否完成
while True:
    with clients_lock:
        current_phone_number = len(clients)
    if current_phone_number == phones_number:
        logger.info(f'All {phones_number} phones connected.')
        break
    else:
        logger.info(f'{current_phone_number}/{phones_number} phones connected.')
        time.sleep(3)

with clients_lock:
    list_clients = list(clients)

# 为手机分配配置
with id_clients_lock:
    for i in range(phones_number):
        phone_id = list(id_configs.keys())[i]
        id_clients[phone_id] = list_clients[i]

first_url = ""
with id_clients_lock:
    for id in id_clients.keys():
        id_configs[id]["name"] = id
        network_dict = id_configs[id]["network"]
        in_dict = network_dict["in"]
        out_dict = network_dict["out"]
        for element in in_dict:
            from_id = element["from"]
            if from_id!= "server":
                element["url"]=f'{id_clients[from_id].remote_address[0]}:{socket_port}'
                print(element["url"])
            else:
                element["url"]=f'{ip}:{port}'
                first_url = f'{id_clients[id].remote_address[0]}:{socket_port}'

        for element in out_dict:
            to_id = element["to"]
            if to_id!= "callback":
                element["url"]=f'{id_clients[to_id].remote_address[0]}:{socket_port}'
                print(element["url"])
# 写入callback地址
with id_clients_lock:
    for id in id_clients.keys():
        id_configs[id]["name"] = id
        network_dict = id_configs[id]["network"]
        out_dict = network_dict["out"]
        for element in out_dict:
            to_id = element["to"]
            if to_id== "callback":
                element["url"]=first_url




# 发送配置
with id_clients_lock:
    for phone_id, client in id_clients.items():
        msg = {
            "type":"config",
            "data": id_configs[phone_id]
        }

        bytes_msg = msgpack.packb(msg)
        asyncio.run_coroutine_threadsafe(send_binary_data(client, bytes_msg), sever_loop[0])
        logger.info(f'Sent config to {phone_id}.')


time.sleep(10)
# 发送输入
for id,config in id_configs.items():
    if config["network"]["in"][0]["from"] == "server":
        msg = {
            "type":"data",
            "data": getBertMiddle()
        }
        bytes_msg = msgpack.packb(msg)
        with id_clients_lock:
            asyncio.run_coroutine_threadsafe(send_binary_data(id_clients[id], bytes_msg), sever_loop[0])
            logger.info(f'Sent input to {id}.')


