"""
02 - 数据类型与集合

Java 开发者注意：
- Python 是动态类型，变量不需要声明类型（但可以加类型提示）
- 常见类型：int, float, str, bool, list, dict, tuple, set
- list 类似 Java 的 ArrayList
- dict 类似 Java 的 HashMap
- 没有基本类型和包装类的区别
"""

from typing import List, Dict, Tuple, Set


def basic_types():
    """基本数据类型"""
    print("=" * 50)
    print("一、基本数据类型")
    print("=" * 50)

    # 整数 - 类似 Java 的 int/long
    age: int = 25
    print(f"整数: {age}, 类型: {type(age)}")

    # 浮点数 - 类似 Java 的 double
    price: float = 99.99
    print(f"浮点数: {price}, 类型: {type(price)}")

    # 字符串 - 类似 Java 的 String
    name: str = "Python"
    print(f"字符串: {name}, 类型: {type(name)}")

    # 布尔值 - 注意是 True/False，不是 true/false
    is_active: bool = True
    print(f"布尔值: {is_active}, 类型: {type(is_bool())}")

    # 空值 - 类似 Java 的 null
    result = None
    print(f"空值: {result}, 类型: {type(result)}")


def is_bool() -> bool:
    return True


def list_demo():
    """列表 List - 类似 Java 的 ArrayList"""
    print("\n" + "=" * 50)
    print("二、列表 List（类似 Java ArrayList）")
    print("=" * 50)

    # 创建列表
    fruits: List[str] = ["苹果", "香蕉", "橙子"]
    print(f"原始列表: {fruits}")

    # 获取元素 - 下标从 0 开始，和 Java 一样
    print(f"第一个元素: {fruits[0]}")
    print(f"最后一个元素: {fruits[-1]}")  # Python 特色：负数索引表示从后往前

    # 添加元素 - 类似 Java 的 add()
    fruits.append("葡萄")
    print(f"添加后: {fruits}")

    # 删除元素
    fruits.remove("香蕉")
    print(f"删除后: {fruits}")

    # 列表长度 - 类似 Java 的 size()
    print(f"列表长度: {len(fruits)}")

    # 切片操作（Python 特色！）
    print(f"前两个元素: {fruits[0:2]}")  # 类似 subList，但更灵活


def dict_demo():
    """字典 Dict - 类似 Java 的 HashMap"""
    print("\n" + "=" * 50)
    print("三、字典 Dict（类似 Java HashMap）")
    print("=" * 50)

    # 创建字典
    student: Dict[str, object] = {
        "name": "张三",
        "age": 20,
        "major": "计算机科学"
    }
    print(f"原始字典: {student}")

    # 获取值 - 类似 Java 的 get()
    print(f"姓名: {student['name']}")
    print(f"年龄: {student.get('age')}")

    # 添加/修改键值对 - 类似 Java 的 put()
    student["grade"] = "三年级"
    print(f"添加后: {student}")

    # 遍历字典
    print("\n遍历所有键值对:")
    for key, value in student.items():
        print(f"  {key}: {value}")


def tuple_demo():
    """元组 Tuple - 不可变的列表"""
    print("\n" + "=" * 50)
    print("四、元组 Tuple（不可变列表）")
    print("=" * 50)

    point: Tuple[int, int] = (10, 20)
    print(f"坐标: {point}")
    print(f"x = {point[0]}, y = {point[1]}")

    # 元组解包（Python 特色！）
    x, y = point
    print(f"解包后: x={x}, y={y}")


def set_demo():
    """集合 Set - 类似 Java 的 HashSet"""
    print("\n" + "=" * 50)
    print("五、集合 Set（类似 Java HashSet）")
    print("=" * 50)

    numbers: Set[int] = {1, 2, 3, 2, 1}  # 自动去重
    print(f"集合（自动去重）: {numbers}")

    numbers.add(4)
    print(f"添加后: {numbers}")


if __name__ == "__main__":
    basic_types()
    list_demo()
    dict_demo()
    tuple_demo()
    set_demo()

    print("\n" + "=" * 50)
    print("练习：")
    print("1. 创建一个包含你喜欢的 3 本书的列表")
    print("2. 创建一个你的个人信息字典（姓名、年龄、爱好）")
    print("3. 试试列表的切片操作 fruits[1:] 是什么结果？")
    print("=" * 50)
