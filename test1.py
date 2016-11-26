import os
class Person(object):
	@classmethod
	def sing(self):
		print("the person is sing.")
	def running(self):
		print("the person is running.")
	@property
	def joking(self):
		print("the person is joking.")



if __name__ == '__main__':
	xiaoming = Person()
	
	xiaoming.running()
	xiaoming.joking
	# Person.joking+"heheh"

	xiaoming.sing()
	print("*"*20)
	# Person.running()
	Person.sing()

# class Person(object):


# a= os.path.join(os.path.dirname(__file__),"./test.py")
# print type(a)
