# coding=utf-8
# code from # http://www.cnblogs.com/itogo/p/5639221.html

# HOWTO: user and args!!!!!!!

import sys

user = {'name':'','is_login':False,'is_admin':False}

def login_confirm(func):
	def wrapper(*args,**kwargs):
		user = args[0]
		if user['is_login']:
			func(*args,**kwargs)
		else:
			print ('未登录用户')
			index()
		return func
	return wrapper

def admin_confirm(func):
	def wrapper(*args,**kwargs):
		user = args[0]
		if user['is_admin']:
			func(*args,**kwargs)
		else:
			print ("无管理员权限")
			index()
		return func
	return wrapper

def index():
	print ("Welcome to the homepage for everyone.")

@login_confirm
def normal_user(user):
	print ("Welcome {0},This page is for login user.".format(user['name']))

@admin_confirm
@login_confirm
def admin(user):
	print ("Welcome {0},This page is for the ADMIN.".format(user['name']))

def login(user):
	# print "in user1111:{0}".format(user)
	name = raw_input("please enter your name:")
	pw = raw_input("please enter your passwd:")

	if name == "admin" and pw == '111111':
		user['name'] = 'admin'
		user['is_login'] = True
		user['is_admin'] = True
	elif name and pw == '123':
		user['name'] = name
		user['is_login'] = True
	else:
		user['name'] = name
	# print "outer user111:{0}".format(user)
	return user

def main(user):
	while True:
		print ("1:访问首页，2：管理员界面，3：普通用户界面，q:退出 \n")
		enter_str = raw_input("please enter the num:")
		if enter_str == 'q':
			sys.exit()
		elif enter_str == '1':
			index()
		elif enter_str == '2':
			chose_login = raw_input("please login(y/n):")
			if chose_login.lower() == 'y':
				print ("this is {0}".format(user))
				login(user)
				admin(user)
			else:
				index()
		elif enter_str == '3':
			chose_login = raw_input("please login(y/n):")
			if chose_login.lower() == 'y':
				login(user)
				normal_user(user)
			else:
				index()
		else:
			print("please check your type?")

		user = {'name':'','is_login':False,'is_admin':False}


if __name__ == '__main__':		#TODO clear usr info
	main(user)