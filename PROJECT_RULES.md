# AI Siyuan Agent - 项目规则

> 专为 Java/SpringAI 开发者设计的 Python 智能体学习项目

---

## 一、项目定位

本项目是一个**循序渐进的 Python 智能体学习项目**，帮助有 Java/SpringAI 背景的开发者快速掌握 Python 生态下的智能体开发技术栈。

### 目标学习者
- 有 Java 开发经验，熟悉 SpringAI 框架
- Python 初学者，希望系统学习智能体开发
- 想了解 LangChain/LangGraph 等 Python 智能体框架

### 学习路径

```
01_python_basics    →  Python 基础语法（Java 开发者视角）
02_langchain_basics →  LangChain 基础（对比 SpringAI 概念）
03_agent_core       →  智能体核心（工具调用、ReAct 模式）
04_rag_knowledge    →  RAG 知识库系统
05_projects         →  综合实战项目
```

---

## 二、目录结构规范

```
ai-siyuan-agent/
├── 01_python_basics/      # Python 基础入门
│   ├── 01_hello_python.py      # 第一个 Python 程序
│   ├── 02_data_types.py        # 数据类型与集合
│   ├── 03_functions.py         # 函数与模块
│   ├── 04_oop.py               # 面向对象编程
│   └── 05_async_await.py       # 异步编程
│
├── 02_langchain_basics/    # LangChain 基础
│   ├── 01_llm_chat.py           # 大模型对话
│   ├── 02_prompt_template.py    # 提示词模板
│   ├── 03_output_parser.py      # 输出解析器
│   └── 04_chain_composition.py  # Chain 组合
│
├── 03_agent_core/          # 智能体核心
│   ├── 01_simple_tool.py        # 简单工具定义
│   ├── 02_react_agent.py        # ReAct 智能体
│   └── 03_multi_tool_agent.py   # 多工具智能体
│
├── 04_rag_knowledge/       # RAG 知识库
│   ├── 01_document_loader.py    # 文档加载
│   ├── 02_text_splitter.py      # 文本分割
│   ├── 03_vector_store.py       # 向量存储
│   └── 04_rag_chain.py          # RAG 问答链
│
├── 05_projects/            # 综合项目
│   └── weather_agent/          # 天气查询智能体
│
├── config/                  # 配置文件
│   ├── .env.example           # 环境变量示例
│   └── settings.py            # 配置管理
│
├── data/                    # 数据目录
│   ├── knowledge_base/       # 知识库文件
│   └── faiss_index/          # FAISS 向量索引
│
├── tests/                   # 测试文件
├── requirements.txt         # Python 依赖
└── PROJECT_RULES.md         # 本文件
```

---

## 三、编码规范

### 3.1 Python 代码风格

- 遵循 **PEP 8** 规范
- 使用 4 空格缩进（不用 Tab）
- 变量/函数使用 `snake_case`（对比 Java 的 `camelCase`）
- 类名使用 `PascalCase`（与 Java 一致）
- 常量使用 `UPPER_SNAKE_CASE`

```python
# 正确示例
class UserProfile:
    MAX_RETRY_COUNT = 3

    def get_user_info(self, user_id: str) -> dict:
        """获取用户信息"""
        pass
```

### 3.2 类型提示（Type Hints）

Python 是动态类型语言，但**强烈建议使用类型提示**，这会让 Java 开发者更有安全感：

```python
# 函数参数和返回值类型
def add_numbers(a: int, b: int) -> int:
    return a + b

# 复杂类型（需要从 typing 导入）
from typing import List, Dict, Optional, Union

def process_users(users: List[Dict[str, str]]) -> Optional[str]:
    pass
```

### 3.3 模块与包

- 每个目录下放置 `__init__.py` 表示这是一个 Python 包
- 模块名使用小写+下划线
- 导入顺序：标准库 → 第三方库 → 本地模块

```python
# 标准库
import os
import sys
from datetime import datetime

# 第三方库
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 本地模块
from config.settings import get_settings
```

---

## 四、智能体开发规范

### 4.1 LLM 配置规范

**所有 LLM 配置必须通过环境变量读取，禁止硬编码 API Key！**

```python
# 正确做法
import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.7,
)

# 错误做法：禁止硬编码
# llm = ChatOpenAI(api_key="sk-xxxxxx")
```

### 4.2 工具定义规范

工具函数必须包含：
1. 清晰的函数名和参数
2. 完整的 docstring（描述工具用途，LLM 依赖这个理解工具）
3. 明确的参数类型和返回类型

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """
    查询指定城市的天气信息。
    
    Args:
        city: 城市名称，例如"北京"、"上海"
        
    Returns:
        天气信息字符串
    """
    return f"{city}今天晴，温度 25°C"
