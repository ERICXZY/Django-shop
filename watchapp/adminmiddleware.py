#导入正则库
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import re
class AdminMiddleware:
	def __init__(self,get_response):
		self.get_response=get_response
		#初始化发生在服务器启动之时
		#为什么会初始化两次
		#print("初始化")
	def __call__(self,request):
		#只要请求该服务器就会调用中间件对象
		#print("测试调用该中间件")
		#1.利用request获得当前请求对象要访问的路径
		path=request.path
		#查看path
		#print(1,path)
		#2.只要访问管理端就需要登录,使用正则匹配
		#match对于第一个参数，在第二个参数中匹配
		#3.为了不限制所有的watchadmin下的路径，将登陆面板特殊对待(关于登陆的均需特殊添加)
		#4.前端页面也是如此'/','/products','/typo','/contact','/account','/register','/single'
		plist=['/watchadmin/admin','/watchadmin/login','/order','/member','/checkout']
		if re.match("/watchadmin",path) and path not in plist:
			#为了保持登入者之后的状态，加入session
			if "adminuser" not in request.session:
				return redirect(reverse("admin_login"))
				
		#非后台页面，且访问列表中的页面时，需要登录，注册
		elif (not re.match("/watchadmin",path)) and (path in plist):
			if "user" not in request.session:
				return redirect(reverse("account"))
		response=self.get_response(request)
		return response