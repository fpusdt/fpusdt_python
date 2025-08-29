#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TRON区块链API接口服务 - Python版本

功能说明：
- 支持TRC10代币操作
- 支持TRC20代币操作（包括USDT）
- 支持TRX原生代币操作
- 支持助记词生成地址
- 支持区块链查询功能

作者：纸飞机(Telegram): https://t.me/king
日期：2025年8月

温馨提示：接受各种代码定制
"""

from flask import Flask, jsonify, request, render_template
try:
    from flask_cors import CORS
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.tron_api import TronAPI
from config.config import Config

def get_docs_data():
    """生成API文档数据"""
    domain = "http://localhost:8765"

    return {
        'wallet': {
            'title': '钱包管理',
            'apis': [
                {
                    'title': '生成TRON地址',
                    'icon': '💳',
                    'method': 'GET',
                    'url': f'{domain}/v1/createAddress',
                    'testUrl': f'{domain}/v1/createAddress',
                    'description': '生成新的TRON地址（简单版本）',
                    'params': None
                },
                {
                    'title': '生成带助记词的钱包地址',
                    'icon': '🔑',
                    'method': 'GET',
                    'url': f'{domain}/v1/generateAddressWithMnemonic',
                    'testUrl': f'{domain}/v1/generateAddressWithMnemonic',
                    'description': '通过助记词生成TRON地址，包含助记词、私钥、公钥',
                    'params': None
                },
                {
                    'title': '根据私钥获取地址',
                    'icon': '🔐',
                    'method': 'GET',
                    'url': f'{domain}/v1/getAddressByKey',
                    'testUrl': f'{domain}/v1/getAddressByKey?privateKey=your_private_key',
                    'description': '通过私钥获取对应的TRON地址信息',
                    'params': [
                        {'name': 'privateKey', 'type': 'string', 'required': '是', 'desc': '64位私钥'}
                    ]
                }
            ]
        },
        'balance': {
            'title': '余额查询',
            'apis': [
                {
                    'title': '查询TRX余额',
                    'icon': '💰',
                    'method': 'GET',
                    'url': f'{domain}/v1/getTrxBalance',
                    'testUrl': f'{domain}/v1/getTrxBalance?address=TTAUj1qkSVK2LuZBResGu2xXb1ZAguGsnu',
                    'description': '查询指定地址的TRX余额',
                    'params': [
                        {'name': 'address', 'type': 'string', 'required': '是', 'desc': 'TRON地址'}
                    ]
                },
                {
                    'title': '查询TRC20代币余额',
                    'icon': '💵',
                    'method': 'GET',
                    'url': f'{domain}/v1/getTrc20Balance',
                    'testUrl': f'{domain}/v1/getTrc20Balance?address=TTAUj1qkSVK2LuZBResGu2xXb1ZAguGsnu',
                    'description': '查询指定地址的TRC20代币余额（如USDT）',
                    'params': [
                        {'name': 'address', 'type': 'string', 'required': '是', 'desc': 'TRON地址'}
                    ]
                },
                {
                    'title': '查询TRC10代币信息',
                    'icon': '🪙',
                    'method': 'GET',
                    'url': f'{domain}/v1/getTrc10Info',
                    'testUrl': f'{domain}/v1/getTrc10Info?address=TTAUj1qkSVK2LuZBResGu2xXb1ZAguGsnu&tokenId=1002992',
                    'description': '查询指定地址的TRC10代币余额和信息',
                    'params': [
                        {'name': 'address', 'type': 'string', 'required': '是', 'desc': 'TRON地址'},
                        {'name': 'tokenId', 'type': 'string', 'required': '否', 'desc': 'TRC10代币ID，默认1002992'}
                    ]
                }
            ]
        },
        'transfer': {
            'title': '转账功能',
            'apis': [
                {
                    'title': 'TRX转账',
                    'icon': '💸',
                    'method': 'POST',
                    'url': f'{domain}/v1/sendTrx',
                    'testUrl': f'{domain}/v1/sendTrx',
                    'description': '发送TRX到指定地址',
                    'params': [
                        {'name': 'to', 'type': 'string', 'required': '是', 'desc': '接收地址'},
                        {'name': 'amount', 'type': 'string', 'required': '是', 'desc': '转账金额(单位: TRX)'},
                        {'name': 'key', 'type': 'string', 'required': '是', 'desc': '发送方私钥'},
                        {'name': 'message', 'type': 'string', 'required': '否', 'desc': '转账备注'}
                    ]
                },
                {
                    'title': 'TRC20代币转账',
                    'icon': '💳',
                    'method': 'POST',
                    'url': f'{domain}/v1/sendTrc20',
                    'testUrl': f'{domain}/v1/sendTrc20',
                    'description': '发送TRC20代币（如USDT）到指定地址',
                    'params': [
                        {'name': 'to', 'type': 'string', 'required': '是', 'desc': '接收地址'},
                        {'name': 'amount', 'type': 'string', 'required': '是', 'desc': '转账金额'},
                        {'name': 'key', 'type': 'string', 'required': '是', 'desc': '发送方私钥'}
                    ]
                },
                {
                    'title': 'TRC10代币转账',
                    'icon': '🎯',
                    'method': 'POST',
                    'url': f'{domain}/v1/sendTrc10',
                    'testUrl': f'{domain}/v1/sendTrc10',
                    'description': '发送TRC10代币到指定地址',
                    'params': [
                        {'name': 'to', 'type': 'string', 'required': '是', 'desc': '接收地址'},
                        {'name': 'amount', 'type': 'string', 'required': '是', 'desc': '转账金额'},
                        {'name': 'key', 'type': 'string', 'required': '是', 'desc': '发送方私钥'},
                        {'name': 'tokenId', 'type': 'string', 'required': '否', 'desc': 'TRC10代币ID，默认1002992'}
                    ]
                }
            ]
        },
        'transaction': {
            'title': '交易查询',
            'apis': [
                {
                    'title': '查询交易详情',
                    'icon': '📊',
                    'method': 'GET',
                    'url': f'{domain}/v1/getTransaction',
                    'testUrl': f'{domain}/v1/getTransaction?txID=your_transaction_id',
                    'description': '根据交易ID查询交易详情',
                    'params': [
                        {'name': 'txID', 'type': 'string', 'required': '是', 'desc': '交易ID'}
                    ]
                },
                {
                    'title': '查询TRC20交易回执',
                    'icon': '📋',
                    'method': 'GET',
                    'url': f'{domain}/v1/getTrc20TransactionReceipt',
                    'testUrl': f'{domain}/v1/getTrc20TransactionReceipt?txID=your_transaction_id',
                    'description': '查询TRC20代币交易的详细回执信息',
                    'params': [
                        {'name': 'txID', 'type': 'string', 'required': '是', 'desc': '交易ID'}
                    ]
                }
            ]
        },
        'blockchain': {
            'title': '区块链查询',
            'apis': [
                {
                    'title': '获取区块高度',
                    'icon': '📈',
                    'method': 'GET',
                    'url': f'{domain}/v1/getBlockHeight',
                    'testUrl': f'{domain}/v1/getBlockHeight',
                    'description': '获取当前TRON区块链的最新区块高度',
                    'params': None
                },
                {
                    'title': '根据区块号查询区块',
                    'icon': '🔍',
                    'method': 'GET',
                    'url': f'{domain}/v1/getBlockByNumber',
                    'testUrl': f'{domain}/v1/getBlockByNumber?blockID=latest',
                    'description': '根据区块号或区块哈希查询区块信息',
                    'params': [
                        {'name': 'blockID', 'type': 'string', 'required': '是', 'desc': '区块号或区块哈希，可以使用"latest"获取最新区块'}
                    ]
                }
            ]
        },
        'tools': {
            'title': '工具接口',
            'apis': [
                {
                    'title': 'API状态检查',
                    'icon': '⚡',
                    'method': 'GET',
                    'url': f'{domain}/v1/status',
                    'testUrl': f'{domain}/v1/status',
                    'description': '检查API服务的运行状态和版本信息',
                    'params': None
                },
                {
                    'title': '获取接口列表',
                    'icon': '📋',
                    'method': 'GET',
                    'url': f'{domain}/v1/getApiList',
                    'testUrl': f'{domain}/v1/getApiList',
                    'description': '获取所有可用的API接口列表',
                    'params': None
                }
            ]
        }
    }

def print_ascii_art():
    """打印ASCII艺术字体"""
    print()
    print("███████╗██████╗ ██╗   ██╗███████╗██████╗ ████████╗")
    print("██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗╚══██╔══╝")
    print("█████╗  ██████╔╝██║   ██║███████╗██║  ██║   ██║   ")
    print("██╔══╝  ██╔═══╝ ██║   ██║╚════██║██║  ██║   ██║   ")
    print("██║     ██║     ╚██████╔╝███████║██████╔╝   ██║   ")
    print("╚═╝     ╚═╝      ╚═════╝ ╚══════╝╚═════╝    ╚═╝   ")
    print("                                                  ")
    print()

def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # 加载配置
    app.config.from_object(Config)

    # 配置JSON输出中文字符不进行ASCII编码
    app.config['JSON_AS_ASCII'] = False

    # 启用跨域支持
    if CORS_AVAILABLE:
        CORS(app)

    # 初始化TRON API
    tron_api = TronAPI()

    # ==================== 主页路由 ====================

    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')

    @app.route('/doc')
    def docs():
        """API文档页面"""
        # 生成文档数据
        api_data = get_docs_data()
        return render_template('docs.html', apiData=api_data)

    # ==================== API v1 路由 ====================

    @app.route('/v1/status', methods=['GET', 'POST'])
    def api_status():
        """API状态检查"""
        return jsonify({
            'code': 1,
            'msg': 'TRON API服务运行正常',
            'data': {
                'version': '3.0',
                'python_version': sys.version,
                'timestamp': int(datetime.now().timestamp()),
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'time': int(datetime.now().timestamp())
        })

    @app.route('/v1/getApiList', methods=['GET', 'POST'])
    def get_api_list():
        """获取API接口列表"""
        api_list = {
            '地址生成': {
                'createAddress': '生成TRON地址',
                'generateAddressWithMnemonic': '通过助记词生成地址',
                'getAddressByKey': '根据私钥获取地址'
            },
            '余额查询': {
                'getTrxBalance': '查询TRX余额',
                'getTrc20Balance': '查询TRC20代币余额',
                'getTrc10Info': '查询TRC10代币信息'
            },
            '转账功能': {
                'sendTrx': 'TRX转账',
                'sendTrc20': 'TRC20代币转账',
                'sendTrc10': 'TRC10代币转账'
            },
            '交易查询': {
                'getTransaction': '查询交易详情',
                'getTrc20TransactionReceipt': '查询TRC20交易回执'
            },
            '区块链信息': {
                'getBlockHeight': '获取区块高度',
                'getBlockByNumber': '根据区块号查询区块'
            },
            '工具接口': {
                'status': 'API状态检查',
                'getApiList': '获取接口列表'
            }
        }

        return jsonify({
            'code': 1,
            'msg': '接口列表获取成功',
            'data': api_list,
            'time': int(datetime.now().timestamp())
        })

    # ==================== 地址生成相关接口 ====================

    @app.route('/v1/createAddress', methods=['GET', 'POST'])
    def create_address():
        """生成TRON地址（简单版本）"""
        return tron_api.create_address()

    @app.route('/v1/generateAddressWithMnemonic', methods=['GET', 'POST'])
    def generate_address_with_mnemonic():
        """通过助记词生成TRON地址"""
        return tron_api.generate_address_with_mnemonic()

    @app.route('/v1/getAddressByKey', methods=['GET', 'POST'])
    def get_address_by_key():
        """根据私钥获取地址信息"""
        private_key = request.args.get('privateKey') or request.form.get('privateKey')
        return tron_api.get_address_by_key(private_key)

    # ==================== 余额查询相关接口 ====================

    @app.route('/v1/getTrxBalance', methods=['GET', 'POST'])
    def get_trx_balance():
        """查询TRX余额"""
        address = request.args.get('address') or request.form.get('address')
        return tron_api.get_trx_balance(address)

    @app.route('/v1/getTrc20Balance', methods=['GET', 'POST'])
    def get_trc20_balance():
        """查询TRC20代币余额（如USDT）"""
        address = request.args.get('address') or request.form.get('address')
        return tron_api.get_trc20_balance(address)

    @app.route('/v1/getTrc10Info', methods=['GET', 'POST'])
    def get_trc10_info():
        """查询TRC10代币余额和信息"""
        address = request.args.get('address') or request.form.get('address')
        token_id = request.args.get('tokenId') or request.form.get('tokenId')
        return tron_api.get_trc10_info(address, token_id)

    # ==================== 转账相关接口 ====================

    @app.route('/v1/sendTrx', methods=['GET', 'POST'])
    def send_trx():
        """TRX转账"""
        to = request.args.get('to') or request.form.get('to')
        amount = request.args.get('amount') or request.form.get('amount')
        key = request.args.get('key') or request.form.get('key')
        message = request.args.get('message') or request.form.get('message')
        return tron_api.send_trx(to, amount, key, message)

    @app.route('/v1/sendTrc20', methods=['GET', 'POST'])
    def send_trc20():
        """TRC20代币转账（如USDT）"""
        to = request.args.get('to') or request.form.get('to')
        amount = request.args.get('amount') or request.form.get('amount', '1.000001')
        key = request.args.get('key') or request.form.get('key')
        return tron_api.send_trc20(to, amount, key)

    @app.route('/v1/sendTrc10', methods=['GET', 'POST'])
    def send_trc10():
        """TRC10代币转账"""
        to = request.args.get('to') or request.form.get('to')
        amount = request.args.get('amount') or request.form.get('amount', '1')
        key = request.args.get('key') or request.form.get('key')
        token_id = request.args.get('tokenId') or request.form.get('tokenId', '1002992')
        return tron_api.send_trc10(to, amount, key, token_id)

    # ==================== 交易查询相关接口 ====================

    @app.route('/v1/getTransaction', methods=['GET', 'POST'])
    def get_transaction():
        """查询交易详情（通用）"""
        tx_id = request.args.get('txID') or request.form.get('txID')
        return tron_api.get_transaction(tx_id)

    @app.route('/v1/getTrc20TransactionReceipt', methods=['GET', 'POST'])
    def get_trc20_transaction_receipt():
        """查询TRC20交易回执"""
        tx_id = request.args.get('txID') or request.form.get('txID')
        return tron_api.get_trc20_transaction_receipt(tx_id)

    # ==================== 区块链信息查询接口 ====================

    @app.route('/v1/getBlockHeight', methods=['GET', 'POST'])
    def get_block_height():
        """获取当前区块高度"""
        return tron_api.get_block_height()

    @app.route('/v1/getBlockByNumber', methods=['GET', 'POST'])
    def get_block_by_number():
        """根据区块号查询区块信息"""
        block_id = request.args.get('blockID') or request.form.get('blockID')
        return tron_api.get_block_by_number(block_id)

    return app

if __name__ == '__main__':
    # 打印ASCII艺术字体
    print_ascii_art()

    # 设置端口
    port = 8765
    host = '0.0.0.0'

    print(f"🚀 TRON API服务启动成功！")
    print(f"📍 服务地址: http://localhost:{port}")
    print(f"📚 接口文档: http://localhost:{port}/doc")
    print(f"✈️ 技术支持: https://t.me/king_orz")
    print()

    # 自动打开浏览器（只在主进程中打开，避免debug模式重复打开）
    import webbrowser
    import threading
    import time
    import os

    def open_browser():
        # 等待服务器启动
        time.sleep(2)
        url = f"http://localhost:{port}"
        print(f"🌐 正在打开浏览器: {url}")
        webbrowser.open(url)

    # 只在主进程中打开浏览器（避免Flask debug模式重启时重复打开）
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

    app = create_app()
    app.run(host=host, port=port, debug=True)
