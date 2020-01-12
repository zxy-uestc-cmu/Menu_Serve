from django.db import models
from django.contrib.auth.models import User 

class Food(models.Model):
    image = models.ImageField(upload_to='./',null=True,blank=True)
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=20)
    intro = models.CharField(max_length=200)

#class allcart(models.Model):
#    storename = models.CharField(max_length=50)
#    amount = models.CharField(max_length=50)

class Chart(models.Model):
    name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    num = models.IntegerField(default=0)

class List(models.Model):
    name = models.CharField(max_length=50)
    foods = models.CharField(max_length=500)
    user = models.CharField(max_length=50,default=None)
    status = models.CharField(max_length=50,default='tobe')

class store(models.Model):
    member = models.ManyToManyField(User,blank=True,null=True,related_name='store')
    name = models.CharField(max_length=120)

class user(models.Model):
    name = models.CharField(max_length=50)




