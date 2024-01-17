"""
URL configuration for zabbixindicators project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from .views import (report1, slas, clientes, clientes_add, clientes_edit, clientes_delete, slas_add, slas_edit, slas_delete, integracao_zabbix)

urlpatterns = [
    path('integracao/', integracao_zabbix),
    path('report1/', report1),
    path('clientes/', clientes),
    path('clientes/add/', clientes_add),
    path('clientes/<int:id>/edit/', clientes_edit),
    path('clientes/<int:id>/delete/', clientes_delete),
    path('slas/', slas),
    path('slas/add/', slas_add),
    path('slas/<int:id>/edit/', slas_edit),
    path('slas/<int:id>/delete/', slas_delete)
]
