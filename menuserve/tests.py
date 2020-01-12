
import time

from django.test import TestCase,LiveServerTestCase
from menuserve.models import Food,Chart,List,store
from django.contrib.auth.models import User,Group

from selenium import webdriver

# Unit model Test
class testFood(TestCase):    
    def test_food_add(self):
        newfood = Food(name='testfood',price='0',intro='testintro')
        newfood.save()
        food = Food.objects.get(name='testfood')
        self.assertIsNotNone(food)
    
    def test_food_attribute(self):
        newfood = Food.objects.get(name='testfood')
        self.assertEqual("testfood",newfood.name)
        self.assertEqual("0",newfood.price)
        self.assertEqual("testintro",newfood.intro)
    
    def test_food_delete(self):
        newfood = Food.objects.get(name='testfood')
        newfood.delete()
        food = Food.objects.filter(name='testfood')
        self.assertIsNone(food)


class testChart(TestCase):
    def test_chart_add(self):
        newfood = Chart(name='testfood',price='0',num=0)
        newfood.save()
        food = Chart.objects.get(name='testfood')
        self.assertIsNotNone(food)

    def test_chart_modify(self):
        food = Chart.objects.get(name='testfood')
        food.name = 'testchange'
        food.price = '1'
        food.num += 1
        food.save()
        self.assertEqual("testchange",food.name)
        self.assertEqual("1",food.price)
        self.assertEqual(1,food.num)
    
    def test_chart_delete(self):
        food = Chart.objects.get(name='testchange')
        food.delete()
        food = Chart.objects.filter(name='testchange')
        self.assertIsNone(food)


class testList(TestCase):
    def test_List_add(self):
        newlist = List(name='testlist',user='test',food='test',status='tobe')
        newlist.save()
        list = List.objects.get(name='testlist')
        self.assertIsNotNone(list)

    def test_List_modify(self):
        list = List.objects.get(name='testlist')
        list.name = 'testchange'
        list.status = 'done'
        list.save()
        self.assertEqual("testchange",list.name)
        self.assertEqual("done",list.status)
    
    def test_List_delete(self):
        list = List.objects.get(name='testchange')
        list.delete()
        list = List.objects.filter(name='testchange')
        self.assertIsNone(list)


class testUser(TestCase):
    def test_user_add(self):
        newuser = User(username='testuser',password='test')
        newuser.save()
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)

    def test_user_add_group(self):
        group = Group.objects.get(name='customer')
        user = User.objects.get(username='testuser')
        user.group.add(group)
        self.assertEqual("customer",user.group.first.name)
    
    def test_user_modify_passw(self):
        user = User.objects.get(username='testuser')
        user.password='testchange'
        user.save()
        self.assertEqual("testchange",user.password)
    
    def test_user_delete(self):
        user = User.objects.get(username='testuser')
        user.delete()
        user = User.objects.filter(username='testuser')
        self.assertIsNone(user)


class testStore(TestCase):
    def test_store_add(self):
        newstore = store(name='teststore')
        newstore.save()
        s = store.objects.get(name='teststore')
        self.assertIsNotNone(s)

    def test_store_add_member(self):
        s = store.objects.get(name='teststore')
        newuser = User(username='teststore',password='test')
        newuser.save()
        s.member.add(newuser)
        self.assertEqual("teststore",s.member.first.name)
        user = User.objects.get(username='teststore')
        user.delete()

    def test_store_delete(self):
        s = store.objects.get(name='teststore')
        s.delete()
        s = store.objects.filter(name='teststore')
        self.assertIsNone(s)


