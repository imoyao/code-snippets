import inspect
from inspect import isfunction
import types

""" 
ref: https://www.zhihu.com/question/26848331
"""
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
    比较两个任意对象的新老属性不同
    """
    def class_name_of_inst(_inst):
        return type(_inst).__name__
    class_of_old_inst = class_name_of_inst(old_inst)
    class_of_new_inst = class_name_of_inst(new_inst)
    if class_of_new_inst == class_of_old_inst:
        old_values = get_attr_of_obj(old_inst)
        new_values = get_attr_of_obj(new_inst)
        all_values =set(old_values + new_values) 
        diff_map = dict()
        for attr in all_values:
            print(attr)
            old_value = getattr(old_inst,attr)
            new_value = getattr(new_inst,attr)
            if old_value != new_value:
                item = f'{attr} of {class_of_new_inst} from {old_value} to {new_value}'
                diff_map[attr] = item
    return diff_map


def get_attr_of_obj(inst):
    attributes = dir(inst)
    ret = []
    b = [a for a in attributes if not(a.startswith('__') and a.endswith('__'))]
    for item in b:
        if not isinstance(getattr(inst,item),types.MethodType):
            ret.append(item)

    return ret
alean = Person('alean',28)
peter = Person('peter',None)
ret=diff_log(alean,peter)
# ret = get_attr_of_obj(alean)
print(ret)