```

### 4.3 智能体创建规范

优先使用 LangChain 新版 API（create_react_agent 等），避免使用过时的 `initialize_agent`。

---

## 五、学习规则

### 5.1 学习顺序

必须按编号顺序学习，每个模块都有示例代码和练习：

1. ✅ `01_python_basics` - 先掌握 Python 语法
2. ✅ `02_langchain_basics` - 理解 LangChain 核心概念
3. ✅ `03_agent_core` - 智能体核心能力
4. ✅ `04_rag_knowledge` - RAG 知识库
5. ✅ `05_projects` - 综合实战

### 5.2 Java → Python 概念对照

| Java/SpringAI 概念 | Python/LangChain 对应 | 说明 |
|-------------------|---------------------|------|
| `@Bean` / 依赖注入 | 直接实例化 / `pydantic` | Python 更灵活 |
| `ChatClient` | `ChatOpenAI` / `ChatModel` | 大模型对话接口 |
| `PromptTemplate` | `ChatPromptTemplate` | 提示词模板 |
| `ToolCallback` / `@Tool` | `@tool` 装饰器 | 工具定义 |
| `AiServices` | `create_react_agent` | 智能体创建 |
| `VectorStore` | `FAISS` / `Chroma` | 向量数据库 |
| `StreamingResponse` | `.stream()` 方法 | 流式输出 |

### 5.3 每模块学习方法

1. **阅读代码** - 先看懂示例代码中的注释
2. **运行代码** - 实际运行，观察输出
3. **修改实验** - 尝试修改参数，看效果变化
4. **做练习题** - 每个模块末尾有练习题目
5. **对比 Java** - 思考和 Java/SpringAI 的异同

---

## 六、版本与依赖规范

### 6.1 Python 版本

- 最低要求：Python 3.10+
- 推荐版本：Python 3.11 或 3.12

### 6.2 核心依赖版本策略

使用稳定版本，避免盲目追新：

```
langchain>=0.3.0          # 核心框架
langchain-openai>=0.2.0   # OpenAI 集成
langchain-community>=0.3.0 # 社区工具
langchain-core>=0.3.0     # 核心抽象
langchain-text-splitters>=0.3.0  # 文本分割
faiss-cpu>=1.8.0          # 向量数据库（CPU 版）
python-dotenv>=1.0.0      # 环境变量管理
pydantic>=2.0.0           # 数据验证（类似 Java 的 Bean Validation）
```

### 6.3 虚拟环境

**必须使用虚拟环境隔离项目依赖！**

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

---

## 七、配置管理规范

### 7.1 环境变量

所有敏感配置通过环境变量管理，使用 `.env` 文件（**不要提交到 git！**）

```bash
# 复制示例文件
cp config/.env.example .env

# 编辑 .env 文件，填入你的配置
```

### 7.2 .env 文件模板

```env
# 大模型配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7

# 向量数据库配置
VECTOR_STORE_PATH=./data/faiss_index

# 其他配置
DEBUG=true
LOG_LEVEL=INFO
```

---

## 八、代码提交规范（如使用 git）

### 8.1 提交信息格式

```
<type>(<scope>): <subject>

类型 type:
- feat: 新功能/新学习模块
- fix: 修复问题
- docs: 文档更新
- refactor: 代码重构
- test: 测试相关
- chore: 构建/工具配置
```

### 8.2 忽略文件

`.gitignore` 至少包含：
```
venv/
__pycache__/
.env
*.pyc
data/faiss_index/
.idea/
.vscode/
```

---

## 九、问题排查指南

### 9.1 ImportError 常见原因

1. **模块路径变化** - LangChain 版本升级快，模块经常拆分
   - 旧：`from langchain.chat_models import ChatOpenAI`
   - 新：`from langchain_openai import ChatOpenAI`

2. **忘记安装依赖** - 检查 `requirements.txt` 是否包含该包

3. **虚拟环境未激活** - 确认 `(venv)` 出现在命令行前

### 9.2 API 调用失败排查

1. 检查 API Key 是否正确配置
2. 检查网络连接和代理设置
3. 检查模型名称是否正确
4. 检查账户余额/额度

---

## 十、项目扩展原则

当你学完基础后，可以按以下方向扩展：

1. **多智能体协作** - 学习 LangGraph
2. **记忆系统** - 短期记忆、长期记忆
3. **更多工具** - 搜索、计算、文件操作
4. **前端界面** - Streamlit / Gradio
5. **部署上线** - FastAPI / Docker

---

## 附：快速开始

```bash
# 1. 克隆/进入项目目录
cd ai-siyuan-agent

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp config/.env.example .env
# 编辑 .env 填入你的 API Key

# 5. 开始学习！从 01 模块开始
python 01_python_basics/01_hello_python.py
```

---

> **记住：编程是练出来的，不是看出来的。每段代码都要亲手运行和修改！**
