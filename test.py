#coding=utf-8
import time
# # 有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数？都是多少？
# # 取1个，再从4个中取一个，如果在，则不加入，否则加入，循环两次
# myList=[]
# for i in range(1,5):
# 	for j in range(1,5):
# 		for k in range(1,5):
# 			if i != j and j != k and i != k:
# 				myStr = str(i)+str(j)+str(k)
# 				myList.append(myStr)
# 				print int(myStr)
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
#     	# leaveMon = 
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

# def makebold(func):
# 	def wrapper():
# 		mystr = "<b>"+func()+"</b>"
# 		return mystr
# 	return wrapper

# def makeitalic(func):
# 	def wrapper():
# 		mystr = "<i>"+func()+"<i>"
# 		return mystr

# 	return wrapper


# # <b><i>Hello<i></b>
# @makebold
# @makeitalic
# def say():
# 	return "hello,world!"
# if __name__ == '__main__':
# 	a = say()fghgfjh
# 	print a


# def getTime():
# 	start = time.clock()
# 	foo()
# 	end = time.clock()
# 	times = end-start
# 	print ("The function takes %f"%times)
# 	print type(end-start)
def getTime(fun):
	def wrapper():
		start = time.clock()
		fun()
		end = time.clock()
		times = end - start
		return times
		print("The function takes %f"%times)
	return wrapper

@getTime	
def foo():
	print "this is foo."
if __name__ == '__main__':
	
	a = foo()
	# print("The function takes %f"%a) 
