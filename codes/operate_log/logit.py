import inspect
from inspect import isfunction
import types
class Person:

    def __init__(self,name,age) -> None:
        self.name= name
        self.age= age

    def method(self):
        pass

class Tool:

    def __init__(self,name,price,size) -> None:
        self.name= name
        self.price= price
        self.size= size

def diff_log(old_inst,new_inst):
    """
    比较两个任意对象的属性不同
    """
    def class_name_of_inst(_inst):
        return type(_inst).__name__
    class_of_old_inst = class_name_of_inst(old_inst)
    class_of_new_inst = class_name_of_inst(new_inst)
    if class_of_new_inst == class_of_old_inst:
        old_values = get_attr_of_obj(old_inst)
        new_values = get_attr_of_obj(new_inst)
        for attr in old_inst:
            pass
            

alean = Person('alean',28)

def get_attr_of_obj(inst):
    attributes = dir(inst)
    ret = []
    b = [a for a in attributes if not(a.startswith('__') and a.endswith('__'))]
    for item in b:
        if not isinstance(getattr(inst,item),types.MethodType):
            ret.append(getattr(inst,item))

    return ret

ret = get_attr_of_obj(alean)
print(ret)