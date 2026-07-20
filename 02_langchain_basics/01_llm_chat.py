"""
01 - 大模型对话 (LLM Chat)

Java/SpringAI 对比：
- SpringAI: ChatClient chatClient = ChatClient.builder(chatModel).build();
- LangChain: llm = ChatOpenAI(...)
- 对话调用: llm.invoke("你好") 类似 chatClient.prompt("你好").call().content()
"""

import sys
import os

# 加入项目根目录到路径，方便导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import get_settings, is_config_ready, print_config_status
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


def get_llm():
    """获取 LLM 实例 - 类似 SpringAI 中配置 ChatModel Bean"""
    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
    )
    return llm


def simple_chat():
    """最简单的对话 - 一问一答"""
    print("=" * 60)
    print("1. 最简单的对话（一问一答）")
    print("=" * 60)

    llm = get_llm()

    # 调用 LLM - invoke 类似 SpringAI 的 call()
    # HumanMessage 表示用户消息
    response = llm.invoke([HumanMessage(content="你好，请用一句话介绍一下自己")])

    # response.content 就是回复内容
    print(f"AI 回复: {response.content}")


def multi_turn_chat():
    """多轮对话 - 带历史消息"""
    print("\n" + "=" * 60)
    print("2. 多轮对话（带历史消息）")
    print("=" * 60)

    llm = get_llm()

    # 消息列表：SystemMessage(系统提示) + HumanMessage(用户) + AIMessage(AI)
    # 类似 Java 中维护一个 List<Message>
    messages = [
        SystemMessage(content="你是一个专业的程序员助手，回答问题要简洁准确。"),
        HumanMessage(content="什么是 Python 的列表推导式？"),
    ]

    # 第一轮
    response1 = llm.invoke(messages)
    print(f"用户: {messages[-1].content}")
    print(f"AI: {response1.content}")

    # 把 AI 回复加入历史，然后问下一个问题
    messages.append(AIMessage(content=response1.content))
    messages.append(HumanMessage(content="能举个例子吗？"))

    # 第二轮
    response2 = llm.invoke(messages)
    print(f"\n用户: {messages[-1].content}")
    print(f"AI: {response2.content}")


def stream_chat():
    """流式输出 - 类似 SpringAI 的 StreamingResponse"""
    print("\n" + "=" * 60)
    print("3. 流式输出（一个字一个字出来）")
    print("=" * 60)

    llm = get_llm()

    print("AI: ", end="", flush=True)
    # stream() 方法返回迭代器，逐个输出 token
    for chunk in llm.stream("请用 50 字介绍一下 LangChain 框架"):
        print(chunk.content, end="", flush=True)
    print()  # 换行


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        print("   复制 config/.env.example 为 .env，然后填入你的 API Key")
        print_config_status()
        return

    print_config_status()

    try:
        simple_chat()
        multi_turn_chat()
        stream_chat()
    except Exception as e:
        print(f"\n❌ 调用出错: {e}")
        print("   请检查 API Key、网络连接和模型配置")

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 修改 SystemMessage，让 AI 扮演一个英语老师")
    print("2. 尝试调整 temperature（0.1 vs 0.9），看回答有什么不同")
    print("3. 实现一个简单的命令行对话循环，可以持续对话")
    print("=" * 60)


if __name__ == "__main__":
    main()
