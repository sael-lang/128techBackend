from django.urls import path
from . import views

urlpatterns = [
    path('create-course', views.register),
    path('get-course', views.show),
    path('get-course-trainer', views.showt),
    path('show-course-trainer', views.showtrainer),
]