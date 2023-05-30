from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from razorpay_integration import views as vr
from django.urls import path
# from .views import uploadDocument

urlpatterns = [
    path("uploadDocument/", views.uploadDocument, name="uploadDocument"),
    path("allDocument/", views.allDocument, name="allDocument"),
    path("yourDocument/", views.yourDocument, name="yourDocument"),
    path("razorpay/", vr.home1, name="razorpay_integration"),
    
]