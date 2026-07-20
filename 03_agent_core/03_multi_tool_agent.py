"""
03 - 多工具智能体实战

构建一个更完整的智能体，包含多种类型的工具：
- 计算工具
- 搜索工具（模拟）
- 翻译工具
- 天气工具
- 日期时间工具
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from typing import List, Dict
import random


def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=0.3,
    )


# ========== 工具定义 ==========

@tool
def calculator(expression: str) -> str:
    """
    数学计算器，支持加减乘除和括号运算。
    输入示例：(10 + 5) * 3 / 2

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果字符串
    """
    try:
        # 安全计算（仅允许基本运算符）
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含非法字符"
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


@tool
def get_current_datetime() -> str:
    """获取当前的日期和时间。"""
    from datetime import datetime
    now = datetime.now()
    weekday_map = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    weekday = weekday_map[now.weekday()]
    return f"当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekday}"


@tool
def get_weather(city: str) -> str:
    """
    查询中国主要城市的天气信息。

    Args:
        city: 城市名称，如北京、上海、广州、深圳、杭州等

    Returns:
        天气详情
    """
    weather_db = {
        "北京": {"天气": "晴", "温度": "25°C", "湿度": "45%", "风力": "微风", "空气质量": "优"},
        "上海": {"天气": "多云", "温度": "28°C", "湿度": "65%", "风力": "东南风3级", "空气质量": "良"},
        "广州": {"天气": "雷阵雨", "温度": "32°C", "湿度": "80%", "风力": "南风2级", "空气质量": "良"},
        "深圳": {"天气": "晴转多云", "温度": "30°C", "湿度": "70%", "风力": "东风3级", "空气质量": "优"},
        "杭州": {"天气": "小雨", "温度": "26°C", "湿度": "75%", "风力": "西北风2级", "空气质量": "优"},
        "成都": {"天气": "阴", "温度": "24°C", "湿度": "60%", "风力": "微风", "空气质量": "良"},
    }

    if city in weather_db:
        w = weather_db[city]
        return f"{city}天气:\n  天气状况: {w['天气']}\n  温度: {w['温度']}\n  湿度: {w['湿度']}\n  风力: {w['风力']}\n  空气质量: {w['空气质量']}"
    else:
        return f"抱歉，暂时没有 {city} 的天气数据。支持的城市：{', '.join(weather_db.keys())}"


@tool
def translate_text(text: str, target_lang: str) -> str:
    """
    将文本翻译成指定语言（模拟翻译）。

    Args:
        text: 要翻译的文本
        target_lang: 目标语言，如 英语、日语、法语、中文

    Returns:
        翻译结果
    """
    # 模拟翻译（实际项目中用真实翻译 API）
    translations = {
        "英语": {
            "你好": "Hello",
            "谢谢": "Thank you",
            "我爱编程": "I love programming",
        },
        "日语": {
            "你好": "こんにちは",
            "谢谢": "ありがとう",
            "我爱编程": "プログラミングが大好きです",
        },
        "法语": {
            "你好": "Bonjour",
            "谢谢": "Merci",
            "我爱编程": "J'adore la programmation",
        },
    }

    lang_trans = translations.get(target_lang, {})
    if text in lang_trans:
        return f"翻译结果: {lang_trans[text]}"
    else:
        return f"[模拟翻译] {text} → {target_lang}: 模拟翻译结果_{target_lang}"


@tool
def search_web(query: str) -> str:
    """
    搜索网络获取信息（模拟搜索引擎）。

    Args:
        query: 搜索关键词

    Returns:
        搜索结果摘要
    """
    # 模拟搜索结果
    mock_results = {
        "python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。以简洁的语法和强大的生态系统著称，广泛应用于 Web 开发、数据分析、人工智能等领域。",
        "langchain": "LangChain 是一个用于构建大语言模型应用的框架，提供了链、智能体、工具等核心组件，支持多种 LLM 提供商，是构建 AI 应用的主流框架之一。",
        "人工智能": "人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统，包括机器学习、深度学习、自然语言处理等技术。",
    }

    # 对查询做简单匹配
    for keyword, result in mock_results.items():
        if keyword in query.lower():
            return f"搜索结果:\n{result}"

    return f"搜索 '{query}' 的结果（模拟）：未找到精确匹配，这是一个通用搜索结果摘要。建议尝试更具体的关键词。"


@tool
def get_holiday_info(year: int, month: int = 0) -> str:
    """
    查询指定年份的节假日信息。

    Args:
        year: 年份，如 2024
        month: 月份（1-12），0 表示全年

    Returns:
        节假日信息
    """
    holidays = {
        1: ["元旦：1月1日"],
        2: ["春节：2月10日-17日（农历正月初一至初八）"],
        4: ["清明节：4月4日-6日"],
        5: ["劳动节：5月1日-5日"],
        6: ["端午节：6月10日"],
        9: ["中秋节：9月17日"],
        10: ["国庆节：10月1日-7日"],
    }

    if month == 0:
        all_holidays = []
        for m in sorted(holidays.keys()):
            all_holidays.extend(holidays[m])
        return f"{year}年节假日:\n" + "\n".join(f"  - {h}" for h in all_holidays)
    elif month in holidays:
        return f"{year}年{month}月节假日:\n" + "\n".join(f"  - {h}" for h in holidays[month])
    else:
        return f"{year}年{month}月没有法定节假日"


# ========== 智能体构建 ==========

def build_agent(verbose: bool = True) -> AgentExecutor:
    """构建多工具智能体"""
    llm = get_llm()

    tools = [
        calculator,
        get_current_datetime,
        get_weather,
        translate_text,
        search_web,
        get_holiday_info,
    ]

    prompt = ChatPromptTemplate.from_template("""
