# AI Siyuan Agent - Python 智能体学习项目

> 专为 Java/SpringAI 开发者设计的 Python 智能体学习路径

---

## 📖 项目简介

这是一个**循序渐进的 Python 智能体学习项目**，帮助有 Java 和 SpringAI 开发经验的开发者快速掌握 Python 生态下的智能体开发技术栈。

每个模块都配有：
- ✅ 完整的示例代码
- ✅ 详细的中文注释
- ✅ Java/SpringAI 概念对比
- ✅ 课后练习题

---

## 🗺️ 学习路径

```
01_python_basics          02_langchain_basics
┌─────────────────┐       ┌─────────────────┐
│ Python 基础语法 │──────▶│ LangChain 基础   │
│ (Java 开发者视角)│       │ (对比 SpringAI) │
└─────────────────┘       └─────────────────┘
           │                        │
           ▼                        ▼
03_agent_core              04_rag_knowledge
┌─────────────────┐       ┌─────────────────┐
│ 智能体核心      │       │ RAG 知识库系统  │
│ 工具调用        │       │ 文档加载        │
│ ReAct 模式      │◀─────▶│ 向量存储        │
│ 多智能体        │       │ 检索增强生成    │
└─────────────────┘       └─────────────────┘
           │                        │
           └──────────┬─────────────┘
                      ▼
              05_projects
         ┌──────────────────┐
         │  综合实战项目    │
         │  天气查询智能体  │
         └──────────────────┘
```

---

## 📚 模块详解

### 第一阶段：Python 基础（01_python_basics）

