"""vending URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import (create_vendingMachine,
                    edit_vendingMachine,
                    delete_vendingMachine,
                    list_vendingMachine,
                    add_item,
                    edit_item,
                    delete_item,
                    list_items,
                    list_time)

urlpatterns = [
    path('vendingMachine/create/', create_vendingMachine, name='create_vendingMachine'),
    path('vendingMachine/edit/', edit_vendingMachine, name='edit_vendingMachine'),
    path('vendingMachine/delete/', delete_vendingMachine, name='delete_vendingMachine'),
    path('vendingMachine/list/', list_vendingMachine, name='list_vendingMachine'),
    path('stock/add/', add_item, name='add_item'),
    path('stock/edit/', edit_item, name='edit_item'),
    path("stock/delete/", delete_item, name="delete_item"),
    path("stock/list/", list_items, name="list_items"),
    path("time/list/", list_time, name="list_time"),
    path('admin/', admin.site.urls),

]
