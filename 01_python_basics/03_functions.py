"""
03 - 函数与模块

Java 开发者注意：
- Python 的函数用 def 关键字定义
- 函数可以返回多个值（Java 做不到！）
- 有默认参数、关键字参数等灵活特性
- 模块就是 .py 文件，用 import 导入
"""

from typing import List, Tuple


# ---------- 基础函数 ----------
def add(a: int, b: int) -> int:
    """
    两数相加

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两数之和
    """
    return a + b


# ---------- 默认参数 ----------
def greet(name: str, greeting: str = "你好") -> str:
    """
    打招呼 - 带默认参数

    类似 Java 的方法重载，但更简洁
    """
    return f"{greeting}，{name}！"


# ---------- 返回多个值 ----------
def calculate(a: int, b: int) -> Tuple[int, int, float]:
    """
    计算和、差、商 - 返回多个值！

    Java 需要封装成对象，Python 直接返回元组
    """
    sum_val = a + b
    diff = a - b
    quotient = a / b if b != 0 else 0.0
    return sum_val, diff, quotient


# ---------- 可变参数 ----------
def sum_all(*numbers: int) -> int:
    """
    求和 - 可变参数

    类似 Java 的 int... numbers
    """
    total = 0
    for num in numbers:
        total += num
    return total


# ---------- 函数作为参数 ----------
def apply_operation(numbers: List[int], operation) -> List[int]:
    """
    对列表中每个元素应用操作

    类似 Java 的 Function 接口
    """
    return [operation(n) for n in numbers]  # 列表推导式，类似 stream().map().collect()


def double(x: int) -> int:
    return x * 2


# ---------- lambda 表达式 ----------
# 类似 Java 的 lambda，但功能更简单（只能一行）
square = lambda x: x * x


# ---------- 主程序 ----------
def main():
    print("=" * 50)
    print("一、基础函数")
    print("=" * 50)
    result = add(3, 5)
    print(f"add(3, 5) = {result}")

    print("\n" + "=" * 50)
    print("二、默认参数")
    print("=" * 50)
    print(greet("小明"))  # 使用默认 greeting
    print(greet("小明", "早上好"))  # 自定义 greeting
    print(greet(name="小红", greeting="晚上好"))  # 关键字参数（顺序可乱）

    print("\n" + "=" * 50)
    print("三、返回多个值（Python 特色！）")
    print("=" * 50)
    s, d, q = calculate(10, 3)  # 解包
    print(f"calculate(10, 3):")
    print(f"  和 = {s}")
    print(f"  差 = {d}")
    print(f"  商 = {q}")

    print("\n" + "=" * 50)
    print("四、可变参数")
    print("=" * 50)
    print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
    print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")

    print("\n" + "=" * 50)
    print("五、函数作为参数 + 列表推导式")
    print("=" * 50)
    nums = [1, 2, 3, 4, 5]
    doubled = apply_operation(nums, double)
    print(f"原列表: {nums}")
    print(f"每个数乘2: {doubled}")

    # 用 lambda 更简洁
    tripled = apply_operation(nums, lambda x: x * 3)
    print(f"每个数乘3: {tripled}")

    # 列表推导式（类似 Java Stream）
    evens = [n for n in nums if n % 2 == 0]
    print(f"偶数: {evens}")

    print("\n" + "=" * 50)
    print("练习：")
    print("1. 写一个函数，判断一个数是不是质数")
    print("2. 写一个函数，接收字符串列表，返回长度最长的字符串")
    print("3. 用列表推导式找出 1-100 中所有能被 7 整除的数")
    print("=" * 50)


if __name__ == "__main__":
    main()
