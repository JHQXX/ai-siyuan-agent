"""
02 - ReAct 智能体

Java/SpringAI 对比：
- SpringAI: AiServices 或 ChatClient + ToolCallback
- LangChain: create_react_agent + AgentExecutor
- ReAct = Reasoning + Acting（推理 + 行动）

ReAct 模式：
1. Thought（思考）：我需要解决这个问题
2. Action（行动）：调用工具获取信息
3. Observation（观察）：工具返回结果
4. 重复 1-3，直到得出答案
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor


def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=0.3,  # Agent 用低 temperature 更稳定
    )


# ---------- 定义工具 ----------
@tool
def calculator(expression: str) -> str:
    """
    一个简单的计算器，可以计算数学表达式。
    支持加减乘除和括号，例如：(2 + 3) * 4

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果
    """
    try:
        # 安全计算（实际项目中不要直接用 eval！）
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"


@tool
def get_current_time() -> str:
    """获取当前日期和时间。"""
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")


@tool
def get_weather(city: str) -> str:
    """
    查询指定城市的天气信息（模拟数据）。

    Args:
        city: 城市名称

    Returns:
        天气信息
    """
    weather_data = {
        "北京": "晴，25°C，微风",
        "上海": "多云，28°C，东南风",
        "广州": "雷阵雨，30°C，南风",
        "深圳": "晴转多云，29°C，东风",
        "杭州": "小雨，24°C，西北风",
    }
    return weather_data.get(city, f"{city}的天气信息暂时无法查询")


def simple_react_agent():
    """简单的 ReAct 智能体"""
    print("=" * 60)
    print("1. 简单 ReAct 智能体 - 数学计算")
    print("=" * 60)

    llm = get_llm()
    tools = [calculator, get_current_time, get_weather]

    # 构建 ReAct 提示词模板
    prompt = ChatPromptTemplate.from_template("""
回答以下问题。你可以使用以下工具：

{tools}

使用以下格式：

Question: 输入的问题
Thought: 你应该思考接下来要做什么
Action: 要执行的工具名称，必须是 [{tool_names}] 中的一个
Action Input: 工具的输入参数
Observation: 工具执行的结果
... (这个 Thought/Action/Action Input/Observation 可以重复多次)
Thought: 我现在知道最终答案了
Final Answer: 最终的答案

现在开始！

Question: {input}
Thought:{agent_scratchpad}
""")

    # 创建 ReAct Agent
    agent = create_react_agent(llm, tools, prompt)

    # 创建 AgentExecutor（执行器）
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # 打印详细过程（可以看到 Thought/Action/Observation）
        handle_parsing_errors=True,  # 处理解析错误
        max_iterations=10,  # 最大迭代次数，防止无限循环
    )

    # 运行智能体
    result = agent_executor.invoke({
        "input": "计算 (128 + 256) * 3 的结果是多少？"
    })

    print(f"\n最终答案: {result['output']}")


def multi_tool_agent():
    """多工具智能体 - 组合使用多个工具"""
    print("\n" + "=" * 60)
    print("2. 多工具智能体 - 综合问答")
    print("=" * 60)

    llm = get_llm()
    tools = [calculator, get_current_time, get_weather]

    prompt = ChatPromptTemplate.from_template("""
你是一个智能助手，尽可能准确地回答用户的问题。

你可以使用以下工具：
{tools}

使用格式：
Thought: <思考过程>
Action: <工具名，从 [{tool_names}] 中选择>
Action Input: <工具输入>
Observation: <工具结果>
...（可重复）
Thought: 我有最终答案了
Final Answer: <最终答案>

用户问题：{input}
{agent_scratchpad}
""")

    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )

    # 测试：需要用到多个工具的问题
    result = agent_executor.invoke({
        "input": "现在几点了？北京今天天气怎么样？如果温度是25度，那么华氏度是多少？"
    })

    print(f"\n最终答案:\n{result['output']}")


def chat_agent():
    """带对话历史的智能体"""
    print("\n" + "=" * 60)
    print("3. 带对话历史的智能体")
    print("=" * 60)

    from langchain_core.prompts import MessagesPlaceholder
    from langchain_core.messages import HumanMessage, AIMessage

    llm = get_llm()
    tools = [calculator, get_current_time, get_weather]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有用的智能助手。回答问题时要简洁准确。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("human", "{agent_scratchpad}"),
    ])

    # 注意：使用 chat_history 时，提示词模板需要调整
    # 这里我们用简化的方式演示多轮对话

    agent = create_react_agent(llm, tools, ChatPromptTemplate.from_template("""
你是一个智能助手。

可用工具: {tools}
工具名称: {tool_names}

之前的对话:
{chat_history}

当前问题: {input}

{agent_scratchpad}
"""))

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    # 第一轮
    result1 = agent_executor.invoke({
        "input": "你好，我叫小明",
        "chat_history": ""
    })
    print(f"\n第一轮 - AI: {result1['output']}")

    # 第二轮（有历史）
    history = f"Human: 你好，我叫小明\nAI: {result1['output']}"
    result2 = agent_executor.invoke({
        "input": "我叫什么名字？再告诉我现在几点",
        "chat_history": history
    })
    print(f"\n第二轮 - AI: {result2['output']}")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    try:
        simple_react_agent()
        multi_tool_agent()
        chat_agent()
    except Exception as e:
        print(f"\n❌ 调用出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 添加一个新工具：字符串反转，让智能体用它来处理问题")
    print("2. 提出一个需要调用 3 次以上工具的问题，观察智能体的思考过程")
    print("3. 思考：ReAct 模式和直接让 LLM 回答相比，优势是什么？")
    print("=" * 60)


if __name__ == "__main__":
    main()
