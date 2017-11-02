from django.shortcuts import render
from django.http import HttpResponse
from watchadmin.models import Users,Types,Goods,Orders,Detail,Contents,Magn
import hashlib
import time,re,json
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
# Create your views here.
#分页显示订单页
def poindex(request,pIndex):
	ol=Orders.objects.all()
	for order in ol:
		order.addtime=time.strftime("%Y-%m-%d",time.localtime(order.addtime))
		if order.state==0:
			order.state="新订单"
		elif order.state==1:
			order.state="已发货"
		elif order.state==2:
			order.state="已收货"
		elif order.state==3:
			order.state="无效订单"
	p1=Paginator(ol,12)
	if pIndex=="":
		pIndex="1"
	p=p1.page(int(pIndex))
	#n=p.len()
	return render(request,'watchadmin/orders/index.html',{"p":p,"lip":p1.page_range})

#跳转至修改页
# def orderupdate(request,oid):
# 	order=Orders.objects.get(id=oid)
# 	context={"order":order}
# 	return render(request,'watchadmin/orders/update.html',context)
#修改状态
# def orderdoupdate(request,oid):
# 	try:
# 		order=Orders.objects.get(id=oid)
# 		order.state=request.POST["state"]
# 		order.save()
# 		context={"info":"修改成功"}
# 		return render(request,'watchadmin/info.html',context)
# 	except:
# 		context={"info":"修改失败"}
# 		return render(request,'watchadmin/info.html',context)

#查看订单详情
def detail(request,oid):
	order=Orders.objects.get(id=oid)
	details=Detail.objects.filter(orderid=oid)
	#为当前订单添加用户名
	username=Users.objects.get(id=order.uid).username
	order.username=username
	order.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(order.addtime))
	#格式化当前订单中的商品
	for detail in details:
		detail.totalprice=detail.num*detail.price
		detail.picname=Goods.objects.get(id=detail.goodsid).picname
	context={"order":order,"details":details}
	return render(request,'watchadmin/orders/orderdetail.html',context)

#修改订单状态
def send(request,sid):
	order=Orders.objects.get(id=sid)
	order.state=1
	order.save()
	return redirect(reverse('admin_delcontents',args=(sid,)))
def cancel(request,sid):
	order=Orders.objects.get(id=sid)
	order.state=3
	order.save()
	return redirect(reverse('admin_delcontents',args=(sid,)))
