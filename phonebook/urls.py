from django.urls import path, re_path
from . import views

# namespace
app_name = 'PB'

urlpatterns = [
    re_path(r'index/([0-9]+)', views.index, name="I"),
    path('add/', views.add, name="A"),
    re_path(r'delete/([0-9]+)', views.delete, name="L"),
    re_path(r'detail/([0-9]+)', views.detail, name="D"),
    re_path(r'update/([0-9]+)', views.update, name="U"),
]