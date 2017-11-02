from django.db import models

# Create your models here.

class Users(models.Model):
	username=models.CharField(max_length=32,unique=True)
	name=models.CharField(max_length=16)
	password=models.CharField(max_length=32)
	sex=models.IntegerField()
	address=models.CharField(max_length=255)
	#定长的字串怎么写
	code=models.CharField(max_length=6)
	phone=models.CharField(max_length=16)
	email=models.CharField(max_length=50)
	state=models.IntegerField(default=1)
	addtime=models.IntegerField()


class Types(models.Model):
	name=models.CharField(max_length=32)
	pid=models.IntegerField(default=0)
	path=models.CharField(max_length=255)

class Goods(models.Model):
    typeid=models.IntegerField()
    goods=models.CharField(max_length=32)
    company=models.CharField(max_length=50)
    descr=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    picname=models.CharField(max_length=255)
    state=models.IntegerField(default=1)
    store=models.IntegerField(default=0)
    num=models.IntegerField(default=0)
    clicknum=models.IntegerField(default=0)
    addtime=models.IntegerField()
    
class Orders(models.Model):
	uid=models.IntegerField()
	linkman=models.CharField(max_length=32)
	address=models.CharField(max_length=255)
	code=models.CharField(max_length=6)
	phone=models.CharField(max_length=16)
	addtime=models.IntegerField()
	total=models.DecimalField(max_digits=8,decimal_places=2)
	state=models.IntegerField()

class Detail(models.Model):
	orderid=models.IntegerField()
	goodsid=models.IntegerField()
	name=models.CharField(max_length=32)
	price=models.DecimalField(max_digits=6,decimal_places=2)
	num=models.IntegerField()

class Contents(models.Model):
	uid=models.IntegerField()
	goodsid=models.IntegerField()
	username=models.CharField(max_length=20)
	content=models.TextField()
	addtime=models.IntegerField()
	
class Magn(models.Model):
	goodsid=models.IntegerField()
	picname=models.CharField(max_length=255)
