"""
01 - 简单工具定义

Java/SpringAI 对比：
- SpringAI: @Tool 注解 + ToolCallback 接口
- LangChain: @tool 装饰器
- 工具的 docstring 很重要！LLM 靠这个理解工具用途
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from typing import List, Dict


# ---------- 工具定义 ----------
@tool
def add_numbers(a: int, b: int) -> int:
    """
    计算两个整数的和。

    Args:
        a: 第一个整数
        b: 第二个整数

    Returns:
        两个数的和
    """
    return a + b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """
    计算两个数的乘积。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两个数的乘积
    """
    return a * b


@tool
def get_word_length(word: str) -> int:
    """
    计算一个单词的长度。

    Args:
        word: 要计算长度的单词

    Returns:
        单词的字符数
    """
    return len(word)


@tool
def get_current_time() -> str:
    """
    获取当前时间。

    Returns:
        当前时间的字符串表示
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def sort_numbers(numbers: List[int], ascending: bool = True) -> List[int]:
    """
    对数字列表进行排序。

    Args:
        numbers: 要排序的数字列表
        ascending: 是否升序排列，默认为 True

    Returns:
        排序后的数字列表
    """
    return sorted(numbers, reverse=not ascending)


def tool_basics():
    """工具基础使用"""
    print("=" * 60)
    print("1. 工具基础 - 查看工具信息")
    print("=" * 60)

    tools = [add_numbers, multiply_numbers, get_word_length, get_current_time, sort_numbers]

    print(f"共有 {len(tools)} 个工具：\n")
    for tool_obj in tools:
        print(f"🔧 工具名: {tool_obj.name}")
        print(f"   描述: {tool_obj.description[:80]}...")
        print(f"   参数: {tool_obj.args}")
        print()


def call_tool_directly():
    """直接调用工具（不经过 LLM）"""
    print("=" * 60)
    print("2. 直接调用工具")
    print("=" * 60)

    # 直接调用，就像普通函数一样
    result = add_numbers.invoke({"a": 10, "b": 20})
    print(f"add_numbers(10, 20) = {result}")

    result = multiply_numbers.invoke({"a": 3.5, "b": 2})
    print(f"multiply_numbers(3.5, 2) = {result}")

    result = get_word_length.invoke({"word": "Hello, World!"})
    print(f"get_word_length('Hello, World!') = {result}")

    result = get_current_time.invoke({})
    print(f"get_current_time() = {result}")

    result = sort_numbers.invoke({"numbers": [5, 2, 8, 1, 9], "ascending": True})
    print(f"sort_numbers([5,2,8,1,9]) = {result}")


def tool_with_pydantic():
    """使用 Pydantic 定义工具参数（更清晰）"""
    print("\n" + "=" * 60)
    print("3. 使用 Pydantic 定义工具参数")
    print("=" * 60)

    from pydantic import BaseModel, Field

    class WeatherInput(BaseModel):
        """天气查询参数"""
        city: str = Field(description="城市名称，例如：北京、上海")
        unit: str = Field(default="celsius", description="温度单位：celsius 或 fahrenheit")

    @tool(args_schema=WeatherInput)
    def get_weather(city: str, unit: str = "celsius") -> str:
        """
        查询指定城市的天气信息（模拟数据）。

        Args:
            city: 城市名称
            unit: 温度单位

        Returns:
            天气信息字符串
        """
        temp_c = 25
        temp = temp_c if unit == "celsius" else temp_c * 9 / 5 + 32
        unit_str = "°C" if unit == "celsius" else "°F"
        return f"{city}今天晴，温度 {temp}{unit_str}，湿度 45%，微风"

    print(f"工具名: {get_weather.name}")
    print(f"参数 schema: {get_weather.args}")
    print()

    result = get_weather.invoke({"city": "北京", "unit": "celsius"})
    print(f"查询北京天气: {result}")

    result = get_weather.invoke({"city": "New York", "unit": "fahrenheit"})
    print(f"查询纽约天气: {result}")


def main():
    tool_basics()
    call_tool_directly()
    tool_with_pydantic()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 定义一个工具：计算圆的面积（参数：半径）")
    print("2. 定义一个工具：将字符串反转（参数：原字符串）")
    print("3. 思考：为什么工具需要详细的 docstring？")
    print("=" * 60)


if __name__ == "__main__":
    main()
