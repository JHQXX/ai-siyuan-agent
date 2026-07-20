"""
01 - Hello Python!
第一个 Python 程序

Java 开发者注意：
- Python 不需要 main 方法，直接写代码就会执行
- 没有分号，换行就是语句结束
- 使用缩进而非大括号表示代码块
- print() 是内置函数，不是 System.out.println()
"""


def main():
    """主函数 - Python 也可以有 main，但不是必须的"""
    # 类似 Java 的 System.out.println("Hello, World!");
    print("Hello, Python!")
    print("欢迎来到 AI 智能体的世界！")

    # 字符串格式化（类似 Java 的 String.format）
    name = "学习者"
    age = 25
    print(f"我是 {name}，今年 {age} 岁")  # f-string，最常用

    # 试试修改上面的内容，运行看看效果！


# 这是 Python 的惯用写法：只有直接运行本文件时才执行 main()
# 类似 Java 的 public static void main(String[] args)
if __name__ == "__main__":
    main()
