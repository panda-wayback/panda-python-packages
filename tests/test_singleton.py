"""
单例装饰器的单元测试
"""
import threading
import time
from panda_python_packages import singleton, singleton_class


class TestSingleton:
    """测试 singleton 装饰器"""
    
    def test_basic_singleton(self):
        """测试基本的单例功能"""
        @singleton
        class MyClass:
            def __init__(self):
                self.value = 0
        
        instance1 = MyClass()
        instance2 = MyClass()
        
        assert instance1 is instance2, "应该是同一个实例"
        assert instance1.value == instance2.value
    
    def test_singleton_with_args(self):
        """测试带参数的 __init__ 方法"""
        @singleton
        class DatabaseConnection:
            def __init__(self, host="localhost", port=5432):
                self.host = host
                self.port = port
                self.created = True
        
        # 第一次创建，参数会被使用
        db1 = DatabaseConnection("server1", 5432)
        assert db1.host == "server1"
        assert db1.port == 5432
        
        # 第二次创建，返回同一个实例，但 __init__ 会被再次调用
        db2 = DatabaseConnection("server2", 3306)
        assert db1 is db2  # 是同一个实例
        # 注意：__init__ 会被再次调用，所以值会被更新
        assert db2.host == "server2"
        assert db2.port == 3306
    
    def test_singleton_with_kwargs(self):
        """测试带关键字参数的 __init__ 方法"""
        @singleton
        class Config:
            def __init__(self, debug=True, timeout=30):
                self.debug = debug
                self.timeout = timeout
        
        config1 = Config(debug=False, timeout=60)
        config2 = Config(debug=True, timeout=20)  # __init__ 会被再次调用
        
        assert config1 is config2  # 是同一个实例
        # 注意：__init__ 会被再次调用，所以值会被更新
        assert config2.debug is True
        assert config2.timeout == 20
    
    def test_singleton_state_sharing(self):
        """测试单例实例的状态共享"""
        @singleton
        class Counter:
            def __init__(self):
                self.count = 0
            
            def increment(self):
                self.count += 1
        
        counter1 = Counter()
        counter2 = Counter()
        
        counter1.increment()
        assert counter2.count == 1, "状态应该共享"
        
        counter2.increment()
        assert counter1.count == 2, "状态应该共享"
    
    def test_multiple_singleton_classes(self):
        """测试多个不同的单例类"""
        @singleton
        class ClassA:
            def __init__(self):
                self.name = "A"
        
        @singleton
        class ClassB:
            def __init__(self):
                self.name = "B"
        
        a1 = ClassA()
        a2 = ClassA()
        b1 = ClassB()
        b2 = ClassB()
        
        assert a1 is a2
        assert b1 is b2
        assert a1 is not b1, "不同的类应该是不同的实例"
    
    def test_singleton_thread_safety(self):
        """测试线程安全性"""
        @singleton
        class ThreadSafeClass:
            def __init__(self):
                self.value = 0
                time.sleep(0.01)  # 模拟初始化耗时
        
        instances = []
        lock = threading.Lock()
        
        def create_instance():
            instance = ThreadSafeClass()
            with lock:
                instances.append(instance)
        
        # 创建多个线程同时实例化
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # 所有实例应该是同一个对象
        first_instance = instances[0]
        assert all(inst is first_instance for inst in instances), \
            "多线程环境下应该返回同一个实例"
    
    def test_singleton_inheritance(self):
        """测试继承的单例类"""
        @singleton
        class BaseClass:
            def __init__(self):
                self.base_value = "base"
        
        @singleton
        class DerivedClass(BaseClass):
            def __init__(self):
                super().__init__()
                self.derived_value = "derived"
        
        base1 = BaseClass()
        base2 = BaseClass()
        derived1 = DerivedClass()
        derived2 = DerivedClass()
        
        assert base1 is base2
        assert derived1 is derived2
        assert base1 is not derived1, "基类和派生类应该是不同的实例"
    
    def test_singleton_with_custom_new(self):
        """测试自定义 __new__ 方法的类（覆盖 else 分支）"""
        @singleton
        class CustomNewClass:
            def __new__(cls, *args, **kwargs):
                # 自定义 __new__ 方法
                instance = super().__new__(cls)
                instance.created_by = "custom_new"
                return instance
            
            def __init__(self, value=0):
                self.value = value
        
        instance1 = CustomNewClass(10)
        instance2 = CustomNewClass(20)
        
        assert instance1 is instance2, "应该是同一个实例"
        assert instance1.created_by == "custom_new", "应该使用自定义的 __new__"
        # __init__ 会被再次调用，所以 value 会被更新
        assert instance2.value == 20
    
    def test_singleton_with_custom_new_and_args(self):
        """测试自定义 __new__ 方法且带参数的类"""
        @singleton
        class CustomNewWithArgs:
            def __new__(cls, name, age):
                # 自定义 __new__ 方法，处理参数
                instance = super().__new__(cls)
                instance._name = name
                instance._age = age
                return instance
            
            def __init__(self, name, age):
                # __init__ 仍然会被调用
                pass
            
            @property
            def info(self):
                return f"{self._name}:{self._age}"
        
        obj1 = CustomNewWithArgs("Alice", 25)
        obj2 = CustomNewWithArgs("Bob", 30)  # 参数会被忽略，返回同一个实例
        
        assert obj1 is obj2
        # 由于 __new__ 在第一次调用时执行，所以保持第一次的值
        assert obj1.info == "Alice:25"
        assert obj2.info == "Alice:25"


