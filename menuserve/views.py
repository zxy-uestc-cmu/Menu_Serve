from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect,HttpResponse
from menuserve.models import Food,Chart,List,user,store
from menuserve.Forms import FoodForm,RegisterForm,LoginForm
from django.contrib import auth
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def menu(request):
    if request.POST and 'signout' in request.POST:
        auth.logout(request)
    if request.POST and 'add' in request.POST:
        newfood = Food(name='None',intro='none',price='0')
        newfood.save()
    cxt = {}
    s = store.objects.all()
    food = Food.objects.all()
    cxt['store'] = s
    cxt['food'] = food
    return render(request, "Menu.html", cxt)

@login_required
def menu_management(request):  
    if request.user.groups.first().name != 'manager':
        return HttpResponseRedirect(reverse('main')) 
    cxt = {}
    s = store.objects.all()
    food = Food.objects.all()
    cxt['food'] = food
    cxt['store'] = s
    if request.POST and 'add' in request.POST:  
        newfood = Food(name='none',price='0',intro='none')
        newfood.save()
    if request.POST and 'delete' in request.POST:
        id = request.POST['item']
        deletefood = Food.objects.get(id=id)
        deletefood.delete()
    if request.POST and 'edit' in request.POST:
        i = request.POST['item']
        return redirect(reverse('menuedit', args=[i]))
    return render(request, "Menu_Management.html", cxt)

@login_required
def menuedit(request,id): 
    if request.user.groups.first().name != 'manager':
        return HttpResponseRedirect(reverse('main'))  
    item = Food.objects.get(id=id)
    dic = {'image':item.image,'name':item.name,'price':item.price,'intro':item.intro}
    form = FoodForm(dic)
    if request.POST and 'comfirm' in request.POST:
        form = FoodForm(request.POST,request.FILES,instance=item)
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect(reverse('edit'))
    cxt = {}
    cxt['id'] = id
    cxt['item'] = item
    cxt['form'] = form
    return render(request, "Menu_Edit.html", cxt)

@login_required
def order(request):
    if request.user.groups.first().name != 'customer':
        return HttpResponseRedirect(reverse('main')) 
    cxt = {}
    s = store.objects.first()
    cxt['s']= s
    if request.POST:   
        if 'selects' in request.POST:
            selects = store.objects.get(id=request.POST['sid'])
            cxt['s'] = selects
        elif 'submit_order' in request.POST:
            s = ''    
            for i in Chart.objects.all():
                s += str(i.num) +' * ' + i.name + ',' + " "
            s = s[:-2]
            Chart.objects.all().delete()
            storename = store.objects.get(id=request.POST['sid'])
            neworder = List(foods=s,name=storename.name,user=request.user.username,status='tobe')
            neworder.save()
            return render(request,"Succeess.html",cxt)
        else:
            #cxt['s'] = store.objects.get(id=request.POST['currents'])
            res = {}
            id = request.POST['id']
            name = Food.objects.get(id=id).name 
            filter = Chart.objects.filter(name=name) 
            if 'add'==request.POST['op']:
                price = Food.objects.get(id=id).price
                if len(filter)==0:    
                    item = Chart(name=name,price=price,num=1)
                else:  
                    item = Chart.objects.get(name=name)
                    item.num += 1
                    item.price = str(float(price)+float(item.price))
                item.save()
                res = {'food':name,'num':item.num,'price':item.price,'op':'add'}
                return HttpResponse(json.dumps(res))
            if 'minus'==request.POST['op']:
                if len(filter)>0:
                    item = Chart.objects.get(name=name)
                    if item.num == 1:
                        item.delete()
                        res = {'food':name,'num':0,'price':0}
                    else:
                        price = Food.objects.get(id=id).price
                        item.num -= 1  
                        item.price = str(float(item.price)-float(price))        
                        item.save() 
                        res = {'food':name,'num':item.num,'price':item.price,'op':'minus'}
                return HttpResponse(json.dumps(res))
            if 'delete'==request.POST['op']:
                if len(filter)>0:
                    item = Chart.objects.get(name=name)
                    item.delete()  
                    res = {'food':name,'num':0,'price':0,'op':'delete'}
                return HttpResponse(json.dumps(res))
            return HttpResponse(json.dumps(res))  
    ss = store.objects.all()
    cxt['store'] = ss   
    cart = Chart.objects.all()
    food = Food.objects.all()
    cxt['food'] = food
    cxt['cart'] = cart
    return render(request,"Order_Submit.html",cxt)

