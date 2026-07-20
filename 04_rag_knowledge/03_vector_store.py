"""
03 - 向量存储 (Vector Store)

Java/SpringAI 对比：
- SpringAI: VectorStore (PgVector, Neo4jVectorStore, etc.)
- LangChain: VectorStore (FAISS, Chroma, Pinecone, etc.)
- 核心思想：把文本转成向量（Embedding），然后存起来供检索
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    """获取嵌入模型"""
    settings = get_settings()
    return OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        model="text-embedding-ada-002",  # 常用的嵌入模型
    )


def get_sample_documents():
    """获取示例文档"""
    return [
        Document(
            page_content="Python 是一种高级编程语言，语法简洁，易于学习。",
            metadata={"source": "python_basic", "topic": "编程语言"}
        ),
        Document(
            page_content="Java 是一种广泛使用的编程语言，以跨平台特性著称。",
            metadata={"source": "java_basic", "topic": "编程语言"}
        ),
        Document(
            page_content="LangChain 是一个用于构建大语言模型应用的开发框架。",
            metadata={"source": "langchain_intro", "topic": "AI框架"}
        ),
        Document(
            page_content="FAISS 是 Facebook 开发的向量相似度搜索库，速度很快。",
            metadata={"source": "faiss_intro", "topic": "数据库"}
        ),
        Document(
            page_content="RAG（检索增强生成）可以让 LLM 基于私有知识库回答问题。",
            metadata={"source": "rag_intro", "topic": "AI技术"}
        ),
        Document(
            page_content="向量数据库用于存储和检索高维向量数据，是 RAG 系统的核心组件。",
            metadata={"source": "vector_db", "topic": "数据库"}
        ),
        Document(
            page_content="Go 语言又称 Golang，是 Google 开发的编程语言，擅长高并发。",
            metadata={"source": "go_basic", "topic": "编程语言"}
        ),
    ]


def basic_vector_store():
    """基础向量存储 - 创建和检索"""
    print("=" * 60)
    print("1. 基础向量存储：创建 + 相似度检索")
    print("=" * 60)

    documents = get_sample_documents()
    embeddings = get_embeddings()

    print(f"文档数量: {len(documents)}")
    print("正在创建向量索引...")

    # 用 FAISS 创建向量存储
    # 过程：文本 → Embedding 模型 → 向量 → 存入 FAISS
    vector_store = FAISS.from_documents(documents, embeddings)

    print("✅ 向量索引创建完成！\n")

    # 相似度搜索
    query = "什么是 RAG？"
    print(f"查询: {query}")

    # search_type="similarity"：相似度检索
    results = vector_store.similarity_search(query, k=3)  # 返回最相关的 3 个

    print(f"\n最相关的 {len(results)} 个文档:")
    for i, doc in enumerate(results, 1):
        print(f"\n  {i}. [{doc.metadata.get('topic', '未知')}] {doc.page_content}")
        print(f"     来源: {doc.metadata.get('source')}")


def similarity_with_score():
    """带分数的相似度检索"""
    print("\n" + "=" * 60)
    print("2. 带分数的相似度检索")
    print("=" * 60)

    documents = get_sample_documents()
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)

    query = "编程语言有哪些？"
    print(f"查询: {query}")

    # similarity_search_with_score 返回（文档, 分数）
    # 注意：FAISS 的分数是距离，越小越相似！
    results = vector_store.similarity_search_with_score(query, k=5)

    print(f"\n检索结果（分数越小越相关）:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n  {i}. 相关度分数: {score:.4f}")
        print(f"     内容: {doc.page_content}")
        print(f"     主题: {doc.metadata.get('topic')}")


def mmr_search():
    """MMR 检索 - 最大边缘相关性（兼顾相关性和多样性）"""
    print("\n" + "=" * 60)
    print("3. MMR 检索（最大边缘相关性）")
    print("   兼顾相关性和结果多样性")
    print("=" * 60)

    documents = get_sample_documents()
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)

    query = "编程语言"
    print(f"查询: {query}")

    # MMR: Maximum Marginal Relevance
    # 既考虑和查询的相似度，又考虑结果之间的差异性
    results = vector_store.max_marginal_relevance_search(
        query,
        k=4,           # 返回结果数
        fetch_k=10,    # 先取最相关的 10 个
        lambda_mult=0.5,  # 多样性参数，0=最多样，1=最相关
    )

    print(f"\nMMR 检索结果:")
    for i, doc in enumerate(results, 1):
        print(f"\n  {i}. [{doc.metadata.get('topic')}] {doc.page_content}")


def save_and_load():
    """保存和加载向量索引"""
    print("\n" + "=" * 60)
    print("4. 保存和加载向量索引（持久化）")
    print("=" * 60)

    documents = get_sample_documents()
    embeddings = get_embeddings()

    index_path = Path(__file__).parent.parent / "data" / "faiss_index"
    index_path.mkdir(parents=True, exist_ok=True)

    # 创建并保存
    print("正在创建并保存向量索引...")
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(str(index_path))
    print(f"✅ 已保存到: {index_path}")

    # 加载（不需要重新计算嵌入！）
    print("\n正在加载向量索引...")
    loaded_store = FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True  # 注意：只加载可信来源的索引
    )
    print("✅ 加载成功！")

    # 测试检索
    results = loaded_store.similarity_search("什么是向量数据库？", k=2)
    print(f"\n测试检索结果:")
    for doc in results:
        print(f"  - {doc.page_content}")


def add_new_documents():
    """向已有向量库添加新文档"""
    print("\n" + "=" * 60)
    print("5. 向向量库添加新文档")
    print("=" * 60)

    documents = get_sample_documents()
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(documents, embeddings)

    # 新文档
    new_docs = [
        Document(
            page_content="Rust 是一种系统级编程语言，注重安全性和性能。",
            metadata={"source": "rust_basic", "topic": "编程语言"}
        ),
        Document(
            page_content="Chroma 是一个开源的向量数据库，专为 LLM 应用设计。",
            metadata={"source": "chroma_intro", "topic": "数据库"}
        ),
    ]

    print(f"添加前文档数: {vector_store.index.ntotal}")
    print(f"添加 {len(new_docs)} 个新文档...")

    vector_store.add_documents(new_docs)

    print(f"添加后文档数: {vector_store.index.ntotal}")

    # 测试新文档是否可检索
    results = vector_store.similarity_search("Rust 语言", k=1)
    print(f"\n检索 'Rust 语言': {results[0].page_content}")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    try:
        basic_vector_store()
        similarity_with_score()
        mmr_search()
        save_and_load()
        add_new_documents()
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 把你自己的文档加入向量库，试试检索效果")
    print("2. 调整 k 值和检索方式，比较结果的差异")
    print("3. 思考：MMR 和普通相似度检索各自适合什么场景？")
    print("=" * 60)


if __name__ == "__main__":
    main()
