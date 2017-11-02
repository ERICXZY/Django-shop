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
from . import views,viewsgoods,viewsorders
urlpatterns = [
	#为什么要这样写？
    url(r'^$',views.index,name='admin_index'),
    
    #定义后台登陆路由
    url(r'^admin$',views.adminlogin,name='admin_login'),
    #后台登入路由
    url(r'^login$',views.doadminlogin,name='doadmin_login'),
    #后台登出
    url(r'^logout$',views.logout,name='logout'),

    #用户管理
    #url(r'^users$',views.usersindex,name='admin_usersindex'),
    #分页显示用户首页
    url(r'^pag(?P<pIndex>[0-9]*)$',views.pagTest,name='pagTest'),
    #添加会员的表单
    url(r'^usersadd$',views.usersadd,name='admin_usersadd'),
    #添加会员
    url(r'^usersinsert$',views.usersinsert,name='admin_usersinsert'),
    #删除会员
    url(r'^usersdel/(?P<uid>[0-9]+)$',views.usersdel,name='admin_usersdel'),
    #编辑表单
    url(r'^usersedit/(?P<uid>[0-9]+)$',views.usersedit,name='admin_usersedit'),
    #编辑的信息提交到数据库
    url(r'^usersupdate$',views.usersupdate,name='admin_usersupdate'),


    #商品类别管理
    url(r'^ptindex(?P<pIndex>[0-9]*)$',viewsgoods.ptindex,name='ptindex'),
    #添加商品的表单
    url(r'^typesadd/(?P<tid>[0-9]*)$',viewsgoods.typesadd,name='admin_typesadd'),
    #添加商品
    url(r'^typesinsert$',viewsgoods.typesinsert,name='admin_typesinsert'),
    #删除商品
    url(r'^typesdel/(?P<uid>[0-9]+)$',viewsgoods.typesdel,name='admin_typesdel'),
    #编辑商品
    url(r'^typesedit/(?P<uid>[0-9]+)$',viewsgoods.typesedit,name='admin_typesedit'),
    #编辑的信息提交到数据库
    url(r'^typesupdate$',viewsgoods.typesupdate,name='admin_typesupdate'),

    #商品信息管理
    url(r'^pgindex(?P<pIndex>[0-9]*)$',viewsgoods.pgindex,name='pgindex'),
    #添加商品的表单
    url(r'^goodsadd$',viewsgoods.goodsadd,name='admin_goodsadd'),
    #添加商品
    url(r'^goodsinsert$',viewsgoods.goodsinsert,name='admin_goodsinsert'),
    #删除商品
    url(r'^goodsdel/(?P<gid>[0-9]+)$',viewsgoods.goodsdel,name='admin_goodsdel'),
    #编辑商品
    url(r'^goodsedit/(?P<gid>[0-9]+)$',viewsgoods.goodsedit,name='admin_goodsedit'),
    #编辑的信息提交到数据库
    url(r'^goodsupdate/(?P<gid>[0-9]+)$',viewsgoods.goodsupdate,name='admin_goodsupdate'),
    #查看商品评论
    url(r'^contents(?P<pIndex>[0-9]*)/(?P<gid>[0-9]+)$',viewsgoods.contents,name='admin_contents'),
    #删除评论
    url(r'^delcontents/(?P<gid>[0-9]+)$',viewsgoods.adelcontents,name='admin_delcontents'),
    #添加放大镜图片
    url(r'^magni/(?P<gid>[0-9]+)$',viewsgoods.magni,name='magni'),


    #商品订单管理
    url(r'^poindex(?P<pIndex>[0-9]*)$',viewsorders.poindex,name='poindex'),
    #显示订单详情
    url(r'^detail/(?P<oid>[0-9]+)$',viewsorders.detail,name='admin_delcontents'),
    #修改订单状态
    url(r'^send/(?P<sid>[0-9]+)$',viewsorders.send,name='admin_send'),
    url(r'^cancel/(?P<sid>[0-9]+)$',viewsorders.cancel,name='admin_cancel'),

]
