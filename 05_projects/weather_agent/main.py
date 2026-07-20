"""
综合项目：天气查询智能体
========================

这是一个综合运用前面所学知识的实战项目：
- 使用 @tool 定义工具
- 使用 ReAct 模式构建智能体
- 支持多轮对话
- 支持天气查询、日期时间、简单计算等功能

对应 Java/SpringAI：类似 AiServices + ToolCallback 的组合
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.settings import is_config_ready, get_settings
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from typing import Optional
from datetime import datetime, timedelta
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
def get_current_weather(city: str) -> str:
    """
    查询指定城市的实时天气信息。
    支持的城市包括：北京、上海、广州、深圳、杭州、成都、武汉、西安、南京、重庆。

    Args:
        city: 城市名称，必须是中文名

    Returns:
        天气详情，包括温度、天气状况、湿度、风力等
    """
    weather_db = {
        "北京": {"天气": "晴", "温度": 26, "湿度": 45, "风力": "微风", "空气质量": "优", "体感温度": 25},
        "上海": {"天气": "多云", "温度": 28, "湿度": 65, "风力": "东南风3级", "空气质量": "良", "体感温度": 30},
        "广州": {"天气": "雷阵雨", "温度": 32, "湿度": 80, "风力": "南风2级", "空气质量": "良", "体感温度": 36},
        "深圳": {"天气": "晴转多云", "温度": 30, "湿度": 70, "风力": "东风3级", "空气质量": "优", "体感温度": 33},
        "杭州": {"天气": "小雨", "温度": 24, "湿度": 75, "风力": "西北风2级", "空气质量": "优", "体感温度": 23},
        "成都": {"天气": "阴", "温度": 24, "湿度": 60, "风力": "微风", "空气质量": "良", "体感温度": 24},
        "武汉": {"天气": "晴", "温度": 29, "湿度": 55, "风力": "南风2级", "空气质量": "良", "体感温度": 31},
        "西安": {"天气": "多云", "温度": 27, "湿度": 50, "风力": "东北风2级", "空气质量": "良", "体感温度": 26},
        "南京": {"天气": "晴间多云", "温度": 28, "湿度": 58, "风力": "东风2级", "空气质量": "良", "体感温度": 29},
        "重庆": {"天气": "阴转小雨", "温度": 25, "湿度": 72, "风力": "微风", "空气质量": "良", "体感温度": 26},
    }

    if city in weather_db:
        w = weather_db[city]
        return (
            f"{city}实时天气：\n"
            f"  天气状况：{w['天气']}\n"
            f"  当前温度：{w['温度']}°C\n"
            f"  体感温度：{w['体感温度']}°C\n"
            f"  相对湿度：{w['湿度']}%\n"
            f"  风力风向：{w['风力']}\n"
            f"  空气质量：{w['空气质量']}"
        )
    else:
        supported = "、".join(weather_db.keys())
        return f"抱歉，暂时不支持查询 {city} 的天气。支持的城市：{supported}"


@tool
def get_weather_forecast(city: str, days: int = 3) -> str:
    """
    查询指定城市未来几天的天气预报。

    Args:
        city: 城市名称
        days: 预报天数，1-7天，默认为3天

    Returns:
        天气预报信息
    """
    days = min(max(days, 1), 7)  # 限制在 1-7 天

    weather_types = ["晴", "多云", "阴", "小雨", "雷阵雨"]
    wind_types = ["微风", "东风2级", "南风3级", "西北风2级", "东南风3级"]

    base_temp = {"北京": 26, "上海": 28, "广州": 32, "深圳": 30, "杭州": 24,
                 "成都": 24, "武汉": 29, "西安": 27, "南京": 28, "重庆": 25}

    base = base_temp.get(city, 25)
    result = [f"{city}未来{days}天天气预报："]

    today = datetime.now()
    for i in range(days):
        date = today + timedelta(days=i)
        date_str = date.strftime("%m月%d日")
        weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][date.weekday()]

        weather = random.choice(weather_types)
        high = base + random.randint(-2, 4)
        low = base - random.randint(3, 8)
        wind = random.choice(wind_types)

        result.append(
            f"  {date_str} {weekday}：{weather}，{low}°C ~ {high}°C，{wind}"
        )

    return "\n".join(result)


@tool
def get_current_datetime() -> str:
    """获取当前的日期和时间，以及星期几。"""
    now = datetime.now()
    weekday_map = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    weekday = weekday_map[now.weekday()]
    return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')} {weekday}"


@tool
def calculate_expression(expression: str) -> str:
    """
    数学计算器，可以计算加减乘除和括号的数学表达式。
    例如：(25 + 30) * 2 / 5

    Args:
        expression: 数学表达式字符串

    Returns:
        计算结果
    """
    try:
        allowed_chars = set("0123456789+-*/(). %.")
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含非法字符，只支持数字和加减乘除括号"
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def get_dressing_advice(city: str) -> str:
    """
    根据天气给出穿衣建议。

    Args:
        city: 城市名称

    Returns:
        穿衣建议
    """
    # 先获取天气
    weather_result = get_current_weather.invoke({"city": city})
    if "抱歉" in weather_result:
        return weather_result

    # 提取温度（简单解析）
    import re
    temp_match = re.search(r"当前温度：(\d+)°C", weather_result)
    if not temp_match:
        return "无法获取温度信息"

    temp = int(temp_match.group(1))

    if temp >= 30:
        advice = "天气炎热，建议穿短袖、短裤、凉鞋等清凉透气的衣物，注意防晒和补水。"
    elif temp >= 25:
        advice = "天气温暖，建议穿短袖T恤、薄长裤或裙子，舒适透气为主。"
    elif temp >= 20:
        advice = "温度适宜，建议穿长袖衬衫、薄外套或卫衣，搭配长裤。"
    elif temp >= 15:
        advice = "天气微凉，建议穿风衣、薄毛衣或外套，注意早晚温差。"
    elif temp >= 10:
        advice = "天气较冷，建议穿厚外套、毛衣、长裤，注意保暖。"
    else:
        advice = "天气寒冷，建议穿羽绒服、厚毛衣、保暖裤，注意防寒保暖。"

    return f"[{city}] 穿衣建议：{advice}"


@tool
def convert_temperature(temp: float, from_unit: str, to_unit: str) -> str:
    """
    温度单位转换，支持摄氏度(°C)和华氏度(°F)互相转换。

    Args:
        temp: 温度数值
        from_unit: 原单位，'celsius' 或 'fahrenheit'
        to_unit: 目标单位，'celsius' 或 'fahrenheit'

    Returns:
        转换结果
    """
    if from_unit == to_unit:
        return f"转换结果：{temp}°"

    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = temp * 9 / 5 + 32
        return f"转换结果：{temp}°C = {result:.1f}°F"
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (temp - 32) * 5 / 9
        return f"转换结果：{temp}°F = {result:.1f}°C"
    else:
        return f"不支持的单位：{from_unit} → {to_unit}，请使用 celsius 或 fahrenheit"


# ========== 智能体构建 ==========

def build_weather_agent(verbose: bool = True) -> AgentExecutor:
    """构建天气查询智能体"""
    llm = get_llm()

    tools = [
        get_current_weather,
        get_weather_forecast,
        get_current_datetime,
        calculate_expression,
        get_dressing_advice,
        convert_temperature,
    ]

    prompt = ChatPromptTemplate.from_template("""
