#静态模板
from django.shortcuts import render
#网页响应
from django.http import HttpResponse
#导入模型
from watchadmin.models import Users,Types,Goods,Orders,Detail,Contents,Magn
#时间，正则，时间,路径，加密
import time,re,json,time,os,hashlib
#分页
from django.core.paginator import Paginator
#重定向
from django.shortcuts import redirect
#反向解析
from django.core.urlresolvers import reverse
#验证码，和图片缩放使用
from PIL import Image


#排序会用到 list = Types.objects.extra(select = {'_has':'concat(path,id)'}).order_by('_has')
# Create your views here.

#分页显示商品类别
def ptindex(request,pIndex):
	#声明全局变量，在删除信息时使用
	global pt
	pt=request.path[19:]
	li=Types.objects.extra(select = {'_has':'concat(path,id)'}).order_by('_has')
		# 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
	for ob in li:
		ob.pname ='. . . '*(ob.path.count(',')-1)+ob.name
	#每页12条信息
	p1=Paginator(li,12)
	#当没有指定第几页时，默认第一页
	if pIndex=="":
		pIndex="1"
	#生成一个page对象，里面包含数据对象
	p=p1.page(int(pIndex))

	return render(request,'watchadmin/types/index.html',{"p":p,"lip":p1.page_range})

#后台添加商品类别的form表单
def typesadd(request,tid):
	#如果点击的是添加商品，则从根类别开始添加。接收的tid是字符串
	#pname用来在html显示
	if tid=="0":
		pname="根类别"
		context={"pname":pname,"tid":tid}
	else:
		t=Types.objects.get(id=tid)
		context={"type":t,"pname":t.name}
	return render(request,'watchadmin/types/add.html',context)

#后台将数据插入表格
def typesinsert(request):
	try:
		#id,name,pid,path
		#如果在根类添加，tid为0。填入的是子类，tid不为0
		if request.POST["tid"]!="0":
			#数据添加
			tp=Types()
			tp.name=request.POST["name"]
			tp.pid=request.POST["id"]
			tp.save()
			tp.path=request.POST["path"]+str(tp.pid)+","
			tp.save()
			context={"info":"添加成功"}
		else:
			#数据添加
			tp=Types()
			tp.name=request.POST["name"]
			tp.pid=0
			tp.save()
			tp.path="0,"
			tp.save()
			context={"info":"添加成功"}
	except:
		context={"info":"添加失败"}
	return render(request,"watchadmin/info.html",context)

#后台删除数据
def typesdel(request,uid):
	try:
		#print(request.path)
		tp=Types.objects.get(id=uid)
		#为什么filter和exclude效果一样
		p=Types.objects.filter(path__contains=str(uid))
		g=Goods.objects.filter(typeid=uid)
		if p.count()!= 0:
			return render(request,"watchadmin/info.html",{"info":"删除父类之前请清空并删除所有子类"})
		elif g.count()!=0:
			return render(request,"watchadmin/info.html",{"info":"删除该类之前请清空所有该类别商品"})
		else:
			tp.delete()
			#删除后停留在当前页面，之后需要完善页面数据删完后，跳转至上一页
			return redirect(reverse("ptindex",args=(pt,)))
	except:
		return render(request,"watchadmin/info.html",{"info":"删除失败"})

#后台用户编辑信息表
def typesedit(request,uid):
	tp=Types.objects.get(id=uid)
	context={"type":tp}
	return render(request,"watchadmin/types/edit.html",context)

#后台用户提交数据到数据库
def typesupdate(request):
	try:
		tp=Types.objects.get(id=request.POST["sid"])
		tp.name=request.POST["name"]
		#修改后保存
		tp.save()
		return render(request,'watchadmin/info.html',{"info":"修改成功"})
	except:
		return render(request,'watchadmin/info.html',{"info":"修改失败"})




#分页显示商品信息
def pgindex(request,pIndex):
	#声明全局变量，在删除信息时使用
	global pg
	pg=request.path[19:]
	#print(request.path)
	li=Goods.objects.all()
	#在页面中显示格式化之后的信息
	for good in li:
		t=Types.objects.get(id=good.typeid)
		good.typeid=t.name
		good.addtime=time.strftime("%Y-%m-%d",time.localtime(good.addtime))
		# %H:%M:%S
	#分页
	p1=Paginator(li,6)
	if pIndex=="":
		pIndex="1"
	p=p1.page(int(pIndex))
	return render(request,'watchadmin/goods/index.html',{"p":p,"lip":p1.page_range})

#后台添加商品类别的form表单
def goodsadd(request):
	#线获取所有的数据
	tp=Types.objects.all()
	#构建一个新列表，放入级别最低的商品类别。用于在下拉框中显示
	goodslist=[]
	for one in tp:
		length=len(one.path.split(","))
		if length==4:
			goodslist.append(one)

	context={"goodslist":goodslist}
	return render(request,'watchadmin/goods/add.html',context)

