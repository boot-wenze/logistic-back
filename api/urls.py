"""
URL configuration for logistique project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# pylint: disable=arguments-differ
# pylint: disable=unused-import
# pylint: disable=import-error
# pylint: disable=missing-docstring
# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-name-in-module

from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("order", views.order, name="order"),
    path("get_all_orders/<str:client_id>", views.get_all_orders, name="get_all_orders"),
]
