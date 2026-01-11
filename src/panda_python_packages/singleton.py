"""
单例模式装饰器实现

提供线程安全的单例装饰器，可以用于类装饰，确保类只有一个实例。
"""
import threading
from functools import wraps
from typing import TypeVar, Type, Any

T = TypeVar('T')


def singleton(cls: Type[T]) -> Type[T]:
    """
    单例装饰器 - 确保类只有一个实例，线程安全
    
    使用示例:
    
    示例1: 基础用法
        >>> from panda_python_packages import singleton
        >>> 
        >>> @singleton
        >>> class DatabaseConnection:
        ...     def __init__(self, host="localhost", port=5432):
        ...         self.host = host
        ...         self.port = port
        ...         print(f"连接到数据库: {host}:{port}")
        ... 
        >>> # 第一次创建实例
        >>> db1 = DatabaseConnection("server1", 5432)
        连接到数据库: server1:5432
        >>> 
        >>> # 后续调用返回同一个实例，参数会被忽略
        >>> db2 = DatabaseConnection("server2", 3306)  # 不会打印，返回同一个实例
        >>> 
        >>> assert db1 is db2  # True
        >>> assert db1.host == "server1"  # 保持首次创建时的值
        >>> assert db1.port == 5432
    
    示例2: 配置类单例
        >>> @singleton
        >>> class AppConfig:
        ...     def __init__(self):
        ...         self.debug = True
        ...         self.timeout = 30
        ... 
        >>> config1 = AppConfig()
        >>> config2 = AppConfig()
        >>> config1.debug = False
        >>> assert config2.debug == False  # 修改一个实例，另一个也会变化
    
    示例3: 线程安全测试
        >>> import threading
        >>> 
        >>> @singleton
        >>> class Counter:
        ...     def __init__(self):
        ...         self.value = 0
        ... 
        >>> def create_instance():
        ...     return Counter()
        ... 
        >>> # 多线程同时创建实例
        >>> threads = [threading.Thread(target=create_instance) for _ in range(10)]
        >>> for t in threads:
        ...     t.start()
        >>> for t in threads:
        ...     t.join()
        >>> 
        >>> # 所有线程获取的都是同一个实例
        >>> instances = [create_instance() for _ in range(10)]
        >>> assert all(inst is instances[0] for inst in instances)  # True
    
    特性:
        - 线程安全（使用双重检查锁定模式）
        - 支持带参数的 __init__ 方法（但只有首次调用会使用参数）
        - 首次调用时创建实例，后续调用返回同一个实例
        - 自动处理类的 __new__ 方法
    
    Args:
        cls: 要装饰的类
    
    Returns:
        装饰后的类，确保只有一个实例
    
    Raises:
        无异常抛出
    """
    _instances: dict[Type[T], T] = {}
    _lock = threading.Lock()
    
    original_new = cls.__new__
    
    def __new__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in _instances:
            with _lock:
                # 双重检查锁定模式
                if cls not in _instances:
                    if original_new is object.__new__:
                        instance = object.__new__(cls)
                    else:
                        instance = original_new(cls, *args, **kwargs)
                    _instances[cls] = instance
        return _instances[cls]
    
    cls.__new__ = staticmethod(__new__)  # type: ignore
    return cls


def singleton_class(cls: Type[T]) -> Type[T]:
    """
    单例类装饰器（另一种实现方式，功能与 singleton 相同）
    
    使用示例:
    
    示例1: 基础用法（与 singleton 相同）
        >>> from panda_python_packages import singleton_class
        >>> 
        >>> @singleton_class
        >>> class Logger:
        ...     def __init__(self, level="INFO"):
        ...         self.level = level
        ...         self.logs = []
        ... 
        ...     def log(self, message):
        ...         self.logs.append(f"[{self.level}] {message}")
        ... 
        >>> logger1 = Logger("DEBUG")
        >>> logger2 = Logger("ERROR")  # 参数会被忽略
        >>> 
        >>> logger1.log("测试消息")
        >>> assert len(logger2.logs) == 1  # 两个实例实际上是同一个
        >>> assert logger1 is logger2  # True
    
    示例2: 缓存管理器
        >>> @singleton_class
        >>> class CacheManager:
        ...     def __init__(self):
        ...         self.cache = {}
        ... 
        ...     def get(self, key):
        ...         return self.cache.get(key)
        ... 
        ...     def set(self, key, value):
        ...         self.cache[key] = value
        ... 
        >>> cache1 = CacheManager()
        >>> cache2 = CacheManager()
        >>> 
        >>> cache1.set("user:1", "Alice")
        >>> assert cache2.get("user:1") == "Alice"  # 共享同一个缓存
    
    示例3: 服务类单例
        >>> @singleton_class
        >>> class EmailService:
        ...     def __init__(self, smtp_server="smtp.example.com"):
        ...         self.smtp_server = smtp_server
        ...         self.sent_count = 0
        ... 
        ...     def send(self, to, subject, body):
        ...         # 模拟发送邮件
        ...         self.sent_count += 1
        ...         return f"邮件已发送到 {to}"
        ... 
        >>> service1 = EmailService("smtp.gmail.com")
        >>> service2 = EmailService()  # 返回同一个实例
        >>> 
        >>> service1.send("user@example.com", "主题", "内容")
        >>> assert service2.sent_count == 1  # 共享计数
    
    注意: 
        - 这个装饰器与 singleton 功能完全相同，只是实现方式略有不同
        - 推荐使用 singleton，代码更简洁
        - 自动处理类的 __new__ 方法，无需手动实现
    
    Args:
        cls: 要装饰的类
    
    Returns:
        装饰后的类，确保只有一个实例
    
    Raises:
        无异常抛出
    """
    _instances: dict[Type[T], T] = {}
    _lock = threading.Lock()
    
    original_new = cls.__new__
    
    @wraps(original_new)
    def __new__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in _instances:
            with _lock:
                if cls not in _instances:
                    if original_new is object.__new__:
                        instance = object.__new__(cls)
                    else:
                        instance = original_new(cls, *args, **kwargs)
                    _instances[cls] = instance
        return _instances[cls]
    
    cls.__new__ = staticmethod(__new__)  # type: ignore
    return cls
