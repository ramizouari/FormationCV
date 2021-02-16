# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 02:42:05 2021

@author: Rami
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]