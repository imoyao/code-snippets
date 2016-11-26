# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import json
import os
import torndb

from tornado.web import RequestHandler, url, StaticFileHandler
from tornado.options import define, options

define("port", default=8000, type=int)


class BaseHandler(RequestHandler):
	def prepare(self):
		pass

	def write_error(self, status_code, **kwargs):
		pass

	def set_default_headers(self):
		pass

	def initialize(self):
		pass

	def on_finish(self):
		pass

class IndexHandler(BaseHandler):

	def get(self):
		userId = self.get_argument("uId")
		# # 对数据库进行查询操作
		sql = "select hi_house_id,hi_user_id,hi_name,hi_address,hi_price from it_user_info inner join it_house_info on ui_user_id=hi_user_id where hi_user_id = %(userId)s"
		
		dataDic ={
			"userId":userId
		}
		# dataDic = dict(
		# 	userId = userId		
		# )
		# self.application.db.get()
		# self.write("aaa")
		try:
			# ret = self.application.db.get("select ui_name,ui_user_id from it_user_info where ui_user_id=1")
			# 输入房东id获得房屋信息(获得一个torndb.Row的列表)
			ret = self.application.db.query(sql,**dataDic)
			# ret = self.application.db.query("select hi_house_id,hi_user_id,hi_name,hi_address,hi_price from it_house_info where hi_user_id = %(userId)s")
		except Exception, e:
			return self.write("DB error:%s"%e)

		houseInfo = []
		if ret:
			for l in ret:
				hInfo = dict(
					hId = l.hi_house_id,
					hUId = l.hi_user_id,
					hName = l.hi_name,
					hAddr = l.hi_address,
					hPrice = l.hi_price,
				)
				# hInfo = {
				# 	'hId':l.hi_house_id,
				# 	'hUId':l.hi_user_id,
				# 	'hName':l.hi_name,
				# 	'hAddr':l.hi_address,
				# 	'hPrice':l.hi_price,
				# }
				houseInfo.append(hInfo)

			# data = dict(
			# userName = ret.ui_name,
			# userId = ret.ui_user_id
			# )
			
		# self.write("Succeed:the data is:%s"%houseInfo)
		print type(houseInfo)
		self.write({"errno":0, "errmsg":"OK", "data":houseInfo})			
			# json_data = json.dumps(data)
			# self.write(json_data)

		# ret = self.application.db.get("select ui_name,ui_user_id from it_user_info where ui_user_id=1")
		# print type(ret)
		# self.write(ret["ui_name"])
		# self.write("userName:"+ret.ui_name+"***")
		# self.write("userId:"+str(ret.ui_user_id))

class InsertHandler(BaseHandler):
	def post(self):
		name = self.get_argument("name")
		passwd = self.get_argument("passwd")
		mobile = self.get_argument("mobile")
		sql = "insert into it_user_info(ui_name,ui_passwd,ui_mobile) values(%(name)s,%(passwd)s,%(mobile)s)"
		dataDic = dict(
			name = name,
			passwd = passwd,
			mobile = mobile			
		)
		try:
			# 执行sql语句,	返回影响的最后一条自增字段值
			user_id = self.application.db.execute(sql,**dataDic)
			# user_id = self.application.db.execute(sql,name=name, passwd=passwd, mobile=mobile)
		except Exception, e:
			# print e
			return self.write("DB error:%s"%e)
		else:
			# self.write("DB OK:%d"%user_id)
			self.write("Succeed:The changed id is %d."%user_id)
			# self.write(str(user_id))
		finally:
			pass

		

	# def post(self):
	# 	name = self.get_argument("name")
	# 	passwd = self.get_argument("passwd")
	# 	mobile = self.get_argument("mobile")
	# 	sql = "insert into it_user_info(ui_name, ui_passwd, ui_mobile) values(%(name)s, %(passwd)s, %(mobile)s)"
	# 	try:
	# 		user_id = self.application.db.execute(sql, name=name, passwd=passwd, mobile=mobile)
	# 	except Exception as e:
	# 		print e
	# 		return self.write("DB error:%s" % e)
	# 	self.write(str(user_id))

class HouseHandler(BaseHandler):
	def get(self):
		user_id = self.get_argument("uid")
		sql = "select * from it_house_info inner join it_user_info on  hi_user_id = ui_user_id vimvimmwhere ui_user_id=%(user_id)s"
		try:
			user_id = self.application.db.execute(sql, name=name, passwd=passwd, mobile=mobile)
		except Exception as e:
			print e
			return self.write({"errNum":1,"errMsg":"db error:%s","data":[]%e})

class Application(tornado.web.Application):
	def __init__(self,*args,**kwargs):
		super(Application,self).__init__(*args,**kwargs)
		self.db = torndb.Connection(
			host = "127.0.0.1",
			database = "itcast",
			user = "root",
			password = "mysql",
		)


if __name__ == '__main__':
	tornado.options.parse_command_line()
	current_path = os.path.dirname(__file__)
	
	urlHandlers = [
	(r"/",IndexHandler),
	(r"/insert",InsertHandler),

	]
	settings = dict(
		static_path = os.path.join(current_path, "static"),
		template_path = os.path.join(current_path, "template"),
		debug=True,
	)
	app = Application(urlHandlers,**settings
	)


	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()