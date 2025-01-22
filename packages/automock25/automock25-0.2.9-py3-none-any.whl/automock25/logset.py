import logging
import logging.config
import os
import configparser
import sys

# 模块级别的变量，用于缓存日志记录器
_logger = None
# 确保 sys 模块中的 stdout 使用 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')
def setup_logging():
    global _logger
    if _logger is not None:
        return _logger

    # 确保日志目录存在
    log_path = 'D:/automock25/logs'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # 使用 RawConfigParser 读取 logging.conf 文件，并显式指定编码为 UTF-8
    config = configparser.RawConfigParser()
    with open('logging.conf', 'r', encoding='utf-8') as config_file:
        config.read_file(config_file)

    # 使用 fileConfig 读取配置对象
    logging.config.fileConfig(config)

    # 获取根日志记录器
    _logger = logging.getLogger()
    return _logger
