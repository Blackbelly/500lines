from simple_model import OBJECT, TYPE, Class, Instance


def test_bound_method():
    class A(object):
        def add(self, a):
            return self.x + a

    obj = A()
    obj.x = 1
    add = obj.add
    assert add(4) == 5

    def add(self, a):
        return self.read_attr('x') + a

    A = Class(name='A', base_class=OBJECT, fields={'add': add}, meta_class=TYPE)
    obj = Instance(A)
    obj.write_attr('x', 1)
    m = obj.read_attr('add')
    assert m(4) == 5





