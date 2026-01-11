"""
Panda Python Packages - 一个 Python 工具包集合

快速开始:

    # 导入单例装饰器
    from panda_python_packages import singleton
    
    # 使用装饰器
    @singleton
    class MyClass:
        def __init__(self):
            self.value = 0
    
    # 创建实例（多次调用返回同一个实例）
    instance1 = MyClass()
    instance2 = MyClass()
    assert instance1 is instance2  # True

更多示例请查看各模块的文档字符串。
"""

__version__ = "0.1.0"

# 导出常用功能，方便用户直接使用
from .singleton import singleton, singleton_class

__all__ = ["singleton", "singleton_class"]
