# FRUSPOT - TRON API 3.0

```
███████╗██████╗ ██╗   ██╗███████╗██████╗ ████████╗
██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗╚══██╔══╝
█████╗  ██████╔╝██║   ██║███████╗██║  ██║   ██║
██╔══╝  ██╔═══╝ ██║   ██║╚════██║██║  ██║   ██║
██║     ██║     ╚██████╔╝███████║██████╔╝   ██║
╚═╝     ╚═╝      ╚═════╝ ╚══════╝╚═════╝    ╚═╝
```

🚀 **专业的 TRON 区块链 API 接口服务** - Python 版本

使用 Python Flask 框架开发，功能完整，性能稳定，易于部署和维护。

## 🚀 功能特色

- ✅ **完整功能**：支持 TRC10、TRC20、TRX 代币的完整操作
- ✅ **高性能**：基于 Flask 框架，轻量高效
- ✅ **易部署**：支持 Docker 部署和云原生架构
- ✅ **完整文档**：提供详细的 API 文档和使用示例
- ✅ **错误处理**：完善的错误处理和日志记录
- ✅ **安全可靠**：支持 HTTPS 和跨域请求

## 📋 支持的功能

### 💳 钱包管理

- 生成 TRON 地址
- 生成带助记词的钱包地址
- 根据私钥获取地址信息

### 💰 余额查询

- 查询 TRX 余额
- 查询 TRC20 代币余额（如 USDT）
- 查询 TRC10 代币信息

### 💸 转账功能

- TRX 转账（支持备注）
- TRC20 代币转账
- TRC10 代币转账

### 📊 交易查询

- 查询交易详情
- 查询 TRC20 交易回执

### ⛓️ 区块链查询

- 获取当前区块高度
- 根据区块号查询区块信息

### 🔧 工具接口

- API 状态检查
- 获取接口列表

## 🛠️ 安装部署

### 环境要求

- Python 3.7+
- pip

### 快速开始

1. **克隆项目**

```bash
git clone https://github.com/fpusdt/fpusdt_py.git
cd fpusdt_py
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

**注意**：如果遇到 Flask-CORS 的 SSL 证书问题，请手动执行：

```bash
pip install Flask-CORS --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

3. **运行服务**

```bash
python main.py
```

4. **访问服务**

- 主页：http://localhost:8765
- API 文档：http://localhost:8765/doc
- API 状态：http://localhost:8765/v1/status

5. **测试 API**

```bash
# 测试生成地址
curl "http://localhost:8765/v1/createAddress"

# 测试助记词生成
curl "http://localhost:8765/v1/generateAddressWithMnemonic"
```

### Docker 部署

1. **构建镜像**

```bash
docker build -t tron-api-python .
```

2. **运行容器**

```bash
docker run -d -p 8765:8765 --name tron-api tron-api-python
```

## 📖 API 文档

### 基础信息

- **Base URL**: `http://localhost:8765`
- **API 版本**: `v1`
- **响应格式**: JSON

### 统一响应格式

```json
{
  "code": 1, // 1=成功, 0=失败
  "msg": "操作成功", // 响应消息
  "data": {}, // 响应数据
  "time": 1756395183 // 时间戳
}
```

### 主要接口

#### 1. 生成钱包地址

```http
GET /v1/createAddress
```

#### 2. 查询 TRX 余额

```http
GET /v1/getTrxBalance?address={address}
```

#### 3. 查询 TRC20 余额

```http
GET /v1/getTrc20Balance?address={address}
```

#### 4. TRX 转账

```http
POST /v1/sendTrx
Content-Type: application/json

{
    "to": "接收地址",
    "amount": "转账金额",
    "key": "发送方私钥",
    "message": "备注信息(可选)"
}
```

更多接口详情请访问：http://localhost:8765/doc

## 🔧 配置说明

### 环境变量

```bash
# Flask配置
SECRET_KEY=your-secret-key
DEBUG=True

# TRON网络配置
TRON_GRID_API_KEY=your-api-key  # 可选，用于提高请求限制
```

### 配置文件

编辑 `config/config.py` 文件进行详细配置：

- TRON 网络节点地址
- TRC20 合约地址
- API 超时时间等

## 📝 开发说明

### 项目结构

```
python/
├── main.py              # 主应用文件
├── app/
│   └── api/
│       └── tron_api.py  # TRON API核心类
├── config/
│   └── config.py        # 配置文件
├── templates/
│   ├── index.html       # 主页模板
│   └── docs.html        # 文档模板
├── requirements.txt     # 依赖列表
└── README.md           # 说明文档
```

### 核心依赖

- **Flask**: Web 框架
- **tronpy**: TRON Python SDK
- **requests**: HTTP 请求库
- **mnemonic**: 助记词生成
- **hdwallet**: HD 钱包支持

## 🔧 故障排除

### 常见问题

1. **编码错误 (UnicodeDecodeError)**

   - 确保 requirements.txt 文件为 UTF-8 编码，不包含中文注释

2. **Flask-CORS 安装失败**

   - 使用信任主机参数：`pip install Flask-CORS --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org`

3. **tronpy 相关错误**

   - 确保已正确安装：`pip install tronpy==0.4.0 mnemonic==0.20`

4. **端口被占用**
   - 检查 8765 端口是否被占用：`netstat -an | findstr 8765`
   - 或在 main.py 中修改端口号

### 依赖版本

- Python 3.7+
- Flask 2.3.3
- tronpy 0.4.0
- mnemonic 0.20

## 🔒 安全注意事项

1. **私钥安全**：请确保私钥在安全环境下使用
2. **HTTPS 部署**：生产环境建议使用 HTTPS 协议
3. **API 限制**：建议添加 API 访问频率限制
4. **错误日志**：监控错误日志，及时发现问题

## 📞 联系方式

- **Telegram**: https://t.me/king_orz
- **官网**: https://www.919968.xyz/

## 📄 开源协议

本项目采用 MIT 开源协议。

---

**温馨提示**：接受各种代码定制服务 | © 2025
