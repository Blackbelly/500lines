from simple_model import OBJECT, TYPE, Class, Instance


def test_read_write_fields():
    class A(object):
        pass

    obj = A()
    obj.a = 2
    obj.b = 5

    assert obj.a == 2
    assert obj.b == 5

    A = Class(name='A', base_class=OBJECT, fields={}, meta_class=TYPE)
    obj = Instance(A)
    obj.write_attr('a', 2)
    assert obj.read_attr('a') == 2

    obj.write_attr('b', 5)
    assert obj.read_attr('b') == 5
    assert obj.read_attr('a') == 2




























