from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from watchapp.models import Users,Types,Goods,Orders,Detail,Contents,Magn
import time
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# Create your views here.
#购物车和订单页
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

#购物车
def checkout(request):
	context=loadContext()
	#统计购物车内商品总价
	allprice=0
	allnum=0
	if "checkoutlist" not in request.session:
		request.session["checkoutlist"]={}
	checkoutlist=request.session["checkoutlist"]
	for one in checkoutlist:
		if request.session["user"]["id"] == checkoutlist[one]["uid"]:
			#计算当前用户购物车内物品的数量
			allnum += 1
			#当前用户购物车的价格
			allprice += checkoutlist[one]["totalprice"]
	request.session["allprice"]=allprice
	request.session["allnum"]=allnum
	return render(request,'watchapp/checkout.html',context)

#添加到购物车
def docheckout(request,sid):
	if "checkoutlist" in request.session:
		pass
	else:
		request.session["checkoutlist"]={}
	#将session里的checkoutlist拿出来，进行操作
	checkoutlist=request.session["checkoutlist"]
	if sid in checkoutlist:
		if not request.POST["n"]:
			checkoutlist[sid]["total"] += 1
		else:
			checkoutlist[sid]["total"] += int(request.POST["n"])
		print(checkoutlist[sid]["total"])
		checkoutlist[sid]["totalprice"]=checkoutlist[sid]["total"]*checkoutlist[sid]["price"]
	else:
		good=Goods.objects.get(id=sid)
		good.addtime=time.strftime("%Y-%m-%d",time.localtime(good.addtime))
		total=1
		totalprice=good.price*total
		#该购物车的主人
		uid=request.session["user"]["id"]
		#做一个单品字典，用来存放单品信息
		goodinfo={"id":good.id,"uid":uid,"typeid":good.typeid,"goods":good.goods,"company":good.company,"descr":good.descr,"price":good.price,"picname":good.picname,"state":good.state,"store":good.store,"num":good.num,"clicknum":good.clicknum,"addtime":good.addtime,"total":total,"totalprice":totalprice}
		#怎样在页面获取sid,利用values函数
		checkoutlist[sid]=goodinfo
		
	if checkoutlist[sid]["total"]>checkoutlist[sid]["store"]:
		checkoutlist[sid]["total"]=checkoutlist[sid]["store"]
	

	#再将checkoutlist放入session
	request.session["checkoutlist"]=checkoutlist
	return redirect(reverse("checkout"))
	#return render(request,"watchapp/info.html")

#增加数量
def acheckout(request,sid):
	#将session里的checkoutlist拿出来，进行操作
	checkoutlist=request.session["checkoutlist"]
	#修改数字
	checkoutlist[sid]["total"] += 1
	checkoutlist[sid]["totalprice"]=checkoutlist[sid]["total"]*checkoutlist[sid]["price"]
	#再将checkoutlist放入session
	request.session["checkoutlist"]=checkoutlist
	return redirect(reverse("checkout"))

#减少
def dcheckout(request,sid):
	#将session里的checkoutlist拿出来，进行操作
	checkoutlist=request.session["checkoutlist"]
	#修改数字
	if checkoutlist[sid]["total"]!=1:
		checkoutlist[sid]["total"] -= 1
	else:
		checkoutlist[sid]["total"] = 1
	checkoutlist[sid]["totalprice"]=checkoutlist[sid]["total"]*checkoutlist[sid]["price"]
	#再将checkoutlist放入session
	request.session["checkoutlist"]=checkoutlist
	return redirect(reverse("checkout"))


#从购物车删除一个商品
def delcheckout(request,sid):
	#将session里的checkoutlist拿出来，进行操作
	checkoutlist=request.session["checkoutlist"]
	#将对应的商品删除
	del checkoutlist[sid]
	#放入session
	request.session["checkoutlist"]=checkoutlist
	return redirect(reverse("checkout"))

#清空购物车
def clearcheckout(request):
	#将session里的数据拿出
	checkoutlist=request.session["checkoutlist"]
	#将购物车的数据清空
	checkoutlist={}
	#将购物车信息更新
	request.session["checkoutlist"]={}
	return redirect(reverse("checkout"))


#订单页
def showorder(request):
	context=loadContext()
	if "orderlist" not in request.session:
		request.session["orderlist"]={}
	orderprice=0
	orderlist=request.session["orderlist"]
	for one in orderlist:
		orderprice += orderlist[one]["totalprice"]
	request.session["orderprice"]=orderprice
	return render(request,'watchapp/order.html',context)

