"""
02 - 文本分割 (Text Splitter)

Java/SpringAI 对比：
- SpringAI: DocumentSplitter / TokenTextSplitter
- LangChain: TextSplitter (RecursiveCharacterTextSplitter, etc.)
- 为什么要分割？LLM 有 token 限制，太长的文档塞不下
- 同时分割后的小块检索更精准
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
)


def get_sample_document() -> Document:
    """获取示例文档"""
    content = """
Python 是一种非常流行的编程语言。它的语法简洁，易于学习，同时功能强大。

Python 的应用场景非常广泛。在 Web 开发领域，Django 和 Flask 是最常用的框架。
Django 提供了全栈解决方案，而 Flask 更加轻量灵活。

在数据科学领域，Python 同样占据主导地位。NumPy 提供了高效的数值计算能力，
Pandas 则让数据处理变得简单直观。Matplotlib 和 Seaborn 可以用来创建各种可视化图表。

人工智能和机器学习是 Python 最热门的应用领域之一。
TensorFlow 和 PyTorch 是两大主流深度学习框架。
LangChain 则让构建大语言模型应用变得更加容易。

Python 还有丰富的标准库，涵盖了文件操作、网络编程、正则表达式等各个方面。
同时，PyPI 上有数十万个第三方包，可以满足各种开发需求。

学习 Python 需要掌握以下要点：
1. 基础语法：变量、数据类型、控制流、函数
2. 面向对象编程：类、继承、多态
3. 异常处理：try-except-finally
4. 模块和包：import 机制
5. 常用库：os, sys, json, datetime 等
6. 虚拟环境：venv, conda
7. 包管理：pip, poetry

Python 的设计哲学是"优雅"、"明确"、"简单"。
正如 Python 之禅所说：Simple is better than complex.
"""
    return Document(page_content=content.strip(), metadata={"source": "python_guide"})


def character_splitter_demo():
    """CharacterTextSplitter - 按字符数分割"""
    print("=" * 60)
    print("1. CharacterTextSplitter - 按字符数分割")
    print("=" * 60)

    doc = get_sample_document()

    splitter = CharacterTextSplitter(
        separator="\n\n",  # 分隔符：段落
        chunk_size=200,     # 每块最大字符数
        chunk_overlap=20,   # 块之间重叠字符数（保证上下文连续）
        length_function=len,
    )

    chunks = splitter.split_documents([doc])

    print(f"原文长度: {len(doc.page_content)} 字符")
    print(f"分割后块数: {len(chunks)}")
    print()

    for i, chunk in enumerate(chunks, 1):
        print(f"--- 第 {i} 块 (长度: {len(chunk.page_content)}) ---")
        print(chunk.page_content[:100] + "..." if len(chunk.page_content) > 100 else chunk.page_content)
        print()


def recursive_character_splitter_demo():
    """RecursiveCharacterTextSplitter - 递归字符分割（最常用）"""
    print("=" * 60)
    print("2. RecursiveCharacterTextSplitter - 递归字符分割（推荐）")
    print("=" * 60)

    doc = get_sample_document()

    # 递归分割：先按段落分，太大再按句子分，再太大按单词分，最后按字符分
    # 这样可以尽量保持语义完整性
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],  # 中文友好的分隔符
    )

    chunks = splitter.split_documents([doc])

    print(f"原文长度: {len(doc.page_content)} 字符")
    print(f"分割后块数: {len(chunks)}")
    print()

    for i, chunk in enumerate(chunks, 1):
        print(f"--- 第 {i} 块 (长度: {len(chunk.page_content)}) ---")
        print(chunk.page_content)
        print()


def token_splitter_demo():
    """TokenTextSplitter - 按 token 数分割"""
    print("\n" + "=" * 60)
    print("3. TokenTextSplitter - 按 token 数分割")
    print("   （更接近 LLM 的实际限制）")
    print("=" * 60)

    doc = get_sample_document()

    # 按 token 分割，更贴近 LLM 的上下文窗口限制
    splitter = TokenTextSplitter(
        chunk_size=100,    # 每块最大 token 数
        chunk_overlap=10,  # 重叠 token 数
    )

    chunks = splitter.split_documents([doc])

    print(f"原文长度: {len(doc.page_content)} 字符")
    print(f"分割后块数: {len(chunks)}")
    print()

    for i, chunk in enumerate(chunks[:3], 1):  # 只显示前 3 块
        print(f"--- 第 {i} 块 ---")
        print(chunk.page_content[:150] + "...")
        print()


def split_multiple_docs():
    """分割多个文档"""
    print("\n" + "=" * 60)
    print("4. 分割多个文档并保留元数据")
    print("=" * 60)

    docs = [
        Document(
            page_content="Python 是一种编程语言。它简单易学，功能强大。",
            metadata={"source": "doc1", "category": "编程"}
        ),
        Document(
            page_content="Java 也是一种编程语言。它跨平台，企业级应用广泛。",
            metadata={"source": "doc2", "category": "编程"}
        ),
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=20,
        chunk_overlap=5,
    )

    all_chunks = []
    for doc in docs:
        chunks = splitter.split_documents([doc])
        all_chunks.extend(chunks)

    print(f"原文档数: {len(docs)}")
    print(f"分割后块数: {len(all_chunks)}")
    print()

    for i, chunk in enumerate(all_chunks, 1):
        print(f"第 {i} 块:")
        print(f"  内容: {chunk.page_content}")
        print(f"  来源: {chunk.metadata.get('source')}")
        print(f"  分类: {chunk.metadata.get('category')}")
        print()


def main():
    character_splitter_demo()
    recursive_character_splitter_demo()
    token_splitter_demo()
    split_multiple_docs()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 调整 chunk_size 和 chunk_overlap，观察分割结果的变化")
    print("2. 找一篇长文章保存为 txt，试试不同的分割方式")
    print("3. 思考：为什么需要 chunk_overlap？重叠多少合适？")
    print("=" * 60)


if __name__ == "__main__":
    main()
