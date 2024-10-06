import logging
import os
# 创建logger对象
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)  # 设置日志级别为ERROR
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
path = os.path.dirname(__file__)
file_handler = logging.FileHandler(os.path.join(path, "log",'log.txt'))
file_handler.setLevel(logging.DEBUG)
# 创建日志格式器
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
# 将格式器添加到处理器
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
# 将处理器添加到logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


