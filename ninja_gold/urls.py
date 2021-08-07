from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('second/<name>', views.second),
    path('process_money/<str:ubi>/',views.process_money),  
]
