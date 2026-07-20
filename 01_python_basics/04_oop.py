"""
04 - 面向对象编程 (OOP)

Java 开发者注意：
- Python 也支持类和继承
- 没有接口（interface），用抽象类或鸭子类型
- 构造函数是 __init__，不是类名
- 所有方法默认都是 public
- self 类似 Java 的 this，但必须显式写在参数里
"""

from typing import List


# ---------- 基础类 ----------
class Person:
    """人类 - 基类"""

    # 类变量（类似 Java 的 static 变量）
    species: str = "智人"

    def __init__(self, name: str, age: int):
        """
        构造函数 - 注意是 __init__，不是类名

        self 类似 Java 的 this，但必须写在第一个参数位置
        """
        # 实例变量（类似 Java 的成员变量）
        self.name = name
        self.age = age

    def introduce(self) -> str:
        """自我介绍 - 实例方法"""
        return f"我叫{self.name}，今年{self.age}岁"

    def celebrate_birthday(self):
        """过生日，年龄 +1"""
        self.age += 1
        print(f"生日快乐！{self.name}现在{self.age}岁了")

    # 类方法（类似 Java 的 static 方法，但更强大）
    @classmethod
    def get_species(cls) -> str:
        return cls.species

    # 静态方法（和 Java 的 static 方法一样）
    @staticmethod
    def is_adult(age: int) -> bool:
        return age >= 18


# ---------- 继承 ----------
class Student(Person):
    """学生类 - 继承自 Person"""

    def __init__(self, name: str, age: int, student_id: str, major: str):
        # 调用父类构造函数 - 类似 Java 的 super()
        super().__init__(name, age)
        self.student_id = student_id
        self.major = major
        self.courses: List[str] = []

    # 方法重写（Override）- 和 Java 一样
    def introduce(self) -> str:
        base_info = super().introduce()
        return f"{base_info}，是{self.major}专业的学生，学号{self.student_id}"

    def enroll_course(self, course: str):
        """选课"""
        self.courses.append(course)
        print(f"{self.name} 选修了 {course}")

    def get_courses(self) -> List[str]:
        return self.courses


# ---------- 多态 ----------
class Teacher(Person):
    """教师类"""

    def __init__(self, name: str, age: int, department: str):
        super().__init__(name, age)
        self.department = department

    def introduce(self) -> str:
        return f"我叫{self.name}，在{self.department}任教"


def introduce_person(person: Person):
    """
    多态示例 - 只要是 Person 的子类都可以传进来

    这就是鸭子类型："只要走起来像鸭子，叫起来像鸭子，那它就是鸭子"
    """
    print(person.introduce())


# ---------- 主程序 ----------
def main():
    print("=" * 50)
    print("一、基础类使用")
    print("=" * 50)

    person = Person("张三", 25)
    print(person.introduce())
    person.celebrate_birthday()

    # 类方法和静态方法
    print(f"\n物种: {Person.get_species()}")
    print(f"20岁是成年吗？ {Person.is_adult(20)}")
    print(f"15岁是成年吗？ {Person.is_adult(15)}")

    print("\n" + "=" * 50)
    print("二、继承")
    print("=" * 50)

    student = Student("李四", 20, "2024001", "计算机科学")
    print(student.introduce())
    student.enroll_course("人工智能导论")
    student.enroll_course("Python 编程")
    print(f"已选课程: {student.get_courses()}")

    print("\n" + "=" * 50)
    print("三、多态")
    print("=" * 50)

    people = [
        Person("王五", 30),
        Student("赵六", 19, "2024002", "数学"),
        Teacher("钱老师", 45, "计算机系")
    ]

    print("大家来自我介绍：")
    for p in people:
        introduce_person(p)

    print("\n" + "=" * 50)
    print("练习：")
    print("1. 创建一个 Animal 类，有 name 属性和 speak() 方法")
    print("2. 创建 Dog 和 Cat 类继承 Animal，重写 speak()")
    print("3. 创建一个动物园类 Zoo，可以添加动物并让所有动物叫")
    print("=" * 50)


if __name__ == "__main__":
    main()