你是一个专业的天气助手小蓝，擅长回答各种天气相关的问题。

你的能力：
1. 查询实时天气
2. 查询未来天气预报
3. 提供穿衣建议
4. 温度单位转换
5. 数学计算
6. 回答当前时间

回答规则：
- 用亲切友好的语气回答
- 天气信息要准确清晰
- 如果是不支持的城市，如实告知并列出支持的城市
- 可以组合使用多个工具来回答复杂问题
- 不确定的事情不要猜测，直接告诉用户

可用工具：
{tools}

工具名称：{tool_names}

使用格式：
Thought: <思考过程>
Action: <工具名称>
Action Input: <工具参数>
Observation: <工具返回结果>
...（可重复）
Thought: 我现在知道最终答案了
Final Answer: <最终答案>

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


# ========== 运行模式 ==========

def run_demo():
    """演示模式：预设问题"""
    agent = build_weather_agent(verbose=True)

    test_questions = [
        "北京今天天气怎么样？",
        "上海未来5天的天气预报",
        "广州今天适合穿什么衣服？",
        "今天北京温度 26 度，转换成华氏度是多少？",
        "现在几点了？",
        "如果北京昨天25度，今天26度，平均温度是多少？",
    ]

    print("=" * 60)
    print("🌤️  天气助手演示")
    print("=" * 60)

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"问题 {i}: {question}")
        print("=" * 60)
        try:
            result = agent.invoke({"input": question})
            print(f"\n✅ 回答：\n{result['output']}")
        except Exception as e:
            print(f"\n❌ 出错: {e}")


def run_interactive():
    """交互模式"""
    agent = build_weather_agent(verbose=False)

    print("=" * 60)
    print("🌤️  天气智能助手 - 交互模式")
    print("=" * 60)
    print("你可以问我：")
    print("  - 北京今天天气怎么样？")
    print("  - 上海未来3天天气预报")
    print("  - 广州穿什么衣服合适？")
    print("  - 25摄氏度等于多少华氏度？")
    print("输入 'quit' 退出\n")

    while True:
        try:
            user_input = input("你: ").strip()
            if user_input.lower() in ["quit", "exit", "退出", "bye", "再见"]:
                print("\n天气助手：再见！祝你有美好的一天！🌤️")
                break
            if not user_input:
                continue

            print("小蓝: 思考中...", end="\r")
            result = agent.invoke({"input": user_input})
            print(" " * 20, end="\r")  # 清掉思考中
            print(f"小蓝: {result['output']}\n")

        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"出错了: {e}\n")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        print("   复制 config/.env.example 为 .env，然后填入你的 API Key")
        return

    print("选择运行模式：")
    print("1. 演示模式（预设问题）")
    print("2. 交互模式（自己提问）")

    choice = input("请选择 (1/2，默认1): ").strip()

    if choice == "2":
        run_interactive()
    else:
        run_demo()


if __name__ == "__main__":
    main()
