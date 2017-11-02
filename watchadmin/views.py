from django.shortcuts import render
from django.http import HttpResponse
from watchadmin.models import Users,Types,Goods,Orders,Detail,Contents,Magn
import hashlib
import time,re,json
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# Create your views here.

#管理员名称：ericadmin
#密码：eric1003939032
#后台登陆页
def adminlogin(request):
	return render(request,'watchadmin/login.html')
#执行登陆操作
def doadminlogin(request):
	#首先判断是否为管理员账户
	try:
		username=request.POST["username"]
		user=Users.objects.get(username=username)
		#读取密码
		s=request.POST["password"].encode("utf-8")
		md=hashlib.md5()
		md.update(s)
		if 0!=user.state:
			context={"info":"只允许管理员登入"}
			return render(request,'watchadmin/login.html',context)
		elif user.password!=md.hexdigest():
			context={"info":"密码错误"}
			return render(requset,'watchadmin/login.html',context)
		else:
			u={"id":user.id,"username":user.username,"name":user.name,"password":user.password,"sex":user.sex,"address":user.sex,"code":user.code,"phone":user.phone,"email":user.email,"state":user.state,"addtime":user.addtime}
			request.session["adminuser"]=u
			request.session["adminname"]=user.username
			return render(request,"watchadmin/index.html")
	except:
		return render(request,"watchadmin/login.html",{"info":"用户名错误"})

#退出登陆
def logout(request):
	#必须清除session，否则会自动登陆
	del request.session["adminuser"]
	return render(request,"watchadmin/login.html")


#后台管理首页
def index(request):
	return render(request,'watchadmin/index.html')
#用户首页
#def usersindex(request):
#	return render
#分页显示用户信息
def pagTest(request,pIndex):
	#声明全局变量，在删除信息时使用
	global pt,n
	pt=request.path[15:]
	li=Users.objects.all()
	for user in li:
		user.addtime=time.strftime("%Y-%m-%d",time.localtime(user.addtime))
		if user.sex==1:
			user.sex="男"
		else:
			user.sex="女"
	for user in li:
		if user.state==0:
			user.state="管理员"
		elif user.state==1:
			user.state="开启"
		elif user.state==2:
			user.state="禁用"
	p1=Paginator(li,12)
	if pIndex=="":
		pIndex="1"
	p=p1.page(int(pIndex))
	#n=p.len()
	return render(request,'watchadmin/users/index.html',{"p":p,"lip":p1.page_range})
#后台添加用户的form表单
def usersadd(request):
	return render(request,'watchadmin/users/add.html')
#后台将数据插入表格
def usersinsert(request):
	try:
		user=Users()
		user.username=request.POST["username"]
		user.name=request.POST["name"]
		user.sex=request.POST["sex"]
		#在hash之前必须规定一个字符编码
		s=request.POST["password"].encode("utf-8")
		md=hashlib.md5()
		md.update(s)
		user.password=md.hexdigest()
		#转换为可识别方式
		user.address=request.POST["address"]
		user.code=request.POST["code"]
		user.phone=request.POST["phone"]
		user.email=request.POST["email"]
		user.state=request.POST["state"]
		user.addtime=time.time()
		p1=re.compile(r'.{6,32}')
		p2=re.compile(r'[0-9a-zA-Z]{12,32}')
		if not p1.match(request.POST["username"]):
			return render(request,'watchadmin/users/add.html',{"info":"请输入6-32位的用户名"})
		elif not p2.match(request.POST["password"]):
			return render(request,'watchadmin/users/add.html',{"info":"请输入12-32位的密码"})
		elif request.POST["password"]!=request.POST["password2"]:
			return render(request,'watchadmin/users/add.html',{"info":"两次密码输入不一致"})
		else:
			user.save()
			return render(request,'watchadmin/info.html',{"info":"添加成功"})
	except:
		return render(request,'watchadmin/info.html',{"info":"添加失败,系统错误"})
#后台删除数据
def usersdel(request,uid):
	try:
		#print(request.path)
		user=Users.objects.get(id=uid)
		user.delete()
		#if n>0:
		return redirect(reverse("pagTest",args=(pt,)))
		#else:
			#return redirect(reverse("pagTest",args=(pt-1,)))
	except:
		return render(request,"watchadmin/info.html",{"info":"删除失败"})
#后台用户编辑信息表
def usersedit(request,uid):
	user=Users.objects.get(id=uid)
	context={"user":user}
	return render(request,"watchadmin/users/edit.html",context)
#后台用户提交数据到数据库
def usersupdate(request):
	try:
		#用户名不能重复
		p=request.POST["uid"]
		user=Users.objects.get(id=p)
		user.name=request.POST["name"]
		user.sex=request.POST["sex"]
		#在hash之前必须规定一个字符编码
		s=request.POST["password"].encode("utf-8")
		md=hashlib.md5()
		md.update(s)
		user.password=md.hexdigest()
		#转换为可识别方式
		user.address=request.POST["address"]
		user.code=request.POST["code"]
		user.phone=request.POST["phone"]
		user.email=request.POST["email"]
		user.state=request.POST["state"]
		user.addtime=time.time()
		p1=re.compile(r'.{6,32}')
		p2=re.compile(r'[0-9a-zA-Z]{12,32}')
		if not p1.match(request.POST["username"]):
			return render(request,'watchadmin/users/add.html',{"info":"请输入6-32位的用户名"})
		elif not p2.match(request.POST["password"]):
			return render(request,'watchadmin/users/add.html',{"info":"请输入12-32位的密码"})
		elif request.POST["password"]!=request.POST["password2"]:
			return render(request,'watchadmin/users/add.html',{"info":"两次密码输入不一致"})
		else:
			user.save()
			return render(request,'watchadmin/info.html',{"info":"修改成功"})
	except:
		return render(request,'watchadmin/info.html',{"info":"修改失败"})





