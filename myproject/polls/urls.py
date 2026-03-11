from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testurl', views.testView, name='testview'),
]