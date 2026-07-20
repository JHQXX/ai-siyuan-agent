"""
03 - 输出解析器 (Output Parser)

Java/SpringAI 对比：
- SpringAI: BeanOutputParser / MapOutputParser
- LangChain: PydanticOutputParser / StrOutputParser 等
- 用于将 LLM 的字符串输出解析成结构化数据
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import is_config_ready, get_settings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    PydanticOutputParser
)
from pydantic import BaseModel, Field
from typing import List


def get_llm():
    settings = get_settings()
    return ChatOpenAI(
        model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL,
        temperature=0.3,  # 结构化输出用低 temperature 更稳定
    )


def str_output_parser():
    """字符串输出解析器 - 最基础的，直接拿文本"""
    print("=" * 60)
    print("1. StrOutputParser - 字符串解析")
    print("=" * 60)

    prompt = ChatPromptTemplate.from_template("用一句话解释{concept}")
    llm = get_llm()
    parser = StrOutputParser()

    # 管道：Prompt → LLM → Parser
    chain = prompt | llm | parser

    result = chain.invoke({"concept": "人工智能"})
    print(f"解析结果类型: {type(result)}")
    print(f"解析结果内容: {result}")


def json_output_parser():
    """JSON 输出解析器 - 解析成字典"""
    print("\n" + "=" * 60)
    print("2. JsonOutputParser - JSON 解析")
    print("=" * 60)

    prompt = ChatPromptTemplate.from_template("""
请用 JSON 格式回答，包含以下字段：
- name: 城市名
- country: 所属国家
- population: 人口（百万）
- famous_for: 著名景点（数组）

城市：{city}
""")

    llm = get_llm()
    parser = JsonOutputParser()

    chain = prompt | llm | parser

    result = chain.invoke({"city": "北京"})
    print(f"解析结果类型: {type(result)}")
    print(f"城市名: {result.get('name')}")
    print(f"国家: {result.get('country')}")
    print(f"人口: {result.get('population')}M")
    print(f"著名景点: {result.get('famous_for')}")


# ---------- Pydantic 模型（类似 Java 的 DTO / Bean）----------
class BookInfo(BaseModel):
    """书籍信息 - 类似 Java 的 POJO / DTO"""
    title: str = Field(description="书名")
    author: str = Field(description="作者")
    year: int = Field(description="出版年份")
    genre: str = Field(description="类型")
    rating: float = Field(description="评分（1-10）")


def pydantic_output_parser():
    """Pydantic 输出解析器 - 解析成强类型对象"""
    print("\n" + "=" * 60)
    print("3. PydanticOutputParser - 强类型对象")
    print("   （类似 Java 的 BeanOutputParser）")
    print("=" * 60)

    # 创建解析器，传入 Pydantic 模型
    parser = PydanticOutputParser(pydantic_object=BookInfo)

    # 解析器会自动生成格式说明
    format_instructions = parser.get_format_instructions()
    print(f"格式说明:\n{format_instructions[:200]}...")
    print()

    prompt = ChatPromptTemplate.from_template("""
请推荐一本{genre}领域的经典书籍。

{format_instructions}
""")

    llm = get_llm()
    chain = prompt | llm | parser

    result: BookInfo = chain.invoke({
        "genre": "科幻小说",
        "format_instructions": format_instructions
    })

    print(f"解析结果类型: {type(result)}")
    print(f"书名: {result.title}")
    print(f"作者: {result.author}")
    print(f"出版年份: {result.year}")
    print(f"类型: {result.genre}")
    print(f"评分: {result.rating}/10")

    # 可以像普通对象一样使用
    if result.rating >= 9:
        print("\n✅ 这是一本高分好书！")


# ---------- 更复杂的模型 ----------
class StudyPlan(BaseModel):
    """学习计划"""
    topic: str = Field(description="学习主题")
    duration_days: int = Field(description="学习天数")
    daily_hours: float = Field(description="每天学习小时数")
    milestones: List[str] = Field(description="里程碑列表")


def complex_pydantic_parser():
    """复杂结构解析"""
    print("\n" + "=" * 60)
    print("4. 复杂结构解析（嵌套 + 列表）")
    print("=" * 60)

    parser = PydanticOutputParser(pydantic_object=StudyPlan)
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template("""
请为我制定一个{topic}的学习计划。

{format_instructions}
""")

    llm = get_llm()
    chain = prompt | llm | parser

    result: StudyPlan = chain.invoke({
        "topic": "Python 智能体开发",
        "format_instructions": format_instructions
    })

    print(f"主题: {result.topic}")
    print(f"总天数: {result.duration_days} 天")
    print(f"每天学习: {result.daily_hours} 小时")
    print(f"里程碑:")
    for i, milestone in enumerate(result.milestones, 1):
        print(f"  {i}. {milestone}")


def main():
    if not is_config_ready():
        print("❌ 请先配置 API Key！")
        return

    try:
        str_output_parser()
        json_output_parser()
        pydantic_output_parser()
        complex_pydantic_parser()
    except Exception as e:
        print(f"\n❌ 调用出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("练习：")
    print("1. 定义一个 Movie Pydantic 模型，包含电影名、导演、演员列表、评分")
    print("2. 用 PydanticOutputParser 解析一部电影的信息")
    print("3. 思考：为什么需要输出解析器？直接让 LLM 输出 JSON 不行吗？")
    print("=" * 60)


if __name__ == "__main__":
    main()
