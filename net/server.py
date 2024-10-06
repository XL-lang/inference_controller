import asyncio

import msgpack
import websockets
from utils import logger
from websockets import WebSocketServerProtocol
from net.var import *
import threading
from typing import List
import logging
import pandas as pd


sever_loop = []
ip = "192.168.1.6"
port = 4112
column_names = ["cpu usage", "memory usage", "inference time"]
df_lock = threading.Lock()
df = pd.DataFrame(columns=column_names)


async def register(client: WebSocketServerProtocol):
    with clients_lock:
        clients.add(client)
    logger.info(f'{client.remote_address} connects.')

async def unregister(client: WebSocketServerProtocol):
    with clients_lock:
        clients.remove(client)
    logger.error(f'{client.remote_address} disconnects,maybe an error occurred.')


ip_complete_message = {}
ip_complete_message_lock = threading.Lock()
async def handle_message(message: List[bytes], client: WebSocketServerProtocol):
    try:
        with ip_complete_message_lock:
            if client.remote_address not in ip_complete_message:
                ip_complete_message[client.remote_address] = b''
            complete_message = ip_complete_message[client.remote_address]

            if message == b'':  # 空二进制数据作为结束信号
                logger.info(f'{client.remote_address} sent termination signal.')
                await process_complete_message(client, complete_message)
                ip_complete_message[client.remote_address] = b''
            else:
                complete_message += message

                ip_complete_message[client.remote_address] = complete_message
                logger.info(f'Received message fragment from {client.remote_address},size is {len(message)}.')

    except Exception as e:
        logger.error(f'Connection closed: {e}')


async def process_complete_message(client: WebSocketServerProtocol, message: List[bytes]):
    decoded_message = msgpack.unpackb(message, raw=False)
    with df_lock:
        data = decoded_message["data"]
        inference_time = data["inference"]
        cpu_usage = 0
        memory_usage = 0
        # 写入df
        length = df .shape[0]
        df.loc[length] = [cpu_usage, memory_usage, inference_time]
        df.to_csv("data.csv", index=False)
    logger.info(f'Received message from {client.remote_address}: {decoded_message}')
    pass
async def server_handler(client: WebSocketServerProtocol, path: str):
    await register(client)
    try:
        async for message in client:
            await handle_message(message, client)
    except Exception as e:
        logger.error(f'Connection closed: {e}')
    finally:
        await unregister(client)

async def send_binary_data(client: WebSocketServerProtocol, data: bytes, chunk_size: int = 1024):
    # 将数据分成块进行传输
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        await client.send(chunk)
    # 发送空二进制数据作为结束标志
    await client.send(b'')
async def main():

    async with websockets.serve(server_handler, ip, port):
        logger.info(f'Server started at ws://{ip}:{port}.')
        await asyncio.Future()  # run forever

def start_server():
    sever_loop.append(asyncio.new_event_loop())
    asyncio.set_event_loop(sever_loop[0])
    sever_loop[0].run_until_complete(main())
def start_thread():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()







