#!/usr/bin/env python
# -*- coding: utf-8 -*-








#############
# class Fruit(object):
#     def __init__(self,totle):
#         self.totle = totle

#     def set(self,count):
#         self.totle = count

#     def print_total(self):
#         print self.totle

# class Apple(Fruit):

#     def set(self,count):
#         self.totle = count

#     def print_total(self):
#         print self.totle

# fru = Fruit(45)
# fru.print_total()
# fru.set(50)
# fru.print_total()

# app = Apple(200)
# app.print_total()
##############
# alist = ['Ha', '   hello', 'World   ', 666, 8, 'de', '12', 5, 'Python', u'Www']
# blist = alist[:]


# def int_list(alist):
#     item_index = dict()
#     ret = dict()
#     for index, item in enumerate(alist):
#         item_index.update({item: index})
#     # print (item_index)
#     # 找出列表中大写开头的（去除空格后）和int型，并返回新列表
#     int_list = [int(numstr) for numstr in [
#         intnum for intnum in alist if isinstance(intnum, int)]]  # int_str_list
#     ret['item_index'] = item_index
#     ret['int_list'] = int_list
#     return ret
# # print (int_list)
# # print "#######int_list"


# def filter_list(alist, int_item_dict):
#     int_list = int_item_dict['int_list']
#     for j in int_list:
#         alist.remove(j)
#     # print alist
#     # [item for item in alist if item.strip().istitle()]  #newlist
#     # int元素和istitle元素组成新的列表
#     int_list.extend([item for item in alist if item.strip().istitle()])
#     return int_list

# # print (int_list)      #[8, 5, 'World', 'Python']


# def sort_index_list(int_str_list, int_item_dict):
#     index_list = []
#     item_index = int_item_dict['item_index']
#     # print item_index
#     for key in int_str_list:
#         index_list.append(item_index[key])
#     sort_indexlist = sorted(index_list)
#     return sort_indexlist
# # print (a)


# def int_and_stripstr(sort_indexlist):
#     ret = []
#     for i in sort_indexlist:
#         if isinstance(blist[i], int):
#             ret.append(blist[i])
#         elif isinstance(blist[i], basestring):
#             ret.append(blist[i].strip())
#         else:
#             pass
#     return ret


# def main(alist):
#     int_lists = int_list(alist)
#     int_str_list = filter_list(alist, int_lists)
#     sort_indexlist = sort_index_list(int_str_list, int_lists)
#     ret = int_and_stripstr(sort_indexlist)
#     return ret

# if __name__ == '__main__':
#     res = main(alist)
#     print(res)
# ret.append(alist[i] for i in a)
# print (ret)
# 按照原来顺序返回！！！
###########################
# class Student(object):

#     def __init__(self, name, course=None):
#         self.name = name
#         if not course:
#             self.course = []

#     def learn_language(self, course_name):
#         self.course.append(course_name)

#     def show_skill(self):
#         # lan = self.list_langeage()
#         print('{} is good at:{},{}.'.format(self.name, *self.list_langeage()))

#     def list_langeage(self):
#         lan = []
#         for item in self.course:
#             lan.append(item)
#         return lan


# a_programmer = Student('Peter')
# a_programmer.learn_language('Python')
# a_programmer.learn_language('Java')
# a_programmer.show_skill()

# print('*'*20)

# b_programmer = Student('Tom')
# b_programmer.learn_language('PHP')
# b_programmer.learn_language('Ruby')
# b_programmer.show_skill()

###########################
# # 有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数？都是多少？
# # 取1个，再从4个中取一个，如果在，则不加入，否则加入，循环两次
# myList=[]
# for i in range(1,5):
#   for j in range(1,5):
#       for k in range(1,5):
#           if i != j and j != k and i != k:
#               myStr = str(i)+str(j)+str(k)
#               myList.append(myStr)
#               print int(myStr)
# print len(myList)

# class BankAccount(object):
#     def __init__(self,name,countNum,balance):
#         self.name = name
#         self.count = countNum
#         self.balanceNum = balance

#     def balance(self):
#         print ("你的账户余额是%.2f"%self.balanceNum)
#     def saveMoney(self,cunNum):
#         self.balanceNum += cunNum
#         print ("你的存钱金额是%.2f"%cunNum)
#         print ("你的账户余额是%.2f"%self.balanceNum)
#         # return amount
#     def quMoney(self,quNum):
#         if self.balanceNum > quNum:
#             self.balanceNum -= quNum
#             print("本次取钱金额为%.2f"%quNum)
#             print("账户余额金额为%.2f"%self.balanceNum)
#         else:
#             print("余额不足，你的可支配余额为%.2f"%self.balanceNum)

# class InterestAccount(BankAccount):
#     # def __init__(self,rate):
#     #     self.rate = rate
#     def addInterest(self,rate):
#       # leaveMon =
#         Lixi = self.balanceNum * rate
#         print ("本年账户产生利息%.2f"%Lixi)
#         self.balanceNum += Lixi
#         print("账户余额为%.2f"%self.balanceNum)
# if __name__ == '__main__':
#     amount = InterestAccount("hello",12345,0.0)
#     amount.balance()
#     amount.saveMoney(800)
#     amount.quMoney(999)

#     # lixi = InterestAccount(0.003)
#     amount.addInterest(0.03)

###########################

# def makebold(func):
#   def wrapper():
#       mystr = "<b>"+func()+"</b>"
#       return mystr
#   return wrapper

# def makeitalic(func):
#   def wrapper():
#       mystr = "<i>"+func()+"<i>"
#       return mystr

#   return wrapper


# # <b><i>Hello<i></b>
# @makebold
# @makeitalic
# def say():
#   return "hello,world!"
# if __name__ == '__main__':
#   a = say()fghgfjh
#   print a

###########################

# def getTime():
#   start = time.clock()
#   foo()
#   end = time.clock()
#   times = end-start
#   print ("The function takes %f"%times)
#   print type(end-start)
# def getTime(fun):
#   def wrapper():
#       start = time.clock()
#       fun()
#       end = time.clock()
#       times = end - start
#       return times
#       print("The function takes %f"%times)
#   return wrapper

# @getTime
# def foo():
#   print "this is foo."
# if __name__ == '__main__':

#   a = foo()
    # print("The function takes %f"%a)
