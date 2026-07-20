# 天气查询智能体 🌤️

这是一个综合实战项目，展示了如何使用 LangChain 构建一个功能完整的天气查询智能体。

## 功能特性

- 🌡️ 实时天气查询
- 📅 未来天气预报（1-7天）
- 👕 穿衣建议
- 🔄 温度单位转换（°C ↔ °F）
- 🧮 数学计算
- ⏰ 当前时间查询

## 运行方式

```bash
# 确保你在项目根目录，并且已经配置好 .env
python 05_projects/weather_agent/main.py
```

然后选择：
1. 演示模式 - 看预设问题的效果
2. 交互模式 - 自己和智能体对话

## 技术要点

这个项目综合运用了前面学到的知识：

| 知识点 | 对应模块 | 用途 |
|-------|---------|------|
| @tool 装饰器 | 03_agent_core/01_simple_tool.py | 定义天气工具 |
| ReAct Agent | 03_agent_core/02_react_agent.py | 智能体推理 |
| 多工具组合 | 03_agent_core/03_multi_tool_agent.py | 多工具协作 |
| 提示词工程 | 02_langchain_basics/02_prompt_template.py | Agent 系统提示 |

## 扩展练习

1. 接入真实的天气 API（如和风天气、心知天气）
2. 添加空气质量查询功能
3. 添加天气预警功能
4. 用 Streamlit 做一个 Web 界面
5. 支持语音输入输出