# Selenuim Test
class HighLevelTest(LiveServerTestCase):
    def setup(self):
        self.dr = webdriver.Chrome('/usr/local/bin/chromedriver') 
    
    # register page
    def register(self):
        self.dr.get('http://www.google.com/')  ####
        self.dr.find_elements_by_id("information").firstChild().send_keys("test")
        self.dr.find_elements_by_id("information").lastChild().send_keys("test")
        self.dr.find_elements_by_tag_name("input").click()
        time.sleep(3)
        self.assertIsNone(self.dr.find_element_by_id("signin"))  

    # order_food, order_submission_successfully pages
    def order_to_chart(self):
        self.dr.get('http://www.google.com/')   ##
        # Add food to cart
        original = len(self.dr.find_elements_by_tag_name("li"))
        self.dr.find_element_by_id("add").click()
        time.sleep(3)
        after=len(self.dr.find_elements_by_tag_name("li"))
        self.assertEquals(after,original+1)
        # Delete food from cart
        self.dr.find_element_by_id("minus").click()
        time.sleep(3)
        ul=len(self.dr.find_elements_by_tag_name("li"))
        self.assertEquals(ul,original)
        # Submit order
        self.dr.find_element_by_id("submit").click()
        time.sleep(3)
        s = self.dr.find_elements_by_id("success")
        self.assertIsNotNone(s)

    def log_out(self):
        self.dr.find_element_by_id("logout").click()
        time.sleep(3)
        self.assertIsNotNone(self.dr.find_element_by_id("signin"))
    
    # login page
    def login_manager(self):
        self.dr.find_element_by_id("signin").click()
        time.sleep(3)
        self.dr.find_elements_by_id("information").firstChild().send_keys("xinyanzh")
        self.dr.find_elements_by_id("information").lastChild().send_keys("Woshihabao97020*")
        self.dr.find_elements_by_tag_name("input").click()
        time.sleep(3)
        self.assertIsNone(self.dr.find_element_by_id("signin")) 

    # menu_management, manu_edit pages
    def edit_menu(self):
        self.dr.get('http://www.google.com/')   ####
        number = len(self.dr.find_elements_by_id("food"))
        # add food
        self.dr.find_element_by_id("add").click()
        time.sleep(3)
        self.assertEquals(len(self.dr.find_elements_by_id("food")),number+1)
        # delete food
        self.dr.find_element_by_id("delete").click()
        time.sleep(3)
        self.assertEquals(len(self.dr.find_elements_by_id("food")),number)
        # edidt food -> menue_edit page
        self.dr.find_element_by_id("edit").click()
        time.sleep(3)
        url = self.dr.current_url
        self.assertEquals('thank you so much !!',url)    ###
        self.dr.find_element_by_id("information").send_keys("testfood")
        self.dr.find_element_by_tag_name("input").click()

    # staff_management, store_edit pages
    def edit_storestaff(self):
        # change roles between customers, employers and managers
        self.dr.get('http://www.google.com/')    ###
        employer_num = len(self.dr.find_elements_by_id("employer"))
        manager_num = len(self.dr.find_elements_by_id("manager"))
        self.dr.find_element_by_id("cte").click()
        time.sleep(4)
        self.assertEquals(len(self.dr.find_elements_by_id("employer")),employer_num+1)
        self.dr.find_element_by_id("etm").click()
        time.sleep(4)
        self.assertEquals(len(self.dr.find_elements_by_id("manager")),manager_num+1)
        # add/delete store
        store_num = self.dr.find_elements_by_id("store")
        self.dr.find_element_by_id("addstore").click()
        time.sleep(3)
        self.assertEquals(self.dr.find_elements_by_id("store"),store_num+1)
        self.dr.find_element_by_id("deletestore").click()
        time.sleep(3)
        self.assertEquals(self.dr.find_elements_by_id("store"),store_num)
        # assign or delete managers/employers to or from certain store
        self.dr.find_element_by_id("addstore").click()
        time.sleep(3)
        self.dr.find_element_by_id("addms").click()
        time.sleep(3)
        self.assertIsNotNone(self.dr.find_element_by_id("hasmanager")) 
        self.dr.find_element_by_id("deletems").click()
        time.sleep(3)
        self.assertIsNone(self.dr.find_elements_by_id("hasmanager")) 
        self.dr.find_element_by_id("addes").click()
        time.sleep(3)
        self.assertIsNotNone(self.dr.find_elements_by_id("hasemployee"))
        self.dr.find_element_by_id("deletees").click()
        time.sleep(3)
        self.assertIsNone(self.dr.find_elements_by_id("hasemployee"))

    # fullfil orders page
    def see_fullfill_orders(self):
        self.dr.get('http://www.google.com/')    #####
        done_num = len(self.dr.find_elements_by_id("donenum"))
        todo_num = len(self.dr.find_elements_by_id("tobenum"))
        if todo_num:
            self.dr.find_element_by_id("done").click()
            time.sleep(3)
            self.assertEquals(len(self.dr.find_elements_by_id("donenum")),done_num+1)

    def logout(self):
        self.dr.find_element_by_id("logout").click()
        time.sleep(3)
        self.assertIsNotNone(self.dr.find_elements_by_id("signin"))








        


