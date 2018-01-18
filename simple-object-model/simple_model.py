
MISSING = object()


class Base(object):
    """
    base class of all classes
    类有几种基本实现: (注意, 先关注行为, 再考虑具体实现)
    1. 继承: a 是 object 的 subclass, 继承 object 的属性, 方法
    2. 实例化: a 是 A 的实例, 具备 A 的所有属性, a 的 class 是 A
    3. 获取 / 设置属性: 
    4. 名称:
    """
    def __init__(self, cls, fields):
        self.cls = cls
        self._fields = fields

    def write_attr(self, key, value):
        self._write_dict(key, value)

    def read_attr(self, key):
        attr = self._read_dict(key)
        if attr is not MISSING:
            return attr
        method = self.cls._read_from_class(key)
        if _is_bindable(method):
            return make_boundmethod(method, self)
        raise AttributeError(key)

    def _write_dict(self, key, value):
        self._fields[key] = value

    def _read_dict(self, key):
        return self._fields.get(key, MISSING)

    def isinstance(self, cls):
        return self.cls.issubclass(cls)

    def call_method(self, methname, *args, **kwargs):
        method = self.cls._read_from_class(methname)
        return method(*args, **kwargs)


class Instance(Base):
    # 实例 只关心 class 和 属性
    def __init__(self, cls):
        assert isinstance(cls, Class)
        Base.__init__(self, cls, {})


class Class(Base):
    # class 只关心父类 和 name
    def __init__(self, name, base_class, fields, meta_class):
        Base.__init__(self, meta_class, fields)
        self.name = name
        self.base_class = base_class

    def method_resolution_order(self):
        if self.base_class is None:
            return [self]
        else:
            return [self] + self.base_class.method_resolution_order()

    def issubclass(self, cls):
        return cls in self.method_resolution_order()

    def _read_from_class(self, methname):
        for cls in self.method_resolution_order():
            if methname in cls._fields:
                return cls._fields[methname]
        return MISSING


def _is_bindable(method):
    return callable(method)


def make_boundmethod(method, self):
    def bound(*args, **kwargs):
        return method(self, *args, **kwargs)
    return bound


# 创建 object 类, 相当于 class object:
OBJECT = Class(name='object', base_class=None, fields={}, meta_class=None)

# 创建 type 类, 是 object 的继承类, 相当于 class type(object):
TYPE = Class(name='type', base_class=OBJECT, fields={}, meta_class=None)

# TYPE 是它自己的实例
TYPE.cls = TYPE

# OBJECT 是 TYPE 的实例
OBJECT.cls = TYPE



