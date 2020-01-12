"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from menuserve import views
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.menu,name='main'),
    path('menu_management/',views.menu_management,name='edit'),
    path('order/',views.order,name='order'),
    path('order-list/',views.order_list,name='order-list'),
    path('customer-orders/',views.customer_orders,name='customer-orders'),
    path('staff/',views.staff,name='staff'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('menu-edit/<id>/',views.menuedit,name='menuedit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

