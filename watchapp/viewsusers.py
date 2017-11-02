from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from watchapp.models import Users,Types,Goods,Orders,Detail,Contents,Magn
import hashlib,time
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# Create your views here.
#登录，注册页，个人中心页
#定义数据提取函数
def loadContext():
	tp=Types.objects.all()
	#构建一个新列表，放入级别最低的商品类别。用于在下拉框中显示
	list1=[]
	list2=[]
	list3=[]
	for one in tp:
		length=len(one.path.split(","))
		if length==2:
			list1.append(one)
		elif length==3:
			list2.append(one)
		elif length==4:
			list3.append(one)
	context={"list1":list1,"list2":list2,"list3":list3}
	return context

#登录页
def account(request):
	context=loadContext()
	return render(request,'watchapp/account.html',context)
#登录状态保持
def doaccount(request):
	try:
		context=loadContext()
		#print(request.path)
		#将密码变为md5
		s=request.POST["password"].encode("utf-8")
		md=hashlib.md5()
		md.update(s)
		p=md.hexdigest()
		#获取为username的数据
		uname=request.POST["username"]
		user=Users.objects.get(username=uname)
		if p==user.password:
			u={"id":user.id,"username":user.username,"name":user.name,"password":user.password,"sex":user.sex,"address":user.sex,"code":user.code,"phone":user.phone,"email":user.email,"state":user.state,"addtime":user.addtime}

			request.session["user"]=u
		else:
			context["info"]="密码错误"
			return render(request,"watchapp/account.html",context)
		return redirect(reverse("member"))
	except:
		context=loadContext()
		context["info"]="无此用户"
		return render(request,"watchapp/info.html",context)
#会员登出
def outaccount(request):
	del request.session["user"]
	context=loadContext()
	context["info"]="请重新登录"
	return render(request,"watchapp/account.html",context)

#会员修改
def update(request,uid):
	user=Users.objects.get(id=uid)
	context=loadContext()
	context["user"]=user
	
	return render(request,"watchapp/update.html",context)

#执行修改
def doupdate(request,uid):
	try:
		user=Users.objects.get(id=uid)
		user.username=request.POST["username"]
		user.name=request.POST["name"]
		user.email=request.POST["email"]
		user.phone=request.POST["phone"]
		user.sex=request.POST["sex"]
		user.code=request.POST["code"]
		user.address=request.POST["address"]

		s=request.POST["password"].encode("utf-8")
		if request.POST["password"]!=request.POST["password2"]:
			return render(request,'watchapp/register.html',{"info":"两次密码输入不一致"})
		md=hashlib.md5()
		md.update(s)
		
		
		context=loadContext()
		context["info"]="修改成功"
		if user.password != md.hexdigest():
			user.password=md.hexdigest()
			user.save()
			return redirect(reverse("outaccount"))
		else:
			return render(request,'watchapp/info.html',context)
	except:
		context=loadContext()
		context["info"]="修改失败"
		return render(request,'watchapp/info.html',context)
	

#注册页
def register(request):
	context=loadContext()
	return render(request,'watchapp/register.html',context)
#将注册信息提交到数据库
def doregister(request):
	try:
		user=Users()
		user.username=request.POST["username"]
		user.name=request.POST["name"]
		user.email=request.POST["email"]
		user.phone=request.POST["phone"]
		user.sex=request.POST["sex"]
		user.code=request.POST["code"]
		user.address=request.POST["address"]

		s=request.POST["password"].encode("utf-8")
		if request.POST["password"]!=request.POST["password2"]:
			return render(request,'watchapp/register.html',{"info":"两次密码输入不一致"})
		md=hashlib.md5()
		md.update(s)
		user.password=md.hexdigest()

		user.addtime=time.time()
		user.state=1
		user.save()
		context=loadContext()
		context["info"]="注册成功"
		return render(request,'watchapp/account.html',context)
	except:
		context=loadContext()
		context["info"]="注册失败"
		return render(request,'watchapp/info.html',context)
#个人中心页
def member(request):
	#将session中的user取出，进行格式化
	user=request.session["user"]
	context=loadContext()
	s1=user["phone"][0:3]
	s2=user["phone"][7:]
	user["phone"]=s1+"****"+s2
	#再将其放入session
	request.session["user"]=user
	#获取当前用户每种状态订单的条数
	or0=[]
	or1=[]
	or2=[]
	or3=[]
	orderlist=Orders.objects.filter(uid=user["id"])
	for order in orderlist:
		if order.state==0:
			or0.append(order)
		elif order.state==1:
			or1.append(order)
		elif order.state==2:
			or2.append(order)
		elif order.state==3:
			or3.append(order)
	context["c0"]=len(or0)
	context["c1"]=len(or1)
	context["c2"]=len(or2)
	context["c3"]=len(or3)

	return render(request,'watchapp/member.html',context)