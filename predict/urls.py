from django.urls import path, re_path
from . import views

urlpatterns = [
    path('index', views.index),
    # 숫자, 영문, 한글, ., -
    re_path('download/([0-9a-zA-Zㄱ-힣.-]+)', views.download),
    path('downlist', views.downlist),
 
    
]