from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    #path("admin/", admin.site.urls),
    path("base/", views.home1, name="home"),
    path("payment/", views.order_payment, name="payment"),
    path("callback/", views.callback, name="callback"),
]

