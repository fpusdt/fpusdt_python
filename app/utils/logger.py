#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日志工具模块
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(name='tron_api', level=logging.INFO):
    """
    设置日志记录器
    
    Args:
        name (str): 日志记录器名称
        level: 日志级别
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    
    # 创建日志目录
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 创建文件处理器（轮转日志）
    log_file = os.path.join(log_dir, f'{name}.log')
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_api_request(logger, method, endpoint, params=None, response_code=None, error=None):
    """
    记录API请求日志
    
    Args:
        logger: 日志记录器
        method (str): HTTP方法
        endpoint (str): API端点
        params (dict): 请求参数
        response_code (int): 响应状态码
        error (str): 错误信息
    """
    
    log_data = {
        'method': method,
        'endpoint': endpoint,
        'params': params or {},
        'response_code': response_code,
        'timestamp': datetime.now().isoformat()
    }
    
    if error:
        log_data['error'] = error
        logger.error(f"API请求失败: {log_data}")
    else:
        logger.info(f"API请求: {log_data}")

# 创建默认日志记录器
default_logger = setup_logger()