"""axfhz1805 URL Configuration

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
from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^home/', views.home, name="home"),
    url(r'^market/', views.market, name="market"),
    url(r'^marketWithParam/(\d+)/(\d+)/(\d+)', views.marketWithParam, name="marketWithParam"),
    url(r'^cart/', views.cart, name="cart"),
    url(r'^mine/', views.mine, name="mine"),
    url(r'^register/', views.register, name="register"),
    url(r'^checkUserUnique/', views.checkUserUnique, name="checkUserUnique"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^addToCart/', views.addToCart, name="addToCart"),
    url(r'^subToCart/', views.subToCart, name="subToCart"),
    url(r'^addCart/', views.addCart, name="addCart"),
    url(r'^subCart/', views.subCart, name="subCart"),
    url(r'^changeSelectStatu/', views.changeSelectStatu, name="changeSelectStatu"),
    url(r'^changeManySelectStatu/', views.changeManySelectStatu, name="changeManySelectStatu"),
    url(r'^createOrder/', views.createOrder, name="createOrder"),
    url(r'^orderInfo/(.+)', views.orderInfo, name="orderInfo"),
    url(r'^changeOrderStatus/', views.changeOrderStatus, name="changeOrderStatus"),
]