#后台将数据插入表格
def goodsinsert(request):
	try:
	#判断图片是否上传，且进行缩放
		pic=request.FILES.get("picname",None)
		#如果没有上传成功
		if not pic:
			return render(request,'watchadmin/info.html',{"info":"没有图片信息,请上传图片"})
		#为了不使图片发生冲突，使用时间戳命名图片
		picname=str(time.time())+"."+pic.name.split(".").pop()
		destination=open(os.path.join("./static/goodsimg",picname),"wb+")
		for chunk in pic.chunks():
			#将原始图片保存
			destination.write(chunk)
		destination.close()
		#缩放图片
		#首先获取原图
		img=Image.open("./static/goodsimg/"+picname)
		#分别以以下大小和格式保存
		#商品详情页大图
		img.thumbnail((305,440.28))
		img.save("./static/goodsimg/x_"+picname)
		#商品列表页
		img.thumbnail((125,200))
		img.save("./static/goodsimg/m_"+picname)
		#商品购物车
		img.thumbnail((82,117))
		img.save("./static/goodsimg/s_"+picname)

		#添加商品
		goods=Goods()
		goods.typeid=request.POST["typeid"]
		goods.goods=request.POST["goods"]
		goods.company=request.POST["company"]
		goods.price=request.POST["price"]
		goods.picname=picname
		goods.state=request.POST["state"]
		goods.store=request.POST["store"]
		goods.descr=request.POST["descr"]
		goods.addtime=time.time()
		goods.save()
		context={"info":"添加成功"}
		return render(request,'watchadmin/info.html',context)
	except:
		context={"info":"添加失败"}
		return render(request,'watchadmin/info.html',context)

#后台删除数据
def goodsdel(request,gid):
	try:
		good=Goods.objects.get(id=gid)
		#删除时，将图片也删除
		os.remove("./static/goodsimg/"+good.picname)
		os.remove("./static/goodsimg/x_"+good.picname)
		os.remove("./static/goodsimg/m_"+good.picname)
		os.remove("./static/goodsimg/s_"+good.picname)
		good.delete()
		return redirect(reverse("pgindex",args=(pt,)))
	except:
		return render(request,"watchadmin/info.html",{"info":"删除失败"})

#后台用户编辑信息表
def goodsedit(request,gid):
	good=Goods.objects.get(id=gid)
	tp=Types.objects.all()
	#构建一个新列表，放入级别最低的商品类别。用于在下拉框中显示
	goodslist=[]
	for one in tp:
		length=len(one.path.split(","))
		if length==4:
			goodslist.append(one)
	good.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(good.addtime))
	context={"good":good,"goodslist":goodslist}
	return render(request,"watchadmin/goods/edit.html",context)

#后台用户提交数据到数据库
def goodsupdate(request,gid):
	#定义一个函数，减少代码冗余
	def a(request):
		goods.typeid=request.POST["typeid"]
		goods.goods=request.POST["goods"]
		goods.company=request.POST["company"]
		goods.price=request.POST["price"]
		goods.state=request.POST["state"]
		goods.store=request.POST["store"]
		goods.descr=request.POST["descr"]
		goods.save()
	try:
		goods=Goods.objects.get(id=gid)
		oldpicname=goods.picname
		pic=request.FILES.get("picname",None)
		if not pic:
			#调用函数
			a(request)
			return render(request,'watchadmin/info.html',{"info":"修改成功"})
		else:
			os.remove("./static/goodsimg/"+oldpicname)
			os.remove("./static/goodsimg/x_"+oldpicname)
			os.remove("./static/goodsimg/m_"+oldpicname)
			os.remove("./static/goodsimg/s_"+oldpicname)
			#为了不使图片发生冲突，使用时间戳命名图片
			picname=str(time.time())+"."+pic.name.split(".").pop()
			destination=open(os.path.join("./static/goodsimg",picname),"wb+")
			for chunk in pic.chunks():
				#将原始图片保存
				destination.write(chunk)

			destination.close()
			#缩放图片
			#首先获取原图
			img=Image.open("./static/goodsimg/"+picname)
			#分别以以下大小和格式保存
			#商品详情页大图
			img.thumbnail((305,440.28))
			img.save("./static/goodsimg/x_"+picname)
			#商品列表页
			img.thumbnail((125,200))
			img.save("./static/goodsimg/m_"+picname)
			#商品购物车
			img.thumbnail((82,117))
			img.save("./static/goodsimg/s_"+picname)
			goods.picname=picname
			a(request)
			return render(request,'watchadmin/info.html',{"info":"修改成功"})
	except:
		pic=request.FILES.get("picname",None)
		if pic:
			os.remove("./static/goodsimg/"+picname)
			os.remove("./static/goodsimg/x_"+picname)
			os.remove("./static/goodsimg/m_"+picname)
			os.remove("./static/goodsimg/s_"+picname)
			return render(request,'watchadmin/info.html',{"info":"图片修改失败"})
		return render(request,'watchadmin/info.html',{"info":"修改失败"})

#上传放大镜图片
def magni(request,gid):
	#首先获取一个magni对象
	magni=Magn()
	magni.goodsid=gid
	pic=request.FILES.get("picname",None)
	#为了不使图片发生冲突，使用时间戳命名图片
	picname=str(time.time())+"."+pic.name.split(".").pop()
	destination=open(os.path.join("./static/magnimg",picname),"wb+")
	for chunk in pic.chunks():
		#将原始图片保存
		destination.write(chunk)
	destination.close()
	magni.picname=picname
	magni.save()
	return redirect(reverse('admin_goodsedit',args=(gid,)))


#查看评论
def contents(request,pIndex,gid):
	global pc
	pc=request.path[21:]
	#print(pc)
	#print(request.path)
	lc=Contents.objects.filter(goodsid=gid)
	#在页面中显示格式化之后的信息
	for content in lc:
		content.addtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(content.addtime))
	#分页
	p1=Paginator(lc,12)
	if pIndex=="":
		pIndex="1"
	p=p1.page(int(pIndex))
	return render(request,'watchadmin/goods/contents.html',{"p":p,"lip":p1.page_range,"gid":gid})

#删除评论
def adelcontents(requset,gid):
	content=Contents.objects.get(id=gid)
	content.delete()
	return redirect(reverse("admin_contents",args=(1,pc,)))