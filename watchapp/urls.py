"""watchproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views,viewsorders,viewsusers
urlpatterns = [
	#网站首页，商品列表，详情
    url(r'^$',views.index,name='index'),
    url(r'^products(?P<pIndex>[0-9]*)$',views.products,name='products'),
    url(r'^products(?P<pIndex>[0-9]*)/(?P<pid>[0-9]*)$',views.products,name='products'),
    url(r'^single/(?P<pid>[0-9]+)$',views.single,name='single'),
    #客户端评论处理
    url(r'^contents/(?P<pid>[0-9]+)$',views.contents,name='contents'),
    #客户端删除评论
    url(r'^delcontents/(?P<pid>[0-9]+)$',views.delcontents,name='delcontents'),
    #商品推介


    #会员相关操作
    #会员登录成功时，留在当前页面
    url(r'^account$',viewsusers.account,name='account'),
    #登录状态保持
    url(r'^doaccount$',viewsusers.doaccount,name='doaccount'),
    #会员登出
    url(r'^outaccount$',viewsusers.outaccount,name='outaccount'),
    #会员注册页面
    url(r'^register$',viewsusers.register,name='register'),
    #会员注册提交的URL。并让其重新登录
    url(r'^doregister$',viewsusers.doregister,name='doregister'),
    #会员信息修改
    url(r'^update/(?P<uid>[0-9]+)$',viewsusers.update,name='update'),
    #执行修改操作
    url(r'^doupdate/(?P<uid>[0-9]+)$',viewsusers.doupdate,name="doupdate"),
    #个人中心
    url(r'^member$',viewsusers.member,name='member'),



    #购物车和订单处理
    url(r'^checkout$',viewsorders.checkout,name='checkout'),
    url(r'^docheckout/(?P<sid>[0-9]+)$',viewsorders.docheckout,name="docheckout"),
    url(r'^delcheckout/(?P<sid>[0-9]+)$',viewsorders.delcheckout,name="delcheckout"),
    url(r'^clearcheckout$',viewsorders.clearcheckout,name="clearcheckout"),
    url(r'^dcheckout/(?P<sid>[0-9]+)$',viewsorders.dcheckout,name="dcheckout"),
    url(r'^acheckout/(?P<sid>[0-9]+)$',viewsorders.acheckout,name="acheckout"),

    #特定的订单信息填写页
    url(r'^showorder$',viewsorders.showorder,name='showorder'),
    url(r'^order$',viewsorders.order,name='order'),
    url(r'^delorder/(?P<sid>[0-9]+)$',viewsorders.delorder,name='delorder'),
    url(r'^clearorder$',viewsorders.clearorder,name='clearorder'),
    #特定的订单信息确认页
    url(r'^orderconfirm$',viewsorders.orderconfirm,name='orderconfirm'),
    #将订单信息添加到数据库中,并跳转到个人订单页
    url(r'^orderadd$',viewsorders.orderadd,name='orderadd'),
    #订单页
    url(r'^orderlist$',viewsorders.orderlist,name='orderlist'),
    #订单状态页
    url(r'^orderlist/(?P<sid>[0-9]+)$',viewsorders.orderlist,name='orderlist'),
    #订单详情页
    url(r'^detail/(?P<sid>[0-9]+)$',viewsorders.detail,name='detail'),
    #客户端将订单改为已收货
    url(r'^receive/(?P<sid>[0-9]+)$',viewsorders.receive,name='receive'),
    #客户端将订单改为取消
    url(r'^cancel/(?P<sid>[0-9]+)$',viewsorders.cancel,name='cancel'),
   


   






    #其他官方博客，联系我们
    url(r'^contact$',views.contact,name='contact'),
    url(r'^typo$',views.typo,name='typo'),




]