你是一个功能强大的智能助手，可以使用多种工具来回答用户的问题。

可用工具列表：
{tools}

工具名称列表：{tool_names}

回答规则：
1. 先思考是否需要使用工具
2. 如果需要，选择最合适的工具并提供正确的参数
3. 可以多次使用工具，也可以组合使用多个工具
4. 如果工具无法解决问题，直接回答或询问用户更多信息
5. 最终答案要清晰、完整

使用格式：
Thought: <你的思考>
Action: <工具名称>
Action Input: <工具输入，JSON 格式>
Observation: <工具返回结果>
...（可以重复多次）
Thought: 我现在知道最终答案了
Final Answer: <最终的完整答案>

现在开始！

用户问题：{input}
{agent_scratchpad}
""")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=15,
    )

    return agent_executor


def test_scenarios():
    """测试各种场景"""
    agent = build_agent(verbose=True)

    test_cases = [
        "现在几点了？今天是周几？",
        "北京今天天气怎么样？温度是多少华氏度？",
        "把'我爱编程'翻译成日语和法语",
        "计算 123 * 456 + 789 的结果",
        "2024年10月有什么节假日？",
        "什么是 LangChain？",
    ]

    for i, question in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试 {i}: {question}")
        print("=" * 60)
        try:
            result = agent.invoke({"input": question})
            print(f"\n✅ 最终答案:\n{result['output']}")
        except Exception as e:
            print(f"\n❌ 出错: {e}")


def interactive_mode():
    """交互模式 - 可以持续对话"""
    print("\n" + "=" * 60)
    print("🤖 智能助手交互模式")
    print("输入 'quit' 或 'exit' 退出")
    print("=" * 60)

    agent = build_agent(verbose=False)

    while True:
        try:
            user_input = input("\n你: ").strip()
            if user_input.lower() in ["quit", "exit", "退出"]:
                print("再见！")
                break
            if not user_input:
                continue

            print("AI 思考中...")
            result = agent.invoke({"input": user_input})
            print(f"\nAI: {result['output']}")

        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n出错了: {e}")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    print("选择运行模式：")
    print("1. 自动测试场景")
    print("2. 交互模式（自己提问）")

    choice = input("请选择 (1/2，默认1): ").strip()

    try:
        if choice == "2":
            interactive_mode()
        else:
            test_scenarios()
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 添加一个新工具：查询手机号码归属地（模拟数据）")
    print("2. 试着问一个需要组合使用 3 个以上工具的复杂问题")
    print("3. 观察智能体在什么情况下会选择不使用工具直接回答")
    print("=" * 60)


if __name__ == "__main__":
    main()
