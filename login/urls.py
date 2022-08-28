from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from . import views

# router = routers.DefaultRouter(trailing_slash=False)
# router.register('employee', views.Employee)

urlpatterns = [
    path('login', views.Employee.register),
    path('signin', views.Employee.login),
    path('get', views.Employee.getadmins),
    path('getrights', views.Employee.get_rights),
    path('updaterights', views.Employee.update_rights),
]