@login_required
def order_list(request):
    if (request.user.groups.first().name != 'manager') and (request.user.groups.first().name != 'employee'):
        return HttpResponseRedirect(reverse('main')) 
    if request.POST and 'update' in request.POST:
        s = request.POST['store']
        ltobe = List.objects.filter(name=s).filter(status='tobe')
        ldone = List.objects.filter(name=s).filter(status='done')
        res = {'ltobe':{},'ldone':{}}
        for i in ltobe:
            res['ltobe'][i.id]={'user':i.user,'food':i.foods}
        for i in ldone:
            res['ldone'][i.id]={'user':i.user,'food':i.foods}
        return HttpResponse(json.dumps(res))
    cxt={}
    first= request.user.store.first()   
    if not first:
        s= request.user.store.all()
        cxt['store'] = s
        return render(request,"Order_List.html",cxt)
    ltobe = List.objects.filter(name=first.name).filter(status='tobe')
    ldone = List.objects.filter(name=first.name).filter(status='done')
    cxt['currentstore']=first
    if request.POST and 'store' in request.POST:
        selects = store.objects.get(id=request.POST['sid'])
        cxt['currentstore'] = selects
        ltobe = List.objects.filter(name=selects.name).filter(status='tobe')
        ldone = List.objects.filter(name=selects.name).filter(status='done')
    if request.POST and 'done' in request.POST:
        id = request.POST['item']
        order = List.objects.get(id = id)
        order.status = 'done'
        order.save()
        currents = store.objects.get(id=request.POST['sid'])
        ltobe = List.objects.filter(name=currents.name).filter(status='tobe')
        ldone = List.objects.filter(name=currents.name).filter(status='done')
        cxt['currentstore'] = currents
    s= request.user.store.all()
    cxt['store'] = s
    cxt['list_tobe'] = ltobe
    cxt['list_done'] = ldone
    return render(request,"Order_List.html",cxt)

@login_required
def customer_orders(request):
    if request.user.groups.first().name != 'customer':
        return HttpResponseRedirect(reverse('main')) 
    cxt={}  
    tobe = List.objects.filter(user=request.user.username).filter(status='tobe')
    done = List.objects.filter(user=request.user.username).filter(status='done')
    cxt['tobe'] = tobe
    cxt['done'] = done
    return render(request,"your-orders.html",cxt)

@login_required
def staff(request):
    if (not request.user.groups.first()) or request.user.groups.first().name != 'manager':
        return HttpResponseRedirect(reverse('main')) 
    groupm = Group.objects.get(name='manager')
    groupe = Group.objects.get(name='employee')
    groupc = Group.objects.get(name='customer')
    if request.POST and 'id' in request.POST: 
        user = User.objects.get(id=request.POST['id'])
    if request.POST and 'sid' in request.POST: 
        s = store.objects.get(id=request.POST['sid'])
    if request.POST and 'addstore' in request.POST:
        newstore = store(name='Store_Name')
        newstore.save()
    if request.POST and 'deletestore' in request.POST:
        s.delete()   
    if request.POST and 'storename' in request.POST:
        s.name = request.POST['storen']
        s.save()
    if request.POST and 'deleteme' in request.POST:  
        s.member.remove(user)    
    if request.POST and 'adds' in request.POST:
        s.member.add(user)
    if request.POST and 'changeme' in request.POST:
        user.groups.remove(groupm)
        user.groups.add(groupe)
    if request.POST and 'changemc' in request.POST:
        user.groups.remove(groupm)
        user.groups.add(groupc)
    if request.POST and 'changecm' in request.POST:
        user.groups.remove(groupc)
        user.groups.add(groupm)
    if request.POST and 'changece' in request.POST:
        user.groups.remove(groupc)
        user.groups.add(groupe)
    if request.POST and 'changeem' in request.POST:
        user.groups.remove(groupe)
        user.groups.add(groupm)
    if request.POST and 'changeec' in request.POST:
        user.groups.remove(groupe)
        user.groups.add(groupc)
    cxt = {}
    s = store.objects.all()
    m = User.objects.filter(groups=groupm)
    e = User.objects.filter(groups=groupe)
    c = User.objects.filter(groups=groupc)
    #cf = User.objects.filter(groups=groupc)
    cxt['store'],cxt['employ'],cxt['manager'],cxt['customer'] = s,e,m,c
    #cxt['customer_front'] =cf
    return render(request,"staff.html",cxt)

def register(request):
    form = RegisterForm()
    if request.POST and 'comfirm' in request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid(): 
            form.save()
            thisuser = User.objects.get(username=request.POST['username'])
            group = Group.objects.get(name='customer')
            thisuser.groups.add(group)
            auth.login(request, thisuser)
            return HttpResponseRedirect(reverse('main'))
    cxt = {}
    cxt['form']=form
    return render(request,"register.html",cxt)

def login(request):    
    cxt = {}
    form = LoginForm()
    if request.POST and 'comfirm' in request.POST:     
        form = LoginForm(request.POST)
        if form.is_valid(): 
            nowuser = auth.authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if nowuser:
                auth.login(request, nowuser)
                return HttpResponseRedirect(reverse('main'))
            else:
                error = 'Wrong username, or wrong password!'
                cxt['error']=error      
    cxt['form']=form
    return render(request,"login.html",cxt)