#为该次订单填入商品
def order(request):
	#先初始化一个订单
	if "orderlist" not in request.session:
		request.session["orderlist"]={}
	#getlist可以获取多选框的值，形成字符串列表
	li=request.POST.getlist("one")
	#首先将session里的购物车取出来
	checkoutlist=request.session["checkoutlist"]
	#再将订单页的session取出来
	orderlist=request.session["orderlist"]
	#对于订单进行添加
	for sid in li:
		#如果已经在订单中，则将total和totalprice更新
		if sid in orderlist:
			orderlist[sid]["total"] += checkoutlist[sid]["total"]
			orderlist[sid]["totalprice"] += checkoutlist[sid]["totalprice"]
		else:
			#将购物车对应商品添加到订单页
			#print(sid)
			#print(checkoutlist[sid])
			orderlist[sid]=checkoutlist[sid]
		#且将购物车里对应的商品清除
		del checkoutlist[sid]
	#放入session
	request.session["checkoutlist"]=checkoutlist
	request.session["orderlist"]=orderlist
	t=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
	request.session["time"]=t
	request.session["orderlist"]=orderlist
	return redirect(reverse("showorder"))

#删除该次订单中的商品
def delorder(request,sid):
	#将session里的orderlist拿出来，进行操作
	orderlist=request.session["orderlist"]
	#将对应的商品删除
	del orderlist[sid]
	#放入session
	request.session["orderlist"]=orderlist
	return redirect(reverse("showorder"))

#清空该次订单的商品
def clearorder(request):
	#将session里的数据拿出
	orderlist=request.session["orderlist"]
	#将购物车的数据清空
	orderlist={}
	#将购物车信息更新
	request.session["orderlist"]={}
	return redirect(reverse("showorder"))

#将该次订单提交，跳转到收货地址确认信息的页面
def orderconfirm(request):
	print(request.POST)
	context=loadContext()
	return render(request,"watchapp/orderconfirm.html",context)

#进行再次确认信息，就会在数据库中添加订单信息，和订单详情信息
def orderadd(request):
	try:
		context=loadContext()
		#实例化订单数据对象
		order=Orders()
		order.linkman=request.POST["linkman"]
		order.phone=request.POST["phone"]
		order.code=request.POST["code"]
		order.address=request.POST["address"]
		order.addtime=time.time()
		order.total=request.session["orderprice"]
		order.state=0
		order.uid=request.session["user"]["id"]
		order.save()
		for good in request.session["orderlist"].values():
			#实例化订单详情数据对象
			detail=Detail()
			detail.orderid=order.id
			detail.goodsid=good["id"]
			detail.name=good["goods"]
			detail.price=good["price"]
			detail.num=good["total"]
			detail.save()
		del request.session["orderlist"]
		#跳转到订单页面
		return redirect(reverse('orderlist'))
	except:
		context=loadContext()
		context["info"]="提交失败"
		return render(request,'watchapp/info.html',context)

#确认成功后，点击订单，可以查看所有订单，和每个订单的详细信息
def orderlist(request,sid=''):
	context=loadContext()
	if sid=='':
		orderlist=Orders.objects.all()
	else:
		orderlist=Orders.objects.filter(state=sid)
	shoplist=Detail.objects.all()
	for order in orderlist:
		#格式化添加订单的时间
		order.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(order.addtime))
		#格式化手机号
		s1=order.phone[0:3]
		s2=order.phone[7:]
		order.phone=s1+"****"+s2
		if order.state == 0:
			order.state = "新订单"
		elif order.state == 1:
			order.state = "已发货"
		elif order.state == 2:
			order.state = "已收货"
		elif order.state == 3:
			order.state = "无效订单"
	#对于每个商品添加一个图片属性
	for shop in shoplist:
		good=Goods.objects.get(id=shop.goodsid)
		shop.picname=good.picname
	context["shoplist"]=shoplist
	context["orderlist"]=orderlist
	return render(request,'watchapp/orderlist.html',context)

#查看订单的详细信息
def detail(request,sid):
	context=loadContext()
	order=Orders.objects.get(id=sid)
	order.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(order.addtime))
	s1=order.phone[0:3]
	s2=order.phone[7:]
	order.phone=s1+"****"+s2
	details=Detail.objects.filter(orderid=sid)
	for shop in details:
		good=Goods.objects.get(id=shop.goodsid)
		shop.picname=good.picname
	context["shoplist"]=details
	context["order"]=order
	return render(request,'watchapp/detail.html',context)

#客户端修改状态
def receive(request,sid):
	order=Orders.objects.get(id=sid)
	order.state=2
	order.save()
	return redirect(reverse('orderlist'))
def cancel(request,sid):
	order=Orders.objects.get(id=sid)
	order.state=3
	order.save()
	return redirect(reverse('orderlist'))

