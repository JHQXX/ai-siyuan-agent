"""
01 - 文档加载 (Document Loader)

Java/SpringAI 对比：
- SpringAI: DocumentReader / VectorStoreReader
- LangChain: DocumentLoader (TextLoader, PyPDFLoader, etc.)
- 负责从各种来源加载文档，统一成 Document 对象
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from pathlib import Path


def create_sample_docs():
    """创建示例文档，方便后续学习使用"""
    print("=" * 60)
    print("1. 创建示例文档")
    print("=" * 60)

    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base"
    kb_path.mkdir(parents=True, exist_ok=True)

    # 示例文档 1：人工智能简介
    doc1_content = """
人工智能（Artificial Intelligence，简称AI）是计算机科学的一个重要分支。
它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

人工智能的研究领域包括：
1. 机器学习（Machine Learning）
2. 深度学习（Deep Learning）
3. 自然语言处理（Natural Language Processing）
4. 计算机视觉（Computer Vision）
5. 专家系统（Expert Systems）

人工智能的应用场景非常广泛，包括：
- 智能客服
- 自动驾驶
- 医疗诊断
- 金融风控
- 智能制造
"""

    # 示例文档 2：LangChain 介绍
    doc2_content = """
LangChain 是一个用于构建大语言模型（LLM）应用的开发框架。
它的核心思想是将不同的组件链接（Chain）在一起，形成强大的应用。

LangChain 的核心组件包括：
1. 模型（Models）：各种 LLM 和嵌入模型
2. 提示词（Prompts）：提示词模板、示例选择器等
3. 链（Chains）：将多个组件组合在一起
4. 智能体（Agents）：让 LLM 自主决策使用工具
5. 记忆（Memory）：保存对话历史
6. 检索（Retrieval）：从知识库中检索相关信息

LangChain 支持多种编程语言，其中 Python 版本功能最完善。
使用 LangChain 可以大大提高开发 LLM 应用的效率。
"""

    # 示例文档 3：Python 学习指南
    doc3_content = """
Python 是一种高级编程语言，以其简洁的语法和强大的功能著称。

Python 的特点：
1. 语法简洁，易于学习
2. 丰富的标准库和第三方库
3. 跨平台，支持 Windows、Linux、macOS
4. 支持多种编程范式：面向对象、函数式、过程式
5. 强大的社区支持

Python 的主要应用领域：
- Web 开发（Django, Flask, FastAPI）
- 数据分析（Pandas, NumPy）
- 人工智能和机器学习（TensorFlow, PyTorch, LangChain）
- 自动化脚本
- 科学计算

学习 Python 的建议：
1. 先掌握基础语法
2. 多动手实践
3. 阅读优秀的代码
4. 参与开源项目
"""

    files = {
        "ai_intro.txt": doc1_content,
        "langchain_intro.txt": doc2_content,
        "python_guide.txt": doc3_content,
    }

    for filename, content in files.items():
        filepath = kb_path / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"  ✅ 创建: {filename}")

    print(f"\n📁 知识库目录: {kb_path}")
    return kb_path


def load_single_file():
    """加载单个文本文件"""
    print("\n" + "=" * 60)
    print("2. 加载单个文本文件")
    print("=" * 60)

    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base"
    file_path = kb_path / "ai_intro.txt"

    if not file_path.exists():
        create_sample_docs()

    # 使用 TextLoader 加载
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents = loader.load()

    print(f"加载文件: {file_path.name}")
    print(f"文档数量: {len(documents)}")
    print(f"文档内容长度: {len(documents[0].page_content)} 字符")
    print(f"\n文档前 200 字:\n{documents[0].page_content[:200]}...")

    # Document 对象有两个核心属性：
    # - page_content: 文档内容（字符串）
    # - metadata: 元数据（字典），比如来源、页码等
    print(f"\n元数据: {documents[0].metadata}")


def load_multiple_files():
    """加载多个文件"""
    print("\n" + "=" * 60)
    print("3. 加载多个文件")
    print("=" * 60)

    kb_path = Path(__file__).parent.parent / "data" / "knowledge_base"

    # 加载目录下所有 .txt 文件
    all_docs = []
    txt_files = sorted(kb_path.glob("*.txt"))

    for txt_file in txt_files:
        loader = TextLoader(str(txt_file), encoding="utf-8")
        docs = loader.load()
        all_docs.extend(docs)
        print(f"  加载: {txt_file.name} ({len(docs[0].page_content)} 字)")

    print(f"\n总共加载: {len(all_docs)} 个文档")
    print(f"总字符数: {sum(len(d.page_content) for d in all_docs)}")


def create_manual_document():
    """手动创建 Document 对象"""
    print("\n" + "=" * 60)
    print("4. 手动创建 Document 对象")
    print("=" * 60)

    # 有时候我们需要手动创建文档（比如从数据库、API 获取）
    doc = Document(
        page_content="这是一段手动创建的文档内容。LangChain 的 Document 非常灵活。",
        metadata={
            "source": "manual",
            "author": "测试用户",
            "created_at": "2024-01-01",
            "category": "测试"
        }
    )

    print(f"文档内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"元数据中的作者: {doc.metadata.get('author')}")


def main():
    create_sample_docs()
    load_single_file()
    load_multiple_files()
    create_manual_document()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 在 data/knowledge_base 目录下添加你自己的 .txt 文件")
    print("2. 尝试加载你添加的文件，看看 Document 的结构")
    print("3. 思考：除了 txt 文件，还可能需要加载哪些格式的文档？")
    print("=" * 60)


if __name__ == "__main__":
    main()
