from django.contrib import admin
from django.urls import path, include
from . import views
from courses.admin import admin_site

urlpatterns = [
    path('', views.index),

]

