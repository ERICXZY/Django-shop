from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from watchapp.models import Users,Types,Goods,Orders,Detail,Contents,Magn
import time
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# Create your views here.
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
#首页
def index(request):
	context=loadContext()
	#获取点击量最大的4条信息，放置在首页
	goodsclick=Goods.objects.all().order_by('-clicknum')[0:4]
	context["goodsclick"]=goodsclick
	#获取最新的4条信息，放置在首页
	goodstime=Goods.objects.all().order_by('-addtime')[0:4]
	for good in goodstime:
		good.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(good.addtime))
	context["goodstime"]=goodstime
	#获取价格排序的4条信息，放置在首页
	goodsprice=Goods.objects.all().order_by('price')[0:4]
	context["goodsprice"]=goodsprice
	return render(request,'watchapp/index.html',context)
#列表页
def products(request,pIndex,pid=0):
	context=loadContext()
	goods=[]
	if pid==0:
		t=Types.objects.filter(path__contains=str(pid)+",")
		#print(1,t)
		for ob in t:
			length=len(ob.path.split(","))
			#print(2,length)
			if length==4:
				good=Goods.objects.filter(typeid=ob.id)
				if len(good)>0:
					#print(len(good))
					for i in good:
						goods.append(i)
				
	else:
		t=Types.objects.filter(path__contains=","+str(pid)+",")
		if not t:
			goods=Goods.objects.filter(typeid=pid)
		else:
			for ob in t:
				length=len(ob.path.split(","))
				#print(2,length)
				if length==4:
					good=Goods.objects.filter(typeid=ob.id)
					if len(good)>0:
						print(len(good))
						for i in good:
							goods.append(i)

	context["goods"]=goods
	p1=Paginator(goods,6)
	if pIndex=="":
		pIndex="1"
	p=p1.page(int(pIndex))
	#n=p.len()
	context["p"]=p
	context["pid"]=pid
	context["lip"]=p1.page_range
	return render(request,'watchapp/products.html',context)
	#return render(request,'watchapp/products.html',context)	

#详情页
def single(request,pid):
	context=loadContext()
	#获取指定的商品
	good=Goods.objects.get(id=pid)
	#获取该商品的评论
	contents=Contents.objects.filter(goodsid=pid)
	#格式化
	for content in contents:
		content.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(content.addtime))
	#获取该商品已被购买的记录
	shop=Detail.objects.filter(goodsid=pid)
	#获取该单品对应的放大镜图片
	magns=Magn.objects.filter(goodsid=pid)
	if len(magns) > 3:
		magns=Magn.objects.filter(goodsid=pid).order_by('-picname')[0:3]
	#获取该商品类别中随机三件商品
	goodslist=Goods.objects.filter(typeid=good.typeid).order_by('?')[0:3]
	#计算该商品的点击量
	good.clicknum += 1
	#计算该商品卖出去的数量
	good.num=len(shop)
	good.save()
	good.addtime=time.strftime("%Y-%m-%d",time.localtime(good.addtime))
	#修改库存量
	good.store=good.store-good.num
	context["good"]=good
	context["contents"]=contents
	context["goodslist"]=goodslist
	context["magns"]=magns
	return render(request,'watchapp/single.html',context)

#添加评论
def contents(request,pid):
	#获取指定的商品
	#good=Goods.objects.get(id=pid)
	#获取当前用户
	try:
		user=request.session["user"]
		#获取当前用户的订单
		orders=Orders.objects.filter(uid=user["id"])
		#对于每个订单，检查商品是否被当前用户购买过
		goodsid=[]
		for order in orders:
			details=Detail.objects.filter(orderid=order.id)
			for detail in details:
				goodsid.append(detail.goodsid)
		#print(goodsid)
		##如果当前用户购买了该商品，允许评论
		if int(pid) in goodsid:
			#实例化评论的数据
			#print(pid)
			con=Contents()
			#添加数据
			con.uid=user["id"]
			con.goodsid=pid
			con.username=user["name"]
			con.content=request.POST["content"]
			con.addtime=time.time()
			con.save()
			return redirect(reverse('single',args=(pid,)))
		else:
			return render(request,'watchapp/info.html',{"info":"您未购买此商品，不能评论"})
	except:
		return render(request,'watchapp/info.html',{"info":"请您登录后再评论"})

#删除评论
def delcontents(request,pid):
	#获取当前用户
	content=Contents.objects.get(id=pid)
	#删除该条数据
	content.delete()
	#返回当前商品详情页
	return redirect(reverse('single',args=(content.goodsid,)))

#商品推介
	

#联系我们
def contact(request):
	context=loadContext()
	return render(request,'watchapp/contact.html',context)
#官方博客
def typo(request):
	context=loadContext()
	return render(request,'watchapp/typo.html',context)

