# coding=utf-8
# !/usr/bin/python
from foo import do_foo

# from deco_order import foo, bar


# # 1. exec
# module_name = 'module'
# exec('  '.join(['import', module_name]))
# a = module.A()
# a.foo()
# a.bar()
# module.baz()

# 2. __import__

# module_name = 'module'  # 模块名
# class_name = 'A'  # 类名
# class_method = 'foo'  # 类中方法名称
# func_name = 'bar'  # 函数名
# module_obj = __import__(module_name)
# # 调用模块中的类
# class_of_module_obj = getattr(module_obj, class_name)
# # 实例化对象
# instance_of_cmo = class_of_module_obj()
# # 调用实例的方法
# method_of_cmo = getattr(instance_of_cmo, class_method)
# method_of_cmo()
# instance_of_cmo.static_method()
# # 调用模块的函数
# func_of_mo = getattr(module_obj, func_name)
# func_of_mo()
# # 也可以直接调用（像真正import模块那样）
# module_obj.baz()

# 3. importlib
import importlib

module_name = 'module'

module_obj = importlib.import_module(module_name)
class_of_module_obj = module_obj.A()
class_of_module_obj.foo()
class_of_module_obj.static_method()
module_obj.bar()
