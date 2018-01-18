from simple_model import Class, Instance, OBJECT, TYPE


def test_isinstance():
    """
    校验实例化
    实例化的具体表现:
    b 由 B 实例化产生, 那么 b 是 B 的实例, 同时也是 B 父类 A 的实例, 以此类推, 也是 A 父类 object 的实例
    但是不是元类的实例
    """
    class A(object):
        pass

    class B(A):
        pass

    b = B()
    assert isinstance(b, B)
    assert isinstance(b, A)
    assert isinstance(b, object)
    assert not isinstance(b, type)

    A = Class(name='A', base_class=OBJECT, fields={}, meta_class=TYPE)
    B = Class(name='B', base_class=A, fields={}, meta_class=TYPE)

    b = Instance(B)
    assert b.isinstance(B)
    assert b.isinstance(A)
    assert b.isinstance(OBJECT)
    assert not b.isinstance(TYPE)





