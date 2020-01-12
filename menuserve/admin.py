from django.contrib import admin
from menuserve.models import Food,Chart,List, store,user
from django.contrib.auth.models import User

# Register your models here.
admin.site.register([Food,Chart,List,store,user])