class TestSingletonClass:
    """测试 singleton_class 装饰器"""
    
    def test_basic_singleton_class(self):
        """测试基本的单例功能"""
        @singleton_class
        class MyClass:
            def __init__(self):
                self.value = 0
        
        instance1 = MyClass()
        instance2 = MyClass()
        
        assert instance1 is instance2, "应该是同一个实例"
    
    def test_singleton_class_with_args(self):
        """测试带参数的 __init__ 方法"""
        @singleton_class
        class Logger:
            def __init__(self, level="INFO"):
                self.level = level
                # 注意：__init__ 会被多次调用，所以需要检查是否已初始化
                if not hasattr(self, 'logs'):
                    self.logs = []
            
            def log(self, message):
                self.logs.append(f"[{self.level}] {message}")
        
        logger1 = Logger("DEBUG")
        logger1.log("测试消息1")
        logger2 = Logger("ERROR")  # __init__ 会被再次调用，但返回同一个实例
        
        assert logger1 is logger2  # 是同一个实例
        # level 会被更新为最新调用的值
        assert logger2.level == "ERROR"
        # logs 通过 hasattr 检查避免重置，所以保留
        assert len(logger2.logs) == 1
    
    def test_singleton_class_state_sharing(self):
        """测试单例实例的状态共享"""
        @singleton_class
        class CacheManager:
            def __init__(self):
                self.cache = {}
            
            def get(self, key):
                return self.cache.get(key)
            
            def set(self, key, value):
                self.cache[key] = value
        
        cache1 = CacheManager()
        cache2 = CacheManager()
        
        cache1.set("user:1", "Alice")
        assert cache2.get("user:1") == "Alice", "缓存应该共享"
    
    def test_singleton_class_thread_safety(self):
        """测试线程安全性"""
        @singleton_class
        class ThreadSafeClass:
            def __init__(self):
                self.value = 0
                time.sleep(0.01)
        
        instances = []
        lock = threading.Lock()
        
        def create_instance():
            instance = ThreadSafeClass()
            with lock:
                instances.append(instance)
        
        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        first_instance = instances[0]
        assert all(inst is first_instance for inst in instances), \
            "多线程环境下应该返回同一个实例"
    
    def test_singleton_class_with_custom_new(self):
        """测试自定义 __new__ 方法的类（覆盖 else 分支）"""
        @singleton_class
        class CustomNewClass:
            def __new__(cls, *args, **kwargs):
                # 自定义 __new__ 方法
                instance = super().__new__(cls)
                instance.created_by = "custom_new"
                return instance
            
            def __init__(self, value=0):
                self.value = value
        
        instance1 = CustomNewClass(10)
        instance2 = CustomNewClass(20)
        
        assert instance1 is instance2, "应该是同一个实例"
        assert instance1.created_by == "custom_new", "应该使用自定义的 __new__"
        # __init__ 会被再次调用，所以 value 会被更新
        assert instance2.value == 20
    
    def test_singleton_class_with_custom_new_and_args(self):
        """测试自定义 __new__ 方法且带参数的类"""
        @singleton_class
        class CustomNewWithArgs:
            def __new__(cls, name, age):
                # 自定义 __new__ 方法，处理参数
                instance = super().__new__(cls)
                instance._name = name
                instance._age = age
                return instance
            
            def __init__(self, name, age):
                # __init__ 仍然会被调用
                pass
            
            @property
            def info(self):
                return f"{self._name}:{self._age}"
        
        obj1 = CustomNewWithArgs("Alice", 25)
        obj2 = CustomNewWithArgs("Bob", 30)  # 参数会被忽略，返回同一个实例
        
        assert obj1 is obj2
        # 由于 __new__ 在第一次调用时执行，所以保持第一次的值
        assert obj1.info == "Alice:25"
        assert obj2.info == "Alice:25"


class TestSingletonEquivalence:
    """测试 singleton 和 singleton_class 的功能等价性"""
    
    def test_both_decorators_work_same(self):
        """测试两个装饰器功能相同"""
        @singleton
        class ClassA:
            def __init__(self):
                self.value = 1
        
        @singleton_class
        class ClassB:
            def __init__(self):
                self.value = 1
        
        a1 = ClassA()
        a2 = ClassA()
        b1 = ClassB()
        b2 = ClassB()
        
        assert a1 is a2
        assert b1 is b2
        assert a1.value == b1.value == 1
