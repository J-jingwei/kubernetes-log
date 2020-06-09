#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' a test module '''
__author__ = 'jiangjw'

from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index,name='index'),
    # path('favicon.ico/',RedirectView.as_view(url='/static/favicon.ico')),
]