| 文件 | 内容 | Java 对应概念 |
|------|------|-------------|
| [01_hello_python.py](file:///Users/lizhi/projects/ai-siyuan-agent/01_python_basics/01_hello_python.py) | 第一个 Python 程序 | main 方法、System.out.println |
| [02_data_types.py](file:///Users/lizhi/projects/ai-siyuan-agent/01_python_basics/02_data_types.py) | 数据类型与集合 | 基本类型、ArrayList、HashMap |
| [03_functions.py](file:///Users/lizhi/projects/ai-siyuan-agent/01_python_basics/03_functions.py) | 函数与模块 | 方法、重载、Function 接口 |
| [04_oop.py](file:///Users/lizhi/projects/ai-siyuan-agent/01_python_basics/04_oop.py) | 面向对象编程 | 类、继承、多态 |
| [05_async_await.py](file:///Users/lizhi/projects/ai-siyuan-agent/01_python_basics/05_async_await.py) | 异步编程 | CompletableFuture |

### 第二阶段：LangChain 基础（02_langchain_basics）

| 文件 | 内容 | SpringAI 对应 |
|------|------|-------------|
| [01_llm_chat.py](file:///Users/lizhi/projects/ai-siyuan-agent/02_langchain_basics/01_llm_chat.py) | 大模型对话 | ChatClient |
| [02_prompt_template.py](file:///Users/lizhi/projects/ai-siyuan-agent/02_langchain_basics/02_prompt_template.py) | 提示词模板 | PromptTemplate |
| [03_output_parser.py](file:///Users/lizhi/projects/ai-siyuan-agent/02_langchain_basics/03_output_parser.py) | 输出解析器 | BeanOutputParser |
| [04_chain_composition.py](file:///Users/lizhi/projects/ai-siyuan-agent/02_langchain_basics/04_chain_composition.py) | Chain 组合（LCEL） | 链式调用 |

### 第三阶段：智能体核心（03_agent_core）

| 文件 | 内容 | SpringAI 对应 |
|------|------|-------------|
| [01_simple_tool.py](file:///Users/lizhi/projects/ai-siyuan-agent/03_agent_core/01_simple_tool.py) | 工具定义 | @Tool / ToolCallback |
| [02_react_agent.py](file:///Users/lizhi/projects/ai-siyuan-agent/03_agent_core/02_react_agent.py) | ReAct 智能体 | AiServices |
| [03_multi_tool_agent.py](file:///Users/lizhi/projects/ai-siyuan-agent/03_agent_core/03_multi_tool_agent.py) | 多工具智能体 | 多工具组合 |

### 第四阶段：RAG 知识库（04_rag_knowledge）

| 文件 | 内容 | SpringAI 对应 |
|------|------|-------------|
| [01_document_loader.py](file:///Users/lizhi/projects/ai-siyuan-agent/04_rag_knowledge/01_document_loader.py) | 文档加载 | DocumentReader |
| [02_text_splitter.py](file:///Users/lizhi/projects/ai-siyuan-agent/04_rag_knowledge/02_text_splitter.py) | 文本分割 | DocumentSplitter |
| [03_vector_store.py](file:///Users/lizhi/projects/ai-siyuan-agent/04_rag_knowledge/03_vector_store.py) | 向量存储 | VectorStore |
| [04_rag_chain.py](file:///Users/lizhi/projects/ai-siyuan-agent/04_rag_knowledge/04_rag_chain.py) | RAG 问答链 | RetrievalAugmentedAdvisor |

### 第五阶段：综合实战（05_projects）

| 项目 | 内容 |
|------|------|
| [weather_agent](file:///Users/lizhi/projects/ai-siyuan-agent/05_projects/weather_agent) | 天气查询智能体 |

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 确认 Python 版本（需要 3.10+）
python --version

# 克隆或进入项目目录
cd ai-siyuan-agent
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制配置模板
cp config/.env.example .env

# 编辑 .env 文件，填入你的 API Key
# 如果你使用的是 OpenAI 兼容接口（如通义千问、DeepSeek 等），
# 记得修改 OPENAI_BASE_URL 和 LLM_MODEL
```

### 5. 开始学习！

```bash
# 从第一个模块开始
python 01_python_basics/01_hello_python.py

# 然后按顺序学习...
python 01_python_basics/02_data_types.py
python 01_python_basics/03_functions.py
# ... 以此类推
```

---

## 📋 项目规则

详细的项目规则和规范请查看 [PROJECT_RULES.md](file:///Users/lizhi/projects/ai-siyuan-agent/PROJECT_RULES.md)，包含：

- 编码规范
- 智能体开发规范
- 版本与依赖规范
- 配置管理规范
- 问题排查指南

---

## 🔧 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 编程语言 | Python 3.10+ | 动态类型 + 类型提示 |
| LLM 框架 | LangChain | 智能体开发核心框架 |
| 向量数据库 | FAISS | Facebook 开源，快速高效 |
| 配置管理 | pydantic + dotenv | 类型安全的配置 |
| 数据验证 | Pydantic | 类似 Java 的 Bean Validation |

---

## 💡 Java → Python 速查表

| Java/SpringAI | Python/LangChain |
|--------------|-----------------|
| `public class User` | `class User:` |
| `void main(String[] args)` | `if __name__ == "__main__":` |
| `System.out.println()` | `print()` |
| `ArrayList<String>` | `list[str]` |
| `HashMap<String, Object>` | `dict[str, Any]` |
| `@Bean` / DI | 直接实例化 / 模块单例 |
| `ChatClient` | `ChatOpenAI` |
| `PromptTemplate` | `ChatPromptTemplate` |
| `@Tool` | `@tool` 装饰器 |
| `AiServices` | `create_react_agent` |
| `VectorStore` | `FAISS` / `Chroma` |
| `BeanOutputParser` | `PydanticOutputParser` |
| `CompletableFuture` | `asyncio` + `async/await` |

---

## 📝 学习建议

1. **按顺序学习** - 每个模块都建立在前一个的基础上
2. **亲手运行** - 每段代码都要运行一遍，观察输出
3. **修改实验** - 尝试修改参数，看效果有什么不同
4. **做练习题** - 每个模块最后都有练习题，一定要做
5. **对比 Java** - 思考和 Java/SpringAI 的异同，加深理解
6. **多查文档** - [LangChain 官方文档](https://python.langchain.com/)是最好的参考

---

## ❓ 常见问题

### Q: 我没有 OpenAI 的 API Key 怎么办？
A: 你可以使用任何兼容 OpenAI 格式的模型服务，比如：
- 阿里云通义千问
- 字节豆包
- DeepSeek
- 本地 Ollama

只需要修改 `.env` 中的 `OPENAI_BASE_URL` 和 `LLM_MODEL` 即可。

### Q: LangChain 版本变化快，代码跑不起来怎么办？
A: 
1. 检查 `requirements.txt` 中的版本号
2. 查看官方文档的迁移指南
3. 模块路径变化是常见问题：旧版 `langchain.xxx` → 新版 `langchain_xxx`

### Q: 我应该学到什么程度算掌握了？
A: 当你能够：
- 独立定义工具函数
- 构建一个简单的 ReAct 智能体
- 用自己的文档做 RAG 问答
- 排查常见的 ImportError 和 API 调用错误

就算入门了！接下来就可以做更复杂的项目了。

---

## 📚 延伸学习

学完本项目后，可以继续学习：

- **LangGraph** - 多智能体协作、状态管理
- **Streamlit** - 快速构建 Web 界面
- **FastAPI** - 把智能体做成 API 服务
- **LangSmith** - 调试和监控 LLM 应用
- **记忆系统** - 短期记忆、长期记忆
- **更多工具** - 搜索、代码执行、文件操作

---

> **记住：编程是练出来的，不是看出来的。每段代码都要亲手运行和修改！**
