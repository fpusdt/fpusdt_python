#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件
"""

import os

class Config:
    """基础配置类"""

    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tron-api-secret-key-2025'
    DEBUG = True

    # TRON网络配置
    TRON_GRID_API_URL = 'https://api.trongrid.io'
    TRON_GRID_API_KEY = os.environ.get('TRON_GRID_API_KEY') or ''  # 可选，用于提高请求限制

    # TRC20 USDT合约配置
    USDT_CONTRACT_ADDRESS = 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t'  # USDT TRC20合约地址
    USDT_DECIMALS = 6  # USDT精度

    # 默认测试配置
    DEFAULT_TEST_ADDRESS = 'TTAUj1qkSVK2LuZBResGu2xXb1ZAguGsnu'
    DEFAULT_TRC10_TOKEN_ID = '1002992'

    # API响应配置
    API_VERSION = '3.0'
    API_TIMEOUT = 30  # 请求超时时间（秒）

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}