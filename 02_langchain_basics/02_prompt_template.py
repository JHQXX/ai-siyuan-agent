"""
02 - 提示词模板 (Prompt Template)

Java/SpringAI 对比：
- SpringAI: PromptTemplate template = new PromptTemplate("你好，{name}");
- LangChain: ChatPromptTemplate.from_template("你好，{name}")
- 都支持变量占位符，LangChain 的功能更强大
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
    )


def basic_template():
    """基础提示词模板 - 字符串替换"""
    print("=" * 60)
    print("1. 基础提示词模板（字符串替换）")
    print("=" * 60)

    # 类似 SpringAI 的 PromptTemplate
    prompt = PromptTemplate.from_template("请用{language}翻译这句话：{text}")

    # 格式化模板 - 类似 template.create(mapOf("language", "英语", ...))
    formatted = prompt.format(language="英语", text="你好，世界")
    print(f"格式化后的提示词: {formatted}")


def chat_prompt_template():
    """对话提示词模板 - 系统提示 + 用户输入"""
    print("\n" + "=" * 60)
    print("2. 对话提示词模板（系统+用户）")
    print("=" * 60)

    # ChatPromptTemplate 用于对话场景
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个{role}，回答问题要{style}。"),
        ("human", "{question}")
    ])

    # 格式化
    messages = prompt.format_messages(
        role="数学老师",
        style="通俗易懂，多举例子",
        question="什么是勾股定理？"
    )

    print("格式化后的消息列表:")
    for msg in messages:
        print(f"  [{msg.type}] {msg.content}")

    # 调用 LLM
    llm = get_llm()
    response = llm.invoke(messages)
    print(f"\nAI 回复: {response.content}")


def prompt_chaining():
    """提示词链 - LCEL 管道语法"""
    print("\n" + "=" * 60)
    print("3. LCEL 管道语法（Prompt | LLM）")
    print("=" * 60)

    # LCEL = LangChain Expression Language
    # 用 | 连接组件，类似 Java 的 Stream API 链式调用
    prompt = ChatPromptTemplate.from_template("用{language}说一句问候语")
    llm = get_llm()

    # 管道：提示词模板 → LLM
    chain = prompt | llm

    # 调用 - 类似 Java 的 chain.apply(...)
    result = chain.invoke({"language": "日语"})
    print(f"日语问候: {result.content}")

    result = chain.invoke({"language": "法语"})
    print(f"法语问候: {result.content}")


def multi_input_template():
    """多变量复杂模板"""
    print("\n" + "=" * 60)
    print("4. 复杂模板（多个变量 + 历史消息）")
    print("=" * 60)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是{assistant_role}，擅长{expertise}。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}")
    ])

    # 模拟聊天历史
    chat_history = [
        HumanMessage(content="你好，我叫小明"),
    ]

    llm = get_llm()
    chain = prompt | llm

    result = chain.invoke({
        "assistant_role": "学习助手",
        "expertise": "Python 编程",
        "chat_history": chat_history,
        "user_input": "我该怎么学习 Python？"
    })

    print(f"AI 回复: {result.content}")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    try:
        basic_template()
        chat_prompt_template()
        prompt_chaining()
        multi_input_template()
    except Exception as e:
        print(f"\n❌ 调用出错: {e}")

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 创建一个代码审查助手的提示词模板")
    print("2. 用 LCEL 语法实现：翻译模板 → LLM → 输出结果")
    print("3. 思考：提示词模板和普通字符串格式化有什么区别？")
    print("=" * 60)


if __name__ == "__main__":
    main()
