"""
04 - Chain 组合 (LCEL)

Java/SpringAI 对比：
- SpringAI: 相对简单的链式调用
- LangChain: LCEL（LangChain Expression Language）非常强大
- 支持管道符 | 连接，类似 Java Stream / Unix Pipeline
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from operator import itemgetter


def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=0.7,
    )


def simple_chain():
    """最简单的链：Prompt → LLM → Parser"""
    print("=" * 60)
    print("1. 基础链：Prompt → LLM → Parser")
    print("=" * 60)

    prompt = ChatPromptTemplate.from_template("用一句话解释{topic}，要通俗易懂")
    llm = get_llm()
    parser = StrOutputParser()

    # 用 | 连接起来，就像 Unix 管道
    chain = prompt | llm | parser

    result = chain.invoke({"topic": "区块链"})
    print(f"解释区块链: {result}")


def sequential_chain():
    """顺序链：多个步骤依次执行"""
    print("\n" + "=" * 60)
    print("2. 顺序链：先翻译，再总结")
    print("=" * 60)

    # 第一步：翻译成英文
    translate_prompt = ChatPromptTemplate.from_template(
        "将以下内容翻译成英文：{text}"
    )

    # 第二步：总结要点
    summarize_prompt = ChatPromptTemplate.from_template(
        "用 3 个要点总结以下英文内容：{english_text}"
    )

    llm = get_llm()
    parser = StrOutputParser()

    # 方式一：手动传递（简单直观）
    translate_chain = translate_prompt | llm | parser

    # 方式二：使用 RunnableLambda 处理输入
    # 类似 Java 的 Function.andThen()
    full_chain = (
        translate_chain
        | (lambda english: {"english_text": english})
        | summarize_prompt
        | llm
        | parser
    )

    result = full_chain.invoke({
        "text": "人工智能是计算机科学的一个分支，它企图了解智能的实质，"
                "并生产出一种新的能以人类智能相似的方式做出反应的智能机器。"
    })

    print(f"总结结果:\n{result}")


def parallel_chain():
    """并行链：多个任务同时执行"""
    print("\n" + "=" * 60)
    print("3. 并行链：同时获取多个观点")
    print("=" * 60)

    llm = get_llm()
    parser = StrOutputParser()

    # RunnableParallel 可以并行执行多个链
    # 类似 Java 的 CompletableFuture.allOf()
    parallel_chain = RunnableParallel(
        # 专家观点
        expert=(
            ChatPromptTemplate.from_template("用专家视角分析{topic}的优缺点，200字以内")
            | llm | parser
        ),
        # 初学者观点
        beginner=(
            ChatPromptTemplate.from_template("用初学者视角解释{topic}是什么，200字以内")
            | llm | parser
        ),
        # 应用场景
        use_cases=(
            ChatPromptTemplate.from_template("列举{topic}的3个典型应用场景")
            | llm | parser
        ),
    )

    result = parallel_chain.invoke({"topic": "大语言模型"})

    print(f"🔬 专家观点:\n{result['expert']}\n")
    print(f"👶 初学者视角:\n{result['beginner']}\n")
    print(f"💼 应用场景:\n{result['use_cases']}")


def branch_chain():
    """分支链：根据条件走不同路径"""
    print("\n" + "=" * 60)
    print("4. 分支链：根据问题类型选择不同回答")
    print("=" * 60)

    llm = get_llm()
    parser = StrOutputParser()

    # 分类链：先判断问题类型
    classify_chain = (
        ChatPromptTemplate.from_template("""
判断以下问题属于哪个类别，只回答类别名称：
- 技术问题
- 生活问题
- 学习问题

问题：{question}
""")
        | llm | parser
    )

    # 不同类别的回答链
    tech_chain = (
        ChatPromptTemplate.from_template("用技术专家的口吻回答：{question}")
        | llm | parser
    )
    life_chain = (
        ChatPromptTemplate.from_template("用生活达人的口吻回答：{question}")
        | llm | parser
    )
    study_chain = (
        ChatPromptTemplate.from_template("用学习导师的口吻回答：{question}")
        | llm | parser
    )

    # 路由函数 - 根据分类结果选择链
    def route(info):
        category = info["category"].strip()
        question = info["question"]
        if "技术" in category:
            return tech_chain.invoke({"question": question})
        elif "生活" in category:
            return life_chain.invoke({"question": question})
        else:
            return study_chain.invoke({"question": question})

    # 组合：分类 → 路由 → 回答
    full_chain = (
        {"category": classify_chain, "question": itemgetter("question")}
        | RunnableLambda(route)
    )

    result = full_chain.invoke({"question": "怎么学习 Python 才高效？"})
    print(f"回答:\n{result}")


def async_chain():
    """异步调用链"""
    print("\n" + "=" * 60)
    print("5. 异步调用链（.ainvoke）")
    print("=" * 60)
    import asyncio

    prompt = ChatPromptTemplate.from_template("用一句话介绍{language}编程语言")
    llm = get_llm()
    parser = StrOutputParser()
    chain = prompt | llm | parser

    async def main_async():
        # 并发调用多个
        results = await asyncio.gather(
            chain.ainvoke({"language": "Python"}),
            chain.ainvoke({"language": "Java"}),
            chain.ainvoke({"language": "Go"}),
        )
        for lang, result in zip(["Python", "Java", "Go"], results):
            print(f"  {lang}: {result}")

    asyncio.run(main_async())


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    try:
        simple_chain()
        sequential_chain()
        parallel_chain()
        branch_chain()
        async_chain()
    except Exception as e:
        print(f"\n❌ 调用出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 实现一个链：先生成一个故事大纲，再根据大纲生成完整故事")
    print("2. 用并行链同时获取 3 个不同城市的天气描述（模拟）")
    print("3. 理解 LCEL 的设计思想：为什么用 | 而不是方法调用？")
    print("=" * 60)


if __name__ == "__main__":
    